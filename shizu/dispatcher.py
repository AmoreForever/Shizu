# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru

import contextlib
import logging
import sys
import inspect
from inspect import getfullargspec, iscoroutine
from types import FunctionType

from pyrogram import Client, filters, types
from pyrogram.handlers import MessageHandler, EditedMessageHandler

from . import loader, utils, database, logger as lo

logger = logging.getLogger(__name__)


async def check_filters(
    func: FunctionType, app: Client, message: types.Message
) -> bool:
    db = database.db

    if custom_filters := getattr(func, "_filters", None):
        coro = custom_filters(app, message)

        if inspect.iscoroutine(coro):
            coro = await coro

        if not coro:
            return False

    elif message.chat.id == db.get("shizu.me", "me"):
        return True

    elif not message.outgoing:
        return False
    return True


class DispatcherManager:
    """Manager of dispatcher"""

    def __init__(self, app: Client, modules: "loader.ModulesManager") -> None:
        self.app = app
        self.modules = modules

    async def load(self) -> bool:
        """Загружает менеджер диспетчера"""
        self.app.add_handler(handler=MessageHandler(self._handle_message, filters.all))
        self.app.add_handler(
            handler=EditedMessageHandler(self._handle_message, filters.all)
        )

        return True

    async def _handle_message(
        self, app: Client, message: types.Message
    ) -> types.Message:
        """Обработчик сообщений"""
        await self._handle_watchers(app, message)
        await self._handle_other_handlers(app, message)

        prefix, command, args = utils.get_full_command(message)
        if not (command or args):
            return

        command = self.modules.aliases.get(command, command)
        func = self.modules.command_handlers.get(command.lower())
        if not func:
            return

        if not await check_filters(func, app, message):
            return

        try:
            if len(vars_ := getfullargspec(func).args) > 3 and vars_[3] == "args":
                await func(app, message, utils.get_full_command(message)[2])
            else:
                try:
                    await func(app, message)
                except Exception as error:
                    item = lo.CustomException.from_exc_info(*sys.exc_info())
                    exc = (
                        "\n\n"
                        + "\n".join(item.full_stack.splitlines()[:-1])
                        + "\n\n"
                        + "🎈 "
                        + item.full_stack.splitlines()[-1]
                    )
                    with contextlib.suppress(Exception):
                        await app.inline_bot.send_message(
                            app.db.get("shizu.chat", "logs", None),
                            f"⛩ <b>Command <code>{prefix}{command}</code> failed with error:</b>\n\n"
                            "🚇 <b>Traceback:</b>"
                            f"{exc}\n",
                            parse_mode="HTML",
                        )
                        await message.answer(
                            f"<emoji id=5019455638053323673>❌</emoji> <b>Command <code>{prefix}{command}</code> failed with error:</b>\n"
                            f"<code>{error}</code>\n",
                        )
        except Exception as error:
            item = lo.CustomException.from_exc_info(*sys.exc_info())
            exc = (
                "\n\n"
                + "\n".join(item.full_stack.splitlines()[:-1])
                + "\n\n"
                + "🎈 "
                + item.full_stack.splitlines()[-1]
            )

            with contextlib.suppress(Exception):
                await app.inline_bot.send_message(
                    app.db.get("shizu.chat", "logs", None),
                    f"⛩ <b>Command <code>{prefix}{command}</code> failed with error:</b>\n\n"
                    "🚇 <b>Traceback:</b>"
                    f"{exc}\n",
                    parse_mode="HTML",
                )
                await message.answer(
                    f"<emoji id=5019455638053323673>❌</emoji> <b>Command <code>{prefix}{command}</code> failed with error:</b>\n"
                    f"<code>{error}</code>\n",
                )

        return message

    async def _handle_watchers(
        self, app: Client, message: types.Message
    ) -> types.Message:
        """Watcher Handler"""
        for watcher in self.modules.watcher_handlers:
            try:
                if not await check_filters(watcher, app, message):
                    continue

                await watcher(app, message)
            except Exception as error:
                logging.exception(error)

        return message

    async def _handle_other_handlers(
        self, app: Client, message: types.Message
    ) -> types.Message:
        """Handler for other handlers"""
        for handler in app.dispatcher.groups[0]:
            if (
                getattr(handler.callback, "__func__", None)
                == DispatcherManager._handle_message
            ):
                continue

            coro = handler.filters(app, message)
            if iscoroutine(coro):
                coro = await coro

            if not coro:
                continue

            try:
                handler = handler.callback(app, message)
                if iscoroutine(handler):
                    await handler
            except Exception as error:
                logging.exception(error)
        return message
