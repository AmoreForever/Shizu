#    Sh1t-UB (telegram userbot by sh1tn3t)
#    Copyright (C) 2021-2022 Sh1tN3t

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru

import os
import sys
import time
import logging
import atexit

from subprocess import check_output

from pyrogram import Client, types, enums

from .. import loader, utils
from ..version import __version__, branch

from aiogram.utils.exceptions import ChatNotFound


@loader.module(name="ShizuUpdater", author="shizu")
class UpdateMod(loader.Module):
    """Updates itself"""

    strings = {
        "last_": "<emoji id=5188420746694633417>🌗</emoji> <b>You have the latest version installed</b>.",
        "update_": "🔁 Update...",
        "reboot_": "<b><emoji id=5328274090262275771>🔁</emoji> Rebooting...</b>",
        "start_r": "<emoji id=5017470156276761427>🔄</emoji> <b>The reboot was successful!</b>\n<emoji id=5451646226975955576>⌛️</emoji> The reboot took <code>{}</code> seconds",
        "start_u": "<emoji id=5258420634785947640>🔄</emoji> <b>The update was successful!</b>\n<emoji id=5451646226975955576>⌛️</emoji> The update took <code>{}</code> seconds",
    }

    strings_ru = {
        "last_": "<emoji id=5188420746694633417>🌗</emoji> <b>У вас установлена последняя версия</b>.",
        "update_": "🔁 Обновление...",
        "reboot_": "<b><emoji id=5328274090262275771>🔁</emoji> Перезагрузка...</b>",
        "start_r": "<emoji id=5017470156276761427>🔄</emoji> <b>Перезагрузка прошла успешно!</b>\n<emoji id=5451646226975955576>⌛️</emoji> Перезагрузка заняла <code>{}</code> секунд",
        "start_u": "<emoji id=5258420634785947640>🔄</emoji> <b>Обновление прошло успешно!</b>\n<emoji id=5451646226975955576>⌛️</emoji> Обновление заняло <code>{}</code> секунд",
    }

    strings_uz = {
        "last_": "<emoji id=5188420746694633417>🌗</emoji> <b>Shizu botningizning yangi versiyasi</b>.",
        "update_": "🔁 Yangilash...",
        "reboot_": "<b><emoji id=5328274090262275771>🔁</emoji> Qayta yuklash...</b>",
        "start_r": "<emoji id=5017470156276761427>🔄</emoji> <b>Qayta yuklash muvaffaqiyatli o'tdi!</b>\n<emoji id=5451646226975955576>⌛️</emoji> Qayta yuklash <code>{}</code> soniyadan iborat",
        "start_u": "<emoji id=5258420634785947640>🔄</emoji> <b>Yangilash muvaffaqiyatli o'tdi!</b>\n<emoji id=5451646226975955576>⌛️</emoji> Yangilash <code>{}</code> soniyadan iborat",
    }

    strings_jp = {
        "last_": "<emoji id=5188420746694633417>🌗</emoji> <b>最新バージョンがインストールされています</b>.",
        "update_": "🔁 更新...",
        "reboot_": "<b><emoji id=5328274090262275771>🔁</emoji> 再起動...</b>",
        "start_r": "<emoji id=5017470156276761427>🔄</emoji> <b>再起動に成功しました！</b>\n<emoji id=5451646226975955576>⌛️</emoji> 再起動には <code>{}</code> 秒かかりました",
        "start_u": "<emoji id=5258420634785947640>🔄</emoji> <b>更新に成功しました！</b>\n<emoji id=5451646226975955576>⌛️</emoji> 更新には <code>{}</code> 秒かかりました",
    }

    strings_ua = {
        "last_": "<emoji id=5188420746694633417>🌗</emoji> <b>У вас встановлена остання версія</b>.",
        "update_": "🔁 Оновлення...",
        "reboot_": "<b><emoji id=5328274090262275771>🔁</emoji> Перезавантаження...</b>",
        "start_r": "<emoji id=5017470156276761427>🔄</emoji> <b>Перезавантаження пройшло успішно!</b>\n<emoji id=5451646226975955576>⌛️</emoji> Перезавантаження зайняло <code>{}</code> секунд",
        "start_u": "<emoji id=5258420634785947640>🔄</emoji> <b>Оновлення пройшло успішно!</b>\n<emoji id=5451646226975955576>⌛️</emoji> Оновлення зайняло <code>{}</code> секунд",
    }

    strings_kz = {
        "last_": "<emoji id=5188420746694633417>🌗</emoji> <b>Сізде соңғы нұсқа орнатылған</b>.",
        "update_": "🔁 Жаңарту...",
        "reboot_": "<b><emoji id=5328274090262275771>🔁</emoji> Қайта іске қосу...</b>",
        "start_r": "<emoji id=5017470156276761427>🔄</emoji> <b>Қайта іске қосу сәтті аяқталды!</b>\n<emoji id=5451646226975955576>⌛️</emoji> Қайта іске қосу <code>{}</code> секунд ұзақтығынан тұрады",
        "start_u": "<emoji id=5258420634785947640>🔄</emoji> <b>Жаңарту сәтті аяқталды!</b>\n<emoji id=5451646226975955576>⌛️</emoji> Жаңарту <code>{}</code> секунд ұзақтығынан тұрады",
    }

    async def on_load(self, app: Client):
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

    @loader.command()
    async def update(self, app: Client, message: types.Message):
        """Updates itself"""
        try:
            await message.answer("Update attempt...")
            check_output("git stash", shell=True).decode()
            output = check_output("git pull", shell=True).decode()
            if "Already up to date." in output:
                return await message.answer(
                    self.strings("last_"),
                )
            self.db.set(
                "shizu.updater",
                "restart",
                {
                    "chat": message.chat.username
                    if message.chat.type == enums.ChatType.BOT
                    else message.chat.id,
                    "id": message.id,
                    "start": str(round(time.time())),
                    "type": "update",
                },
            )

            await message.answer(self.strings("update_"))

            atexit.register(os.execl(sys.executable, sys.executable, "-m", "shizu"))
            return sys.exit(0)
        except Exception as error:
            await message.answer(f"An error occurred: {error}")

    @loader.command()
    async def restart(self, app: Client, message: types.Message):
        """Rebooting the user bot"""
        ms = await message.answer(self.strings("reboot_"))
        self.db.set(
            "shizu.updater",
            "restart",
            {
                "chat": message.chat.id,
                "id": ms.id,
                "start": time.time(),
                "type": "restart",
            },
        )

        atexit.register(os.execl(sys.executable, sys.executable, "-m", "shizu"))
        return sys.exit(0)
