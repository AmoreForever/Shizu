import logging
import re
from loguru import logger
from typing import Tuple

from pyrogram import errors, types

from .. import fsm, utils
from .types import Item

FIND = True


class TokenManager(Item):
    """Менеджер токенов"""

    async def _find_bot(self) -> Union[Tuple[str, str], None]:
        """Find the bot"""
        async with fsm.Conversation(self._app, "@BotFather", True) as conv:
            logging.info("Checking for the presence of a bot...")

            try:
                await conv.ask("/cancel")
            except errors.UserIsBlocked:
                await self._app.unblock_user("@BotFather")

            await conv.get_response()
            await conv.ask("/mybots")
            r = await conv.get_response()

            if not r.reply_markup:
                return None  # Bot not found

            data = r.reply_markup.inline_keyboard
            buttons_text = [button.text for row in data for button in row]

            if not buttons_text:
                logger.error("The bot was not found, attempting to create a new bot...")
                return None  # Bot not found

            buttons = [
                index
                for index, item in enumerate(buttons_text)
                if "shizu" in item.lower()
            ]
            logger.success("Found bot: %s", buttons_text[buttons[0]])
            resp = await conv.get_response()
            await resp.click(buttons[0])

            h2 = await conv.get_another_same()
            await h2.click(0)

            response = await conv.get_response()
            token_match = re.search(r"(\d+:[A-Za-z0-9_-]+)", response.text)
            username_match = re.search(r"@(\w+)", response.text)

            if token_match and username_match:
                return token_match[1], username_match[1]
            else:
                return None  # Bot not found

    async def _create_bot(self) -> Union[str, None]:
        """Create and configure a bot"""
        async with fsm.Conversation(self._app, "@BotFather", True) as conv:
            logging.info("The process of creating a new bot has begun...")

            try:
                await conv.ask("/cancel")
            except errors.UserIsBlocked:
                await self._app.unblock_user("@BotFather")

            await conv.get_response()
            await conv.ask("/newbot")
            response = await conv.get_response()

            error_phrases = ["That I cannot do.", "Sorry"]

            if any(phrase in response.text for phrase in error_phrases):
                logging.error(
                    "An error occurred when creating the bot. @BotFather's response:"
                )
                logging.error(response.text)

                if "too many attempts" in response.text:
                    seconds = response.text.split()[-2]
                    logger.error(f"Please repeat in {seconds} seconds")

            bot_username = f"shizu_{utils.random_id(6)}_bot"

            await conv.ask(
                f"🐙 Shizu UserBot of {utils.get_display_name(self._all_modules.me)[:45]}"
            )
            await conv.get_response()

            await conv.ask(bot_username)

            response = await conv.get_response()

            search = re.search(r"(?<=<code>)(.*?)(?=</code>)", response.text.html)
            if not search:
                logging.error(
                    "An error occurred when creating the bot. @BotFather's response:"
                )
                return logging.error(response.text)

            token = search[0]

            await conv.ask("/setuserpic")
            await conv.get_response()

            await conv.ask(f"@{bot_username}")
            await conv.get_response()

            self._app.me = await self._app.get_me()
            await conv.ask_media("assets/bot.jpg", media_type="photo")
            await conv.get_response()

            await conv.ask("/setinline")
            await conv.get_response()

            await conv.ask(f"@{bot_username}")
            await conv.get_response()

            await conv.ask("shizu>>")
            await conv.get_response()

            logger.success(f"Bot successfully created @{bot_username}")

            return token, bot_username
