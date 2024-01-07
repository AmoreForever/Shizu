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

# ---------------------------------------------------------------------------


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
import os
import sys
import time
import atexit

from subprocess import check_output

from pyrogram import Client, types, enums

from .. import loader, utils
from ..version import __version__, branch


@loader.module(name="ShizuUpdater", author="shizu")
class UpdateMod(loader.Module):
    """Updates itself"""

    strings = {
        "last_": "<emoji id=5188420746694633417>🌗</emoji> <b>You have the latest version installed</b>.",
        "update_": "🔁 Update...",
        "reboot_": "<b><emoji id=5328274090262275771>🔁</emoji> Rebooting...</b>",
    }

    strings_ru = {
        "last_": "<emoji id=5188420746694633417>🌗</emoji> <b>У вас установлена последняя версия</b>.",
        "update_": "🔁 Обновление...",
        "reboot_": "<b><emoji id=5328274090262275771>🔁</emoji> Перезагрузка...</b>",
    }

    strings_uz = {
        "last_": "<emoji id=5188420746694633417>🌗</emoji> <b>Shizu botningizning yangi versiyasi</b>.",
        "update_": "🔁 Yangilash...",
        "reboot_": "<b><emoji id=5328274090262275771>🔁</emoji> Qayta yuklash...</b>",
    }

    strings_jp = {
        "last_": "<emoji id=5188420746694633417>🌗</emoji> <b>最新バージョンがインストールされています</b>.",
        "update_": "🔁 更新...",
        "reboot_": "<b><emoji id=5328274090262275771>🔁</emoji> 再起動...</b>",
    }

    strings_ua = {
        "last_": "<emoji id=5188420746694633417>🌗</emoji> <b>У вас встановлена остання версія</b>.",
        "update_": "🔁 Оновлення...",
        "reboot_": "<b><emoji id=5328274090262275771>🔁</emoji> Перезавантаження...</b>",
    }

    strings_kz = {
        "last_": "<emoji id=5188420746694633417>🌗</emoji> <b>Сізде соңғы нұсқа орнатылған</b>.",
        "update_": "🔁 Жаңарту...",
        "reboot_": "<b><emoji id=5328274090262275771>🔁</emoji> Қайта іске қосу...</b>",
    }

    strings_kr = {
        "last_": "<emoji id=5188420746694633417>🌗</emoji> <b>최신 버전이 설치되어 있습니다</b>.",
        "update_": "🔁 업데이트...",
        "reboot_": "<b><emoji id=5328274090262275771>🔁</emoji> 재부팅...</b>",
    }

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