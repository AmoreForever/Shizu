import logging
import asyncio
import contextlib
import sys

from aiogram import Bot, Dispatcher, exceptions
from pyrogram import Client

from typing import Union, NoReturn
from loguru import logger

from .events import Events
from .token_manager import TokenManager

from .. import database, types

with contextlib.suppress(Exception):
    bot = Bot(token=database.db.get("shizu.bot", "token", None), parse_mode="html")
    dp = Dispatcher(bot)
    
class BotManager(
    Events,
    TokenManager
):
    """Bot manager"""

    def __init__(
        self,
        app: Client,
        db: database.Database,
        all_modules: types.ModulesManager
    ) -> None:
        """Initializing a class

        Parameters:
            app (``program.Client`):
        Client

                    db (``database.Database`):
        Database

                    all_modules (`loader.Modules"):
        Modules
        """
        self._app = app
        self._db = db
        self._all_modules = all_modules
        self._token = self._db.get("shizu.bot", "token", None)

    async def load(self) -> Union[bool, NoReturn]:
        """Loads the bot manager"""
        if not self._token:
            logging.error("The token was not found. Attempt to recreate the token")
            token, bot_username = await self._find_bot()
            if token is False:
                logging.warning("Не удалось найти бота")
                logging.info("Создание бота...")
                token, bot_username = await self._create_bot()
            self._token = token
            self._bot_username = bot_username

            if self._token is False:
                error_text = "A user bot needs a bot. Solve the problem of creating a bot and start the user bot again"

                logging.error(error_text)
                return sys.exit(1)

            self._db.set("shizu.bot", "token", self._token)
            self._db.set("shizu.bot", "username", self._bot_username)

        try:
            self.bot = Bot(self._token, parse_mode="html")
        except (exceptions.ValidationError, exceptions.Unauthorized):
            logging.error("Invalid token. Attempt to recreate the token")

            self._db.set("shizu.bot", "token", self._token)
            self._db.set("shizu.bot", "username", self._bot_username)
            return await self.load()

        self._dp = Dispatcher(self.bot)
        self._dp.register_message_handler(
            self._message_handler, lambda _: True,
            content_types=["any"]
        )
        self._dp.register_inline_handler(
            self._inline_handler, lambda _: True
        )
        self._dp.register_callback_query_handler(
            self._callback_handler, lambda _: True
        )

        asyncio.ensure_future(
            self._dp.start_polling())

        self.bot.manager = self
        return True
