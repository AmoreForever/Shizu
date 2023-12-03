# Shizu Copyright (C) 2023-2024  AmoreForever

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import contextlib
import time
import os
import sys
import atexit
import logging

from pyrogram import Client
from pyrogram.raw import functions, types as typ

from aiogram.utils.exceptions import ChatNotFound

from .. import loader, utils
from ..version import __version__, branch


@loader.module(name="ShizuOnload", author="hikamoru")
class ShizuOnload(loader.Module):
    """This module for shizu onload events"""

    strings = {
        "start_r": "<emoji id=5017470156276761427>🔄</emoji> <b>The reboot was successful!</b>\n<emoji id=5451646226975955576>⌛️</emoji> The reboot took <code>{}</code> seconds",
        "start_u": "<emoji id=5258420634785947640>🔄</emoji> <b>The update was successful!</b>\n<emoji id=5451646226975955576>⌛️</emoji> The update took <code>{}</code> seconds",
    }

    strings_ru = {
        "start_r": "<emoji id=5017470156276761427>🔄</emoji> <b>Перезагрузка прошла успешно!</b>\n<emoji id=5451646226975955576>⌛️</emoji> Перезагрузка заняла <code>{}</code> секунд",
        "start_u": "<emoji id=5258420634785947640>🔄</emoji> <b>Обновление прошло успешно!</b>\n<emoji id=5451646226975955576>⌛️</emoji> Обновление заняло <code>{}</code> секунд",
    }

    strings_uz = {
        "start_r": "<emoji id=5017470156276761427>🔄</emoji> <b>Qayta yuklash muvaffaqiyatli o'tdi!</b>\n<emoji id=5451646226975955576>⌛️</emoji> Qayta yuklash <code>{}</code> soniyadan iborat",
        "start_u": "<emoji id=5258420634785947640>🔄</emoji> <b>Yangilash muvaffaqiyatli o'tdi!</b>\n<emoji id=5451646226975955576>⌛️</emoji> Yangilash <code>{}</code> soniyadan iborat",
    }

    strings_jp = {
        "start_r": "<emoji id=5017470156276761427>🔄</emoji> <b>再起動に成功しました！</b>\n<emoji id=5451646226975955576>⌛️</emoji> 再起動には <code>{}</code> 秒かかりました",
        "start_u": "<emoji id=5258420634785947640>🔄</emoji> <b>更新に成功しました！</b>\n<emoji id=5451646226975955576>⌛️</emoji> 更新には <code>{}</code> 秒かかりました",
    }

    strings_ua = {
        "start_r": "<emoji id=5017470156276761427>🔄</emoji> <b>Перезавантаження пройшло успішно!</b>\n<emoji id=5451646226975955576>⌛️</emoji> Перезавантаження зайняло <code>{}</code> секунд",
        "start_u": "<emoji id=5258420634785947640>🔄</emoji> <b>Оновлення пройшло успішно!</b>\n<emoji id=5451646226975955576>⌛️</emoji> Оновлення зайняло <code>{}</code> секунд",
    }

    strings_kz = {
        "start_r": "<emoji id=5017470156276761427>🔄</emoji> <b>Қайта іске қосу сәтті аяқталды!</b>\n<emoji id=5451646226975955576>⌛️</emoji> Қайта іске қосу <code>{}</code> секунд ұзақтығынан тұрады",
        "start_u": "<emoji id=5258420634785947640>🔄</emoji> <b>Жаңарту сәтті аяқталды!</b>\n<emoji id=5451646226975955576>⌛️</emoji> Жаңарту <code>{}</code> секунд ұзақтығынан тұрады",
    }

    async def on_load(self, app: Client):
        with contextlib.suppress(Exception):
            async for _ in app.get_dialogs():
                pass

            if not self.db.get("shizu.updater", "bot"):
                ms = await app.send_message("@shizu_ubot", "/start")
                await ms.delete()
                self.db.set("shizu.updater", "bot", True)

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
            if restart["type"] == "shizubot":
                await self.app.send_message("@shizu_ubot", "#updated")
            if restart["type"] == "update":
                restarted_text = self.strings("start_u").format(
                    round(time.time()) - int(restart["start"])
                )
            try:
                if restart["type"] != "shizubot":
                    await app.edit_message_text(
                        restart["chat"], restart["id"], restarted_text
                    )
            except Exception as why:
                logging.error(f"Failed to edit message: {why}")

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
