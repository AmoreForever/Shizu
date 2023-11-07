import time
import os
import sys
import atexit
import logging

from .. import loader, utils
from ..version import __version__, branch

from pyrogram import Client
from pyrogram.raw import functions, types as typ

from aiogram.utils.exceptions import ChatNotFound


@loader.module(name="ShizuOnload", author="hikamoru")
class ShizuOnload(loader.Module):
    """This module for shizu onload events"""

    async def on_load(self, app: Client):
        if not self.db.get("shizu.folder", "folder"):
            logging.info("Trying to create folder")
            app.me = await app.get_me()
            folder_id = 250
            logs_id = (
                await utils.create_chat(
                    app,
                    "Shizu-logs",
                    "📫 Shizu-logs do not delete this group, otherwise bot will be broken",
                    True,
                    True,
                    True,
                )
            ).id

            backup_id = (
                await utils.create_chat(
                    app,
                    "Shizu-backup",
                    "📫 Backup-logs do not delete this group, otherwise bot will be broken",
                    True,
                    True,
                    True,
                )
            ).id

            logs = await app.resolve_peer(logs_id)
            backup = await app.resolve_peer(backup_id)

            await app.set_chat_photo(chat_id=logs_id, photo="assets/logs.jpg")
            await app.set_chat_photo(chat_id=backup_id, photo="assets/backups.jpg")

            await app.invoke(
                functions.messages.UpdateDialogFilter(
                    id=folder_id,
                    filter=typ.DialogFilter(
                        id=folder_id,
                        title="Shizu",
                        include_peers=[logs, backup],
                        pinned_peers=[],
                        exclude_peers=[],
                        emoticon="❤️",
                    ),
                )
            )

            logging.info("Folder created")
            self.db.set("shizu.folder", "folder", True)
            self.db.set("shizu.chat", "logs", logs_id)
            self.db.set("shizu.chat", "backup", backup_id)
            atexit.register(os.execl(sys.executable, sys.executable, "-m", "shizu"))

        if restart := self.db.get("shizu.updater", "restart"):
            if restart["type"] == "restart":
                restarted_text = self.strings("start_r").format(
                    round(time.time()) - int(restart["start"])
                )
            else:
                restarted_text = self.strings("start_u").format(
                    round(time.time()) - int(restart["start"])
                )

            try:
                await app.edit_message_text(
                    restart["chat"], restart["id"], restarted_text
                )
            except Exception as why:
                logging.error(f"Failed to edit message: {why}")
            logging.info("Successfully started!")
            self.db.pop("shizu.updater", "restart")

        started_text = (
            f"🐙 <b>Your <u>Shizu</u> started</b> <code>v{'.'.join(map(str, __version__))}</code>\n\n"
            f"🌳 <b>Branch:</b> <code>{branch}</code>\n"
        )
        try:
            await self._bot.send_photo(
                chat_id=self.db.get("shizu.chat", "logs", None),
                photo=open("assets/Shizu.jpg", "rb"),
                caption=started_text,
                parse_mode="HTML",
            )
        except ChatNotFound:
            await utils.invite_bot(app, self.db.get("shizu.chat", "logs", None))
            await self._bot.send_photo(
                chat_id=self.db.get("shizu.chat", "logs", None),
                photo=open("assets/Shizu.jpg", "rb"),
                caption=started_text,
                parse_mode="HTML",
            )
        except Exception:
            pass
