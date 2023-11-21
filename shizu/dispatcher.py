# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru

import random
import contextlib
import logging
import sys
import traceback

import inspect
from inspect import getfullargspec

from types import FunctionType

from pyrogram import Client, filters, types, raw
from pyrogram.handlers import MessageHandler, EditedMessageHandler

from . import loader, utils, database, logger as lo

logger = logging.getLogger(__name__)


async def check_filters(
    func: FunctionType,
    app: Client,
    message: types.Message,
) -> bool:
    db = database.db
    if custom_filters := getattr(func, "_filters", None):
        coro = custom_filters(app, message)

        if inspect.iscoroutine(coro):
            coro = await coro

        if not coro:
            return False

    if message.chat.id == db.get("shizu.me", "me", None):
        return True

    if (
        message.sender_chat.id if message.from_user is None else message.from_user.id
    ) in db.get("shizu.me", "owners", []) and db.get("shizu.owner", "status", False):
        return True

    if not message.outgoing:
        return False

    return True


class DispatcherManager:
    """Manager of dispatcher"""

    def __init__(self, app: Client, modules: "loader.ModulesManager") -> None:
        self.app = app
        self.modules = modules

    async def load(self) -> bool:
        """Loads dispatcher"""
        self.app.add_handler(handler=MessageHandler(self._handle_message, filters.all))
        self.app.add_handler(handler=EditedMessageHandler(self._handle_message, filters.all), group=random.randint(1, 1000))

        return True

    async def _handle_message(
        self, app: Client, message: types.Message
    ) -> types.Message:
        """Handle message"""""
        await self._handle_watchers(app, message)

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
            if (len(vars_ := getfullargspec(func).args) > 3) and (vars_[3] == "args"):
                args = utils.get_full_command(message)[2]
                await func(app, message, args)

            else:
                await func(app, message)

        except Exception:
            item = lo.CustomException.from_exc_info(*sys.exc_info())
            exc = item.message + "\n\n" + item.full_stack
            trace = traceback.format_exc().replace(
                "Traceback (most recent call last):\n", ""
            )

            with contextlib.suppress(Exception):
                log_message = f"⛳️ <b>Command <code>{prefix}{command}</code> failed with error:</b>\n\n{exc}\n"
                await app.inline_bot.send_animation(
                    app.db.get("shizu.chat", "logs", None),
                    "https://i.gifer.com/LRP3.gif",
                    caption=log_message,
                    parse_mode="HTML",
                )
                answer_message = f"<emoji id=5372892693024218813>🥶</emoji> <b>Command <code>{prefix}{command}</code> failed with error:</b>\n\n<code>{trace}</code>\n"
                await message.answer(answer_message)

        return message

    async def _handle_watchers(
        self, app: Client, message: types.Message
    ) -> types.Message:
        """Watcher Handler"""
        if isinstance(raw.types, raw.types.UpdatesTooLong):
            return 
        
        for watcher in self.modules.watcher_handlers:
            try:
                await watcher(app, message)
            except Exception as error:
                logging.exception(error)

        return message
