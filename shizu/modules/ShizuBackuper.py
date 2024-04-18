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

import os
import io
import json
import time

from datetime import datetime
from pyrogram import Client, types, enums

from .. import loader, utils


LOADED_MODULES_DIR = os.path.join(os.getcwd(), "shizu/modules")


@loader.module(name="ShizuBackuper", author="hikamoru")
class BackupMod(loader.Module):
    """With this module you can make backups of mods and the entire userbot"""

    strings = {
        "backup": "👉 <b>Database backup</b>\n🕔 <b>{}</b>",
        "done": "<emoji id=5260416304224936047>✅</emoji> Backup created\nCheck backup in <b>backups chat</b>",
        "restoring": "<emoji id=5370706614800097423>🧐</emoji> <b>Restoring database...</</b>",
        "invalid": "<emoji id=5413472879771658264>❌</emoji> Invalid file format",
        "loaded": "<emoji id=5870888735041655084>📁</emoji> <b>Backup successfully loaded</b>",
        "restart": "<b><emoji id=5328274090262275771>🔁</emoji> Restarting...</b>",
        "enabled": "<emoji id=5260416304224936047>✅</emoji> <b>Autobackup <u>enabled</u></b>",
        "disabled": "<emoji id=5260416304224936047>✅</emoji> <b>Autobackup <u>disabled</u></b>",
    }

    strings_ru = {
        "backup": "👉 <b>Бэкап базы</b>\n🕔 <b>{}</b>",
        "done": "<emoji id=5260416304224936047>✅</emoji> Бэкап создан\nПроверьте бэкап в <b>бэкаповом чате</b>",
        "restoring": "<emoji id=5370706614800097423>🧐</emoji> <b>Восстановление базы...</</b>",
        "invalid": "<emoji id=5413472879771658264>❌</emoji> Недопустимый формат",
        "loaded": "<emoji id=5870888735041655084>📁</emoji> <b>Бэкап успешно загружен</b>",
        "restart": "<b><emoji id=5328274090262275771>🔁</emoji> Перезапуск...</b>",
        "enabled": "<emoji id=5260416304224936047>✅</emoji> <b>Автобэкап <u>включен</u></b>",
        "disabled": "<emoji id=5260416304224936047>✅</emoji> <b>Автобэкап <u>отключен</u></b>",
    }

    strings_uz = {
        "backup": "👉 <b>Bazani bekapi</b>\n🕔 <b>{}</b>",
        "done": "<emoji id=5260416304224936047>✅</emoji> Bekap yaratildi\nYuklab olish <b>backups chat</b>",
        "restoring": "<emoji id=5370706614800097423>🧐</emoji> <b>Yozish...</</b>",
        "invalid": "<emoji id=5413472879771658264>❌</emoji> Xatolik",
        "loaded": "<emoji id=5870888735041655084>📁</emoji> <b>Bekap yuklandi</b>",
        "restart": "<b><emoji id=5328274090262275771>🔁</emoji> Restart...</b>",
        "enabled": "<emoji id=5260416304224936047>✅</emoji> <b>Autobekap <u>aktiv</u></b>",
        "disabled": "<emoji id=5260416304224936047>✅</emoji> <b>Autobekap <u>deaktiv</u></b>",
    }

    strings_jp = {
        "backup": "👉 <b>データベースのバックアップ</b>\n🕔 <b>{}</b>",
        "done": "<emoji id=5260416304224936047>✅</emoji> バックアップが作成されました\nバックアップを確認する <b>backups chat</b>",
        "restoring": "<emoji id=5370706614800097423>🧐</emoji> <b>データベースの復元...</</b>",
        "invalid": "<emoji id=5413472879771658264>❌</emoji> 無効なファイル形式",
        "loaded": "<emoji id=5870888735041655084>📁</emoji> <b>バックアップが正常にロードされました</b>",
        "restart": "<b><emoji id=5328274090262275771>🔁</emoji> 再起動...</b>",
        "enabled": "<emoji id=5260416304224936047>✅</emoji> <b>自動バックアップ <u>有効</u></b>",
        "disabled": "<emoji id=5260416304224936047>✅</emoji> <b>自動バックアップ <u>無効</u></b>",
    }

    strings_ua = {
        "backup": "👉 <b>Бекап бази</b>\n🕔 <b>{}</b>",
        "done": "<emoji id=5260416304224936047>✅</emoji> Бекап створено\nПеревірте бекап в <b>бекаповому чаті</b>",
        "restoring": "<emoji id=5370706614800097423>🧐</emoji> <b>Відновлення бази...</</b>",
        "invalid": "<emoji id=5413472879771658264>❌</emoji> Неприпустимий формат",
        "loaded": "<emoji id=5870888735041655084>📁</emoji> <b>Бекап успішно завантажено</b>",
        "restart": "<b><emoji id=5328274090262275771>🔁</emoji> Перезапуск...</b>",
        "enabled": "<emoji id=5260416304224936047>✅</emoji> <b>Автобекап <u>увімкнено</u></b>",
        "disabled": "<emoji id=5260416304224936047>✅</emoji> <b>Автобекап <u>вимкнено</u></b>",
    }

    strings_kz = {
        "backup": "👉 <b>Деректер базасының резерттеуі</b>\n🕔 <b>{}</b>",
        "done": "<emoji id=5260416304224936047>✅</emoji> Резерттеу жасалды\nРезерттеуді тексеріңіз <b>backups chat</b>",
        "restoring": "<emoji id=5370706614800097423>🧐</emoji> <b>Деректер базасын қалпына келтіру...</</b>",
        "invalid": "<emoji id=5413472879771658264>❌</emoji> Қате формат",
        "loaded": "<emoji id=5870888735041655084>📁</emoji> <b>Резерттеу сәтті жүктелді</b>",
        "restart": "<b><emoji id=5328274090262275771>🔁</emoji> Қайта іске қосу...</b>",
        "enabled": "<emoji id=5260416304224936047>✅</emoji> <b>Авторезерттеу <u>қосылған</u></b>",
        "disabled": "<emoji id=5260416304224936047>✅</emoji> <b>Авторезерттеу <u>өшірілген</u></b>",
    }

    strings_kr = {
        "backup": "👉 <b>데이터베이스 백업</b>\n🕔 <b>{}</b>",
        "done": "<emoji id=5260416304224936047>✅</emoji> 백업이 생성되었습니다\n백업 확인 <b>backups chat</b>",
        "restoring": "<emoji id=5370706614800097423>🧐</emoji> <b>데이터베이스 복원...</</b>",
        "invalid": "<emoji id=5413472879771658264>❌</emoji> 잘못된 파일 형식",
        "loaded": "<emoji id=5870888735041655084>📁</emoji> <b>백업이 성공적으로 로드되었습니다</b>",
        "restart": "<b><emoji id=5328274090262275771>🔁</emoji> 재시작...</b>",
        "enabled": "<emoji id=5260416304224936047>✅</emoji> <b>자동 백업 <u>활성화</u></b>",
        "disabled": "<emoji id=5260416304224936047>✅</emoji> <b>자동 백업 <u>비활성화</u></b>",
    }

    @loader.command()
    async def backupdb(self, app: Client, message: types.Message):
        """Create database backup [will be sent in backups chat]"""
        txt = io.BytesIO(json.dumps(self.db).encode("utf-8"))
        txt.name = f"shizu-{datetime.now().strftime('%d-%m-%Y-%H-%M')}.json"
        await app.inline_bot.send_document(
            app.db.get("shizu.chat", "backup"),
            document=txt,
            caption=self.strings("backup").format(
                datetime.now().strftime("%d-%m-%Y %H:%M")
            ),
        )
        await message.answer(self.strings("done"))

    @loader.command()
    async def restoredb(self, app: Client, message: types.Message):
        """Easy restore database"""
        reply = message.reply_to_message
        if not reply or not reply.document:
            return await message.answer(self.strings("invalid"))

        await message.answer(self.strings("restoring"))
        file = await app.download_media(reply.document)
        decoded_text = json.loads(io.open(file, "r", encoding="utf-8").read())

        if not file.endswith(".json"):
            return await message.answer(self.strings("invalid"))

        self.db.reset()

        self.db.update(**decoded_text)

        self.db.save()

        await app.send_message(
            message.chat.id,
            self.strings("loaded"),
        )

        ms = await message.answer(self.strings("restart"))

        self.db.set(
            "shizu.updater",
            "restart",
            {
                "chat": (
                    message.chat.username
                    if message.chat.type == enums.ChatType.BOT
                    else message.chat.id
                ),
                "id": ms.id,
                "start": time.time(),
                "type": "restart",
            },
        )

        utils.restart()
