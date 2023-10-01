import inspect
import logging

from aiogram.types import (
    CallbackQuery,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from .. import utils
from .types import Item
from .. import database

TEXT = (
    "🌘 <b><a href='https://github.com/AmoreForever/Shizu'>Shizu Userbot</a></b>\n\n\n"
    "💫 A userbot can be characterized as a <b>third-party software application</b> that engages with the Telegram API in order to execute <b>automated operations on behalf of an end user</b>. These userbots possess the capability to streamline a variety of tasks, encompassing activities such as <b>dispatching messages, enrolling in channels, retrieving media files, and more</b>.\n\n"
    "😎 Diverging from conventional Telegram bots, <b>userbots operate within the confines of a user's account</b> rather than within a dedicated bot account. This particular distinction empowers userbots with enhanced accessibility to a broader spectrum of functionalities and a heightened degree of flexibility in executing actions.\n\n"
    )

class Events(Item):
    """Обработчик событий"""

    async def _message_handler(self, message: Message) -> Message:
        """Обработчик сообщений"""
        if message.text == "/start":
            if message.chat.type != "private":
                return
            await message.answer_photo(
                open("assets/Shizu.jpg", "rb"),
                caption="🐙 <b>Shizu – Your Secret Telegram Weapon! With plugin support and effortless setup, this bot unlocks a world of possibilities in Telegram. Dive in and experience the extraordinary!</b>\n\n🧑‍💻 <b>hikamoru.t.me</b>",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(
                        text="🌍 Github", url="https://github.com/AmoreForever/Shizu"
                    )
                ),
            )
        if message.text == '/userbot':
            if message.chat.type != "private":
                return False
            await message.answer(TEXT, parse_mode="HTML", disable_web_page_preview=True)
        
        for func in self._all_modules.message_handlers.values():
            if not await self._check_filters(func, func.__self__, message):
                continue
            try:
                await func(self._app, message)
            except Exception as error:
                logging.exception(error)
        return message

    async def _callback_handler(self, call: CallbackQuery) -> CallbackQuery:
        """Обработчик каллбек-хендлеров"""
        if call.from_user.id != database.db.get("shizu.me", "me"):
            return await call.answer("Hands off my buttons!", show_alert=True)
        for func in self._all_modules.callback_handlers.values():
            if not await self._check_filters(func, func.__self__, call):
                continue

            try:
                await func(self._app, call)
            except Exception as error:
                logging.exception(error)

        return call

    async def _inline_handler(self, inline_query: InlineQuery) -> InlineQuery:
        """Обработчик инлайн-хендеров"""
        if inline_query.from_user.id != database.db.get("shizu.me", "me"):
            return await inline_query.answer(
                [
                    InlineQueryResultArticle(
                        id=utils.random_id(),
                        title="Available only for the owner of the user bot",
                        input_message_content=InputTextMessageContent(
                            "🚸 <b>Unfortunately, this is only available to the owner of the user bot</b>"
                        ),
                        thumb_url="https://cdn-icons-png.flaticon.com/512/7754/7754235.png",
                    )
                ],
                cache_time=0,
            )

        if not (query := inline_query.query):
            commands = ""
            for command, func in self._all_modules.inline_handlers.items():
                if await self._check_filters(func, func.__self__, inline_query):
                    commands += (
                        f"\n💬 <code>@{(await self.bot.me).username} {command}</code>"
                    )

            message = InputTextMessageContent(
                f"👇 <b>Available commands</b>\n" f"{commands}"
            )

            return await inline_query.answer(
                [
                    InlineQueryResultArticle(
                        id=utils.random_id(),
                        title="Available commands",
                        description="👇 Available commands",
                        input_message_content=message,
                        thumb_url="https://cdn-icons-png.flaticon.com/512/5278/5278692.png",
                    )
                ],
                cache_time=0,
            )

        query_ = query.split()

        cmd = query_[0]
        args = " ".join(query_[1:])

        func = self._all_modules.inline_handlers.get(cmd)
        if not func:
            return await inline_query.answer(
                [
                    InlineQueryResultArticle(
                        id=utils.random_id(),
                        title="Error",
                        description="🤷‍♂️ There is no such inline command",
                        input_message_content=InputTextMessageContent(
                            "🤷‍♂️ <b>There is no such inline command</b>"
                        ),
                        thumb_url="https://cdn-icons-png.flaticon.com/512/10621/10621123.png",
                    )
                ],
                cache_time=0,
            )

        if not await self._check_filters(func, func.__self__, inline_query):
            return

        try:
            if (
                len(vars_ := inspect.getfullargspec(func).args) > 3
                and vars_[3] == "args"
            ):
                await func(self._app, inline_query, args)
            else:
                await func(self._app, inline_query)
        except Exception as error:
            logging.exception(error)

        return inline_query
