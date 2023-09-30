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
import zipfile
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
            app.db.get("shizu.chat", "backup"), document=txt, caption="Database backup"
        )
        await utils.answer(
            message,
            "<emoji id=5260416304224936047>✅</emoji> Backup created\nCheck backup in <b>backups chat</b>",
        )

    @loader.command()
    async def restoredb(self, app: Client, message: types.Message):
        """Easy restore database"""
        reply = message.reply_to_message
        if not reply or not reply.document:
            return await utils.answer(message, "❌ Нет файла")
        await utils.answer(
            message,
            "<emoji id=5370706614800097423>🧐</emoji> <b>Restoring database...</</b>",
        )
        file = await app.download_media(reply.document)
        decoded_text = json.loads(io.open(file, "r", encoding="utf-8").read())
        if not file.endswith(".json"):
            return await utils.answer(
                message, "<emoji id=5413472879771658264>❌</emoji> Invalid file format"
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

        ms = await utils.answer(
            message, "<b><emoji id=5328274090262275771>🔁</emoji> Restarting...</b>"
        )
        self.db.set(
            "shizu.updater",
            "restart",
            {
                "chat": message.chat.username if message.chat.type == enums.ChatType.BOT else message.chat.id,
                "id": ms.id,
                "start": time.time(),
                "type": "restart",
            },
        )
        logging.info("Перезагрузка...")
        atexit.register(restart)
        return sys.exit(0)

    # @loader.command()
    # async def backupmods(self, app: Client, message: types.Message):
    #     """Create backup of all modules"""
    #     mods_quantity = len(self.db.get("shizu.loader", "modules", {}))

    #     result = io.BytesIO()
    #     result.name = "mods.zip"

    #     db_mods = json.dumps(self.db.get("shizu.loader", "modules", {})).encode()

    #     with zipfile.ZipFile(result, "w", zipfile.ZIP_DEFLATED) as zipf:
    #         for root, _, files in os.walk(LOADED_MODULES_DIR):
    #             for file in files:
    #                 with open(os.path.join(root, file), "rb") as f:
    #                     zipf.writestr(file, f.read())
    #                     mods_quantity += 1

    #         zipf.writestr("db_mods.json", db_mods)

    #     archive = io.BytesIO(result.getvalue())
    #     archive.name = f"mods-{datetime.now():%d-%m-%Y-%H-%M}.zip"
    #     await app.inline_bot.send_document(
    #         app.db.get("shizu.chat", "backup"),
    #         document=archive,
    #         caption="Modules backup",
    #     )

    # @loader.command()
    # async def restoremods(self, app: Client, message: types.Message):
    #     """Easy restore modules"""
    #     reply = message.reply_to_message
    #     if not reply or not reply.document:
    #         return await utils.answer(message, "❌ Нет файла")
    #     await utils.answer(
    #         message,
    #         "<emoji id=5370706614800097423>🧐</emoji> <b>Restoring modules...</b>",
    #     )
    #     file = await app.download_media(reply.document)
    #     if not file.endswith(".zip"):
    #         return await utils.answer(
    #             message, "<emoji id=5413472879771658264>❌</emoji> Invalid file format"
    #         )
    #     with zipfile.ZipFile(file, "r") as zipf:
    #         zipf.extractall(LOADED_MODULES_DIR)
    #     await app.send_message(
    #         message.chat.id,
    #         "<emoji id=5870888735041655084>📁</emoji> <b>Mods successfully loaded</b>",
    #     )
    #     m = await utils.answer(
    #         message, "<b><emoji id=5328274090262275771>🔁</emoji> Restarting...</b>"
    #     )
    #     self.db.set(
    #         "shizu.updater",
    #         "restart",
    #         {"chat": m.chat.id, "id": m.id, "start": time.time(), "type": "restart"},
    #     )
    #     atexit.register(os.execl(sys.executable, sys.executable, "-m", "shizu"))
    #     logging.info("Перезагрузка...")
    #     return sys.exit(0)
