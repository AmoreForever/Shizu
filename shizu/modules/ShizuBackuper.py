# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru

import os
import io
import json
import atexit
import logging
import time
import sys

from datetime import datetime
from pyrogram import Client, types, enums

from .. import loader, utils


LOADED_MODULES_DIR = os.path.join(os.getcwd(), "shizu/modules")


@loader.module(name="ShizuBackuper", author="hikamoru")
class BackupMod(loader.Module):
    """With this module you can make backups of mods and the entire userbot"""

    @loader.command()
    async def backupdb(self, app: Client, message: types.Message):
        """Create database backup [will be sent in backups chat]"""
        txt = io.BytesIO(json.dumps(self.db).encode("utf-8"))
        txt.name = f"shizu-{datetime.now().strftime('%d-%m-%Y-%H-%M')}.json"
        await app.inline_bot.send_document(
            app.db.get("shizu.chat", "backup"),
            document=txt,
            caption=f"👉 <b>Database backup</b>\n🕔 <b>{datetime.now().strftime('%d-%m-%Y %H:%M')}</b>",
        )
        await message.answer(
            "<emoji id=5260416304224936047>✅</emoji> Backup created\nCheck backup in <b>backups chat</b>",
        )

    @loader.command()
    async def restoredb(self, app: Client, message: types.Message):
        """Easy restore database"""
        reply = message.reply_to_message
        if not reply or not reply.document:
            return await message.answer("❌ Нет файла")
        await message.answer(
            "<emoji id=5370706614800097423>🧐</emoji> <b>Restoring database...</</b>",
        )
        file = await app.download_media(reply.document)
        decoded_text = json.loads(io.open(file, "r", encoding="utf-8").read())
        if not file.endswith(".json"):
            return await message.answer(
                "<emoji id=5413472879771658264>❌</emoji> Invalid file format"
            )
        self.db.reset()
        self.db.update(**decoded_text)
        self.db.save()
        await app.send_message(
            message.chat.id,
            "<emoji id=5870888735041655084>📁</emoji> <b>Backup successfully loaded</b>",
        )

        def restart() -> None:
            """Запускает загрузку юзербота"""
            os.execl(sys.executable, sys.executable, "-m", "shizu")

        ms = await message.answer(
            "<b><emoji id=5328274090262275771>🔁</emoji> Restarting...</b>"
        )
        self.db.set(
            "shizu.updater",
            "restart",
            {
                "chat": message.chat.username
                if message.chat.type == enums.ChatType.BOT
                else message.chat.id,
                "id": ms.id,
                "start": time.time(),
                "type": "restart",
            },
        )
        logging.info("restart...")
        atexit.register(restart)
        return sys.exit(0)

    @loader.command()
    async def abackup(self, app: Client, message: types.Message):
        """Enable/disable autobackup it will backup database everyday"""
        if not self.db.get("shizu.backuper", "autobackup", None):
            self.db.set("shizu.backuper", "autobackup", True)
            await message.answer(
                "<emoji id=5260416304224936047>✅</emoji> <b>Autobackup <u>enabled</u></b>"
            )
        else:
            self.db.set("shizu.backuper", "autobackup", None)
            await message.answer(
                "<emoji id=5260416304224936047>✅</emoji> <b>Autobackup <u>disabled</u></b>"
            )

    @loader.loop(interval=86000, autostart=True)
    async def autobackupmods(self):
        if not self.db.get("shizu.backuper", "autobackup", None):
            return
        txt = io.BytesIO(json.dumps(self.db).encode("utf-8"))
        txt.name = f"shizu-{datetime.now().strftime('%d-%m-%Y-%H-%M')}.json"
        await self._bot.send_document(
            self.db.get("shizu.chat", "backup"),
            document=txt,
            caption=f"👉 <b>Database backup</b>\n🕔 <b>{datetime.now().strftime('%d-%m-%Y %H:%M')}</b>",
        )
