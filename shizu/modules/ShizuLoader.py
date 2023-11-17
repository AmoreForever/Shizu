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


import atexit
import logging
import os
import re
import sys
import time
from typing import List

import requests
from pyrogram import Client, enums, types

from .. import loader, utils

VALID_URL = r"[-[\]_.~:/?#@!$&'()*+,;%<=>a-zA-Z0-9]+"

VALID_PIP_PACKAGES = re.compile(
    r"^\s*# required:(?: ?)((?:{url} )*(?:{url}))\s*$".format(url=VALID_URL),
    re.MULTILINE,
)
GIT_REGEX = re.compile(
    r"^https?://github\.com((?:/[a-z0-9-]+){2})(?:/tree/([a-z0-9-]+)((?:/[a-z0-9-]+)*))?/?$",
    flags=re.IGNORECASE,
)

logger = logging.getLogger(__name__)


@loader.module(name="ShizuLoader", author="shizu")
class Loader(loader.Module):
    """Mainly used to load modules"""

    strings = {
        "invalid_repo": "❌ Invalid repository link.\n",
        "no_all": "❌ The all.txt file was not found in the <a href='{}'>repository</a>.\n",
        "mods_in_repo": "{} <b>List of available modules in <a href='{}'>repository</a></b>:\n\n",
        "check": "<emoji id=5280506417478903827>🛡</emoji> Analyzing the module..",
        "found_delete_": "<emoji id=5203929938024999176>🛡</emoji> <b><u>Shizu</u> protected your account from</b> <code>DeleteAccount</code>.\n<emoji id=5404380425416090434>ℹ️</emoji> <b>This module contains a dangerous code that can delete your account.</b>",
        "dep_installed_req_res": "✅ Dependencies are installed. Reboot required",
        "not_module": "❌ Failed to load the module. See the logs for details",
        "inc_link": "❌ The link is incorrect",
        "not_aw_by_link": "❌ The module is not available by the link",
        "unex_error": "❌ An unexpected error has occurred. See the logs for details",
        "loaded": (
            "<emoji id=5267468588985363056>✔️</emoji> Module <b>{}</b> loaded\n"
            "<emoji id=5787544344906959608>ℹ️</emoji>  {} \n\n"
        ),
        "repo_set": "✅ Repository has been set",
        "no_repy_to_file": "❌ No reply to file",
        "loading": "<emoji id=5215493819641895305>🚛</emoji> <b>Loading the module..</b>",
        "core_do": "❌ It is not allowed to load core modules",
        "inc_module_name": "❌ Incorrect module name",
        "core_unload": "<emoji id=5364241851500997604>⚠️</emoji> You cannot unload the core modules",
        "unloaded": "<emoji id=6334471265700546607>🧹</emoji> Module <code>{}</code> unloaded",
        "spec_action": "<emoji id=5188420746694633417>🌗</emoji> <b>Specify the action</b>",
        "not_for_this_account": "<emoji id=5352726898151534058>😢</emoji> <b>This module is not available for this account</b>",
        "all_unloaded": "<emoji id=6334471265700546607>🧹</emoji> All modules unloaded",
        "restart": "<b><emoji id=5328274090262275771>🔁</emoji> Restarting...</b>",
        "only_telethon": "<b><emoji id=5818764548080930127>⛰</emoji>You have not enabled Telethon mode, thus it is not possible to use this module</b>",
        "specify_to_block": "🫦 <b>Specify the module to ban. (reply or link)</b>",
        "module_banned": "<emoji id=5258011861273551368>🌘</emoji> <b>Module <code>{}</code> banned the next time you cannot load it</b>",
        "loaded_banned": "<emoji id=5418159410646099061>🚫</emoji> <b>Hey, hey, hey, you have banned this module, you cannot load it</b>",
        "no_banned": "<emoji id=5839434146912407382>🚫</emoji> <b>There are no banned modules</b>",
        "banned_list": "<emoji id=5780471598922337683>🌍</emoji> <b>Heres a list of banned modules:</b>\n\n {}",
        "specify_to_unblock": "🫦 <b>Specify the module to unblock.</b>",
        "unblocked": "<emoji id=5418159410646099061>🚫</emoji> <b>Module <code>{}</code> unblocked</b>",
    }

    strings_ru = {
        "invalid_repo": "❌ Недопустимый репозиторий.\n",
        "no_all": "❌ Не найдено all.txt в репозитории <a href='{}'>repository</a>.\n",
        "mods_in_repo": "{} <b>Список доступных модулей в <a href='{}'>repository</a></b>:\n\n",
        "check": "<emoji id=5280506417478903827>🛡</emoji> Проверка модуля..",
        "found_delete_": "<emoji id=5203929938024999176>🛡</emoji> <b><u>Shizu</u> защитил ваш аккаунт от</b> <code>DeleteAccount</code>.\n<emoji id=5404380425416090434>ℹ️</emoji> <b>Этот модуль содержит опасный код, который может удалить ваш аккаунт.</b>",
        "dep_installed_req_res": "✅ Зависимости установлены. Перезагрузка требуется",
        "not_module": "❌ Не удалось загрузить модуль. Проверьте логи",
        "inc_link": "❌ Ссылка некорректна",
        "not_aw_by_link": "❌ Модуль недоступен по ссылке",
        "unex_error": "❌ Ошибка. Проверьте логи",
        "loaded": (
            "<emoji id=5267468588985363056>✔️</emoji> Модуль <b>{}</b> загружен\n"
            "<emoji id=5787544344906959608>ℹ️</emoji> {} \n\n"
        ),
        "repo_set": "✅ Репозиторий установлен",
        "no_repy_to_file": "❌ Нет ответа на файл",
        "loading": "<emoji id=5215493819641895305>🚛</emoji> <b>Загрузка модуля..</b>",
        "core_do": "❌ Нельзя загружать встроенные модули",
        "inc_module_name": "❌ Неверное имя модуля",
        "core_unload": "<emoji id=5364241851500997604>⚠️</emoji> Вы не можете удалить встроенные модули ",
        "unloaded": "<emoji id=6334471265700546607>🧹</emoji> Модуль <code>{}</code> выгружен",
        "spec_action": "<emoji id=5188420746694633417>🌗</emoji> <b>Укажите действие</b>",
        "not_for_this_account": "<emoji id=5352726898151534058>😢</emoji> <b>Этот модуль недоступен для этого аккаунта</b>",
        "all_unloaded": "<emoji id=6334471265700546607>🧹</emoji> Все модули выгружены",
        "restart": "<b><emoji id=5328274090262275771>🔁</emoji> Перезапуск...</b>",
        "only_telethon": "<b><emoji id=5818764548080930127>⛰</emoji>Вы не включили Телетон мод, поэтому он недоступен</b>",
        "specify_to_block": "🫦 <b>Укажите модуль для блокировки. (ответ или ссылка)</b>",
        "module_banned": "<emoji id=5258011861273551368>🌘</emoji> <b>Модуль <code>{}</code> заблокирован, в следующий раз вы не сможете его загрузить</b>",
        "loaded_banned": "<emoji id=5418159410646099061>🚫</emoji> <b>Эй, эй, эй, вы заблокировали этот модуль, вы не можете его загрузить</b>",
        "no_banned": "<emoji id=5839434146912407382>🚫</emoji> <b>Заблокированных модулей нет</b>",
        "banned_list": "<emoji id=5780471598922337683>🌍</emoji> <b>Вот список заблокированных модулей:</b>\n\n {}",
        "specify_to_unblock": "🫦 <b>Укажите модуль для разблокировки.</b>",
        "unblocked": "<emoji id=5418159410646099061>🚫</emoji> <b>Модуль <code>{}</code> разблокирован</b>",
    }

    strings_uz = {
        "invalid_repo": "❌ Xatolik yuz berdi.\n",
        "no_all": "❌ All.txt fayl mavjud emas <a href='{}'>repository</a>.\n",
        "mods_in_repo": "{} <b>Modullar ro'yhati <a href='{}'>repository</a></b>:\n\n",
        "check": "<emoji id=5280506417478903827>🛡</emoji> Modul tekshirilmoqda..",
        "found_delete_": "<emoji id=5203929938024999176>🛡</emoji> <b><u>Shizu</u> DeleteAccount dan hisobingizni himoya qildi</b> <code>DeleteAccount</code>.\n<emoji id=5404380425416090434>ℹ️</emoji> <b>Bu modul hisobingizni o'chirishi mumkin bo'lgan xavfsizlik kodi bor.</b>",
        "dep_installed_req_res": "✅ Zarrashilmoqda. Userbotni qayta yuklash kerak",
        "not_module": "❌ Modul yuklanmadi. Loglaridan foydalaning",
        "inc_link": "❌ Link xato",
        "not_aw_by_link": "❌ Modul mavjud emas",
        "unex_error": "❌ Xatolik. Loglaridan foydalaning",
        "loaded": (
            "<emoji id=5267468588985363056>✔️</emoji> Modul <b>{}</b> yuklandi\n"
            "<emoji id=5787544344906959608>ℹ️</emoji> {} \n\n"
        ),
        "repo_set": "✅ Repository yuklandi",
        "no_repy_to_file": "❌ Faylni reply qiliing",
        "loading": "<emoji id=5215493819641895305>🚛</emoji> <b>Modul yuklanmoqda..</b>",
        "core_do": "❌ Userbotni modullarini yuklash mumkun emas",
        "inc_module_name": "❌ Module nomi xato",
        "core_unload": "<emoji id=5364241851500997604>⚠️</emoji> Bu modulni userbotdan yuklanmaydi",
        "unloaded": "<emoji id=6334471265700546607>🧹</emoji> Modul <code>{}</code> ochirildi",
        "spec_action": "<emoji id=5188420746694633417>🌗</emoji> <b>Nma qilishim kerak?</b>",
        "not_for_this_account": "<emoji id=5352726898151534058>😢</emoji> <b>Bu modul ushbu akkaunt uchun mavjud emas</b>",
        "all_unloaded": "<emoji id=6334471265700546607>🧹</emoji> Barcha modullar ochirildi",
        "restart": "<b><emoji id=5328274090262275771>🔁</emoji> Qayta ishlayapti...</b>",
        "only_telethon": "<b><emoji id=5818764548080930127>⛰</emoji>Telethon mod ishlatilmadi shuning uchun modul zagruzka bolmadi</b>",
        "specify_to_block": "🫦 <b>Blocklash uchun modulni ko'rsating. (reply yoki link)</b>",
        "module_banned": "<emoji id=5258011861273551368>🌘</emoji> <b>Modul <code>{}</code> bloklandi, keyinroq uni yuklab bo'lmaydi</b>",
        "loaded_banned": "<emoji id=5418159410646099061>🚫</emoji> <b>Hey, hey, hey, siz bu modulni blokladingiz, uni yuklab bo'lmaydi</b>",
        "no_banned": "<emoji id=5839434146912407382>🚫</emoji> <b>Bloklangan modullar yo'q</b>",
        "banned_list": "<emoji id=5780471598922337683>🌍</emoji> <b>Bloklangan modullar ro'yhati:</b>\n\n {}",
        "specify_to_unblock": "🫦 <b>Unblocklash uchun modulni ko'rsating.</b>",
        "unblocked": "<emoji id=5418159410646099061>🚫</emoji> <b>Modul <code>{}</code> unblocklandi</b>",
    }

    strings_jp = {
        "invalid_repo": "❌ 無効なリポジトリ.\n",
        "no_all": "❌ all.txtファイルが<a href='{}'>repository</a>に見つかりませんでした.\n",
        "mods_in_repo": "{} <b>リポジトリの利用可能なモジュールのリスト <a href='{}'>repository</a></b>:\n\n",
        "check": "<emoji id=5280506417478903827>🛡</emoji> モジュールをチェックしています..",
        "found_delete_": "<emoji id=5203929938024999176>🛡</emoji> <b><u>Shizu</u> あなたのアカウントを保護しました</b> <code>DeleteAccount</code>.\n<emoji id=5404380425416090434>ℹ️</emoji> <b>このモジュールには、アカウントを削除する可能性のある危険なコードが含まれています。</b>",
        "dep_installed_req_res": "✅ 依存関係がインストールされました。再起動が必要です",
        "not_module": "❌ モジュールをロードできませんでした。詳細についてはログを参照してください",
        "inc_link": "❌ リンクが無効です",
        "not_aw_by_link": "❌ モジュールはリンクで利用できません",
        "unex_error": "❌ 予期しないエラーが発生しました。詳細についてはログを参照してください",
        "loaded": (
            "<emoji id=5267468588985363056>✔️</emoji> モジュール <b>{}</b> ロードされました\n"
            "<emoji id=5787544344906959608>ℹ️</emoji>  {} \n\n"
        ),
        "repo_set": "✅ リポジトリが設定されました",
        "no_repy_to_file": "❌ ファイルに返信しない",
        "loading": "<emoji id=5215493819641895305>🚛</emoji> <b>モジュールをロードしています..</b>",
        "core_do": "❌ コアモジュールをロードすることは許可されていません",
        "inc_module_name": "❌ モジュール名が無効です",
        "core_unload": "<emoji id=5364241851500997604>⚠️</emoji> コアモジュールをアンロードすることはできません",
        "unloaded": "<emoji id=6334471265700546607>🧹</emoji> モジュール <code>{}</code> アンロードされました",
        "spec_action": "<emoji id=5188420746694633417>🌗</emoji> <b>アクションを指定してください</b>",
        "not_for_this_account": "<emoji id=5352726898151534058>😢</emoji> <b>このアカウントではこのモジュールは利用できません</b>",
        "all_unloaded": "<emoji id=6334471265700546607>🧹</emoji> すべてのモジュールがアンロードされました",
        "restart": "<b><emoji id=5328274090262275771>🔁</emoji> 再起動しています...</b>",
        "only_telethon": "<b><emoji id=5818764548080930127>⛰</emoji>テレソンモードが有効になっていないため、このモジュールを使用することはできません</b>",
        "specify_to_block": "🫦 <b>ブロックするモジュールを指定してください。 (返信またはリンク)</b>",
        "module_banned": "<emoji id=5258011861273551368>🌘</emoji> <b>モジュール <code>{}</code> 次回はロードできません</b>",
        "loaded_banned": "<emoji id=5418159410646099061>🚫</emoji> <b>ヘイ、ヘイ、ヘイ、このモジュールをブロックしました、ロードすることはできません</b>",
        "no_banned": "<emoji id=5839434146912407382>🚫</emoji> <b>ブロックされたモジュールはありません</b>",
        "banned_list": "<emoji id=5780471598922337683>🌍</emoji> <b>ブロックされたモジュールのリストです:</b>\n\n {}",
        "specify_to_unblock": "🫦 <b>ブロック解除するモジュールを指定してください。</b>",
        "unblocked": "<emoji id=5418159410646099061>🚫</emoji> <b>モジュール <code>{}</code> ブロック解除されました</b>",
    }

    strings_ua = {
        "invalid_repo": "❌ Невірний репозиторій.\n",
        "no_all": "❌ all.txt файл не знайдено в репозиторії <a href='{}'>repository</a>.\n",
        "mods_in_repo": "{} <b>Модулі репозиторію <a href='{}'>repository</a></b>:\n\n",
        "check": "<emoji id=5280506417478903827>🛡</emoji> Аналіз модуля..",
        "loaded": "<emoji id=5267468588985363056>✔️</emoji> Модуль <b>{}</b> завантажено\n"
        "<emoji id=5787544344906959608>ℹ️</emoji> {} \n\n",
        "repo_set": "✅ Репозиторій установлено",
        "unloaded": "<emoji id=6334471265700546607>🧹</emoji> Модуль <code>{}</code> вилучено",
        "spec_action": "<emoji id=5188420746694633417>🌗</emoji> <b>Акцію вказано</b>",
        "no_repy_to_file": "❌ Не надіслати повідомлення",
        "loading": "<emoji id=5215493819641895305>🚛</emoji> <b>Модуль завантажується..</b>",
        "not_for_this_account": "<emoji id=5352726898151534058>😢</emoji> <b>Цей модуль недоступний для цього облікового запису</b>",
        "all_unloaded": "<emoji id=6334471265700546607>🧹</emoji> Всі модулі вилучено",
        "restart": "<b><emoji id=5328274090262275771>🔁</emoji> Перезавантаження...</b>",
        "only_telethon": "<b><emoji id=5818764548080930127>⛰</emoji>Ви не включили Телетон мод, тому він недоступний</b>",
        "specify_to_block": "🫦 <b>Вкажіть модуль для блокування. (відповідь або посилання)</b>",
        "module_banned": "<emoji id=5258011861273551368>🌘</emoji> <b>Модуль <code>{}</code> заблоковано, наступного разу ви не зможете його завантажити</b>",
        "loaded_banned": "<emoji id=5418159410646099061>🚫</emoji> <b>Ей, ей, ей, ви заблокували цей модуль, ви не можете його завантажити</b>",
        "no_banned": "<emoji id=5839434146912407382>🚫</emoji> <b>Заблокованих модулів немає</b>",
        "banned_list": "<emoji id=5780471598922337683>🌍</emoji> <b>Ось список заблокованих модулів:</b>\n\n {}",
        "specify_to_unblock": "🫦 <b>Вкажіть модуль для розблокування.</b>",
        "unblocked": "<emoji id=5418159410646099061>🚫</emoji> <b>Модуль <code>{}</code> розблоковано</b>",
    }

    strings_kz = {
        "invalid_repo": "❌ Репозиторий жарамсыз.\n",
        "no_all": "❌ all.txt файлын табылмады <a href='{}'>repository</a>.\n",
        "mods_in_repo": "{} <b>Модульдер репозиториясы <a href='{}'>repository</a></b>:\n\n",
        "check": "<emoji id=5280506417478903827>🛡</emoji> Модульді тексеру..",
        "loaded": "<emoji id=5267468588985363056>✔️</emoji> Модуль <b>{}</b> жүктелді\n"
        "<emoji id=5787544344906959608>ℹ️</emoji> {} \n\n",
        "repo_set": "✅ Репозиторий орнатылды",
        "unloaded": "<emoji id=6334471265700546607>🧹</emoji> Модуль <code>{}</code> жойылды",
        "spec_action": "<emoji id=5188420746694633417>🌗</emoji> <b>Әрекетті көрсетіңіз</b>",
        "no_repy_to_file": "❌ Файлға жауап бермеу",
        "loading": "<emoji id=5215493819641895305>🚛</emoji> <b>Модуль жүктелуде..</b>",
        "not_for_this_account": "<emoji id=5352726898151534058>😢</emoji> <b>Бұл модуль бұл аккаунтқа қолжетімді емес</b>",
        "all_unloaded": "<emoji id=6334471265700546607>🧹</emoji> Барлық модульдер жойылды",
        "restart": "<b><emoji id=5328274090262275771>🔁</emoji> Қайта іске қосу...</b>",
        "only_telethon": "<b><emoji id=5818764548080930127>⛰</emoji>Телетон модты қоспағансыз сондықтан ол қолжетімді емес</b>",
        "specify_to_block": "🫦 <b>Блоктау үшін модульді көрсетіңіз. (жауап немесе сілтеме)</b>",
        "module_banned": "<emoji id=5258011861273551368>🌘</emoji> <b>Модуль <code>{}</code> блокталды, келесі рет оны жүкте алмайсыз</b>",
        "loaded_banned": "<emoji id=5418159410646099061>🚫</emoji> <b>Эй, эй, эй, сіз осы модульді блоктадыңыз, оны жүкте алмайсыз</b>",
        "no_banned": "<emoji id=5839434146912407382>🚫</emoji> <b>Блокталған модульдер жоқ</b>",
        "banned_list": "<emoji id=5780471598922337683>🌍</emoji> <b>Блокталған модульдер тізімі:</b>\n\n {}",
        "specify_to_unblock": "🫦 <b>Блоктауды бұзу үшін модульді көрсетіңіз.</b>",
        "unblocked": "<emoji id=5418159410646099061>🚫</emoji> <b>Модуль <code>{}</code> блоктауды бұзылды</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "repo",
            "https://github.com/AmoreForever/ShizuMods",
            "Repository link",
            "private_repo",
            None,
            "Private repository link",
            "private_token",
            None,
            "Private repository token",
        )

    @loader.command(aliases=['dlm'])
    async def dlmod(self, app: Client, message: types.Message, args: str):
        """Download module by link. Usage: dlmod <link or all or nothing>"""

        bot_username = (await self.bot.bot.get_me()).username
        dop_help = "<emoji id=5100652175172830068>▫️</emoji>"
        modules_repo = self.config["repo"]
        private = self.config["private_repo"], self.config["private_token"]

        api_result = await self.get_git_raw_link(modules_repo)
        
        if not api_result:
            return await message.answer(self.strings("invalid_repo"))

        raw_link = api_result

        modules = await utils.run_sync(requests.get, f"{raw_link}all.txt")

        if modules.status_code != 200:
            return await message.answer(
                self.strings("no_all").format(raw_link), disable_web_page_preview=True
            )

        modules: List[str] = modules.text.splitlines()

        if self.config["private_repo"] and self.config["private_token"]:
            api_resultP = await self.get_git_raw_link(private[0], private[1])

            if not api_resultP:
                return await message.answer(self.strings("invalid_repo"))

            headers = {"Authorization": f"token {private[1]}"}

            modulesP = await utils.run_sync(
                requests.get, f"{api_resultP}all.txt", headers=headers
            )

            if modulesP.status_code != 200:
                return await message.answer(
                    self.strings("no_all").format(api_resultP),
                    disable_web_page_preview=True,
                )

            modulesP: List[str] = modulesP.text.splitlines()

        if not args:
            text = self.strings("mods_in_repo").format("🎍", modules_repo) + "\n".join(
                map("• <code>{}</code>".format, modules)
            )

            if self.config["private_repo"] and self.config["private_token"]:
                textP = self.strings("mods_in_repo").format(
                    "🫦", private[0]
                ) + "\n".join(map("• <code>{}</code>".format, modulesP))

                return await self.bot.list(
                    message,
                    [text, textP],
                    disable_web_page_preview=True,
                )

            return await message.answer(text, disable_web_page_preview=True)

        error_text: str = None
        module_name: str = None
        is_private = False

        if args in modules:
            args = raw_link + args + ".py"
            r = await utils.run_sync(requests.get, args)
            if r.status_code != 200:
                raise requests.exceptions.ConnectionError

            await message.answer(self.strings("check"))

            module_name = await self.all_modules.load_module(r.text, r.url)

        if self.config["private_repo"] and self.config["private_token"] and args in modulesP:
            args = api_resultP + args + ".py"
        
            headers = {"Authorization": f"token {private[1]}"}
        
            r = await utils.run_sync(requests.get, args, headers=headers)
        
            if r.status_code != 200:
                raise requests.exceptions.ConnectionError
        
            await message.answer(self.strings("check"))
        
            module_name = await self.all_modules.load_module(r.text, "<string>")
            is_private = True

        try:
            if module_name == "DAR":
                error_text = self.strings("found_delete_")
            if module_name == "NFA":
                error_text = self.strings("not_for_this_account")
            if module_name is True:
                error_text = self.strings("dep_installed_req_res")
            if not module_name:
                error_text = self.strings("not_module")

        except requests.exceptions.MissingSchema:
            error_text = self.strings("inc_link")
        except requests.exceptions.ConnectionError:
            error_text = self.strings("inc_link")
        except requests.exceptions.RequestException:
            error_text = self.strings("unex_error")

        if error_text:
            return await message.answer(error_text)

        if args in modules:
            self.db.set(
                "shizu.loader",
                "modules",
                list(set(self.db.get("shizu.loader", "modules", []) + [args])),
            )

        if is_private:
            with open(
                f"./shizu/modules/{module_name}.py", "w", encoding="utf-8"
            ) as file:
                file.write(r.text)

        if not (module := self.all_modules.get_module(module_name, True)):
            return await message.answer(
                "<b><emoji id=5465665476971471368>❌</emoji> There is no such module</b>",
            )

        prefix = self.db.get("shizu.loader", "prefixes", ["."])[0]
        command_descriptions = "\n".join(
            f"{dop_help} <code>{prefix + command}</code> - {module.command_handlers[command].__doc__ or 'No description'}"
            for command in module.command_handlers
        )
        inline_descriptions = "\n".join(
            f"{dop_help} <code>@{bot_username} {command}</code> - {module.inline_handlers[command].__doc__ or 'No description'}"
            for command in module.inline_handlers
        )
        modname = str(module.name).capitalize()

        header = self.strings("loaded").format(
            modname, module.__doc__ or "No description"
        )
        footer = (
            f"<emoji id=5190458330719461749>🧑‍💻</emoji> <code>{module.author}</code>"
            if module.author
            else ""
        )
        return await message.answer(
            header + command_descriptions + "\n" + inline_descriptions + "\n" + footer,
        )

    async def get_git_raw_link(self, repo_url: str, token: str = None):
        
        match = GIT_REGEX.search(repo_url)
        if not match:
            return False

        repo_path, branch, path = match.group(1), match.group(2), match.group(3)

        if token:
            headers = {"Authorization": f"token {token}"}
            r = await utils.run_sync(
                requests.get,
                f"https://api.github.com/repos{repo_path}",
                headers=headers,
            )
        else:
            r = await utils.run_sync(
                requests.get, f"https://api.github.com/repos{repo_path}"
            )

        if r.status_code != 200:
            return False

        branch = branch or r.json().get("default_branch", "")

        return f"https://raw.githubusercontent.com{repo_path}/{branch}{path or ''}/"

    @loader.command(aliases=["lm"])
    async def loadmod(self, app: Client, message: types.Message):
        """Load the module by file. Usage: <replay per file>"""
        reply = message.reply_to_message
        bot_username = (await self.bot.bot.get_me()).username
        dop_help = (
            "<emoji id=5100652175172830068>🔸</emoji>"
            if message.from_user.is_premium
            else "🔸"
        )

        file = (
            message if message.document else reply if reply and reply.document else None
        )

        if not file:
            return await message.answer(self.strings("no_repy_to_file"))

        await message.answer(self.strings("loading"))
        file = await reply.download()

        for mod in self.cmodules:
            if file == mod:
                return await message.answer(self.strings("core_do"))

        try:
            with open(file, "r", encoding="utf-8") as file:
                module_source = file.read()

        except UnicodeDecodeError:
            return await message.answer("❌ Incorrect file encoding")
        await message.answer(self.strings("check"))

        module_name = await self.all_modules.load_module(module_source)
        if module_name is True:
            return await message.answer(self.strings("dep_installed_req_res"))

        if not module_name:
            return await message.answer(self.strings("not_module"))

        if module_name == "DAR":
            return await message.answer(self.strings("found_delete_"))

        if module_name == "NFA":
            return await message.answer(self.strings("not_for_this_account"))

        if module_name == "OTL":
            return await message.answer(self.strings("only_telethon"))

        if module_name == "BAN":
            return await message.answer(self.strings("loaded_banned"))

        module = "_".join(module_name.lower().split())
        with open(f"shizu/modules/{module}.py", "w", encoding="utf-8") as file:
            file.write(module_source)

        if not (module := self.all_modules.get_module(module_name, True)):
            return await message.answer(
                "<b><emoji id=5465665476971471368>❌</emoji> There is no such module</b>",
            )

        prefix = self.db.get("shizu.loader", "prefixes", ["."])[0]
        command_descriptions = "\n".join(
            f"{dop_help} <code>{prefix + command}</code> - {module.command_handlers[command].__doc__ or 'No description'}"
            for command in module.command_handlers
        )
        inline_descriptions = "\n".join(
            f"{dop_help} <code>@{bot_username} {command}</code> - {module.inline_handlers[command].__doc__ or 'No description'}"
            for command in module.inline_handlers
        )
        modname = str(module.name).capitalize()

        header = self.strings("loaded").format(
            modname, module.__doc__ or "No description"
        )
        footer = (
            f"<emoji id=5190458330719461749>🧑‍💻</emoji> <code>{module.author}</code>"
            if module.author
            else ""
        )
        return await message.answer(
            header + command_descriptions + "\n" + inline_descriptions + "\n" + footer,
        )

    @loader.command()
    async def unloadmod(self, app: Client, message: types.Message, args: str):
        """Unload the module. Usage: unloadmod <module name>"""

        if not (module_name := self.all_modules.unload_module(args)):
            return await message.answer(self.strings("inc_module_name"))

        if module_name in self.cmodules:
            logging.error("You can't unload core modules")
            return await message.answer(self.strings("core_unload"))

        return await message.answer(self.strings("unloaded").format(module_name))

    @loader.command()
    async def unloadall(self, app: Client, message: types.Message):
        """Unload all modules"""

        self._local_modules_path: str = "./shizu/modules"

        self.db.set("shizu.loader", "modules", [])

        for local_module in filter(
            lambda file_name: file_name.endswith(".py")
            and not file_name.startswith("Shizu"),
            os.listdir(self._local_modules_path),
        ):
            os.remove(f"{self._local_modules_path}/{local_module}")

        await message.answer(self.strings("all_unloaded"))
        ms = await message.answer(self.strings("restart"))

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

        atexit.register(os.execl(sys.executable, sys.executable, "-m", "shizu"))
        return sys.exit(0)

    @loader.command()
    async def banmodslist(self, app: Client, message: types.Message):
        """Show banned modules list"""

        modules = self.db.get("shizu.loader", "banned", [])

        if not modules:
            return await message.answer(self.strings("no_banned"))

        text = self.strings("banned_list").format(
            "\n".join(map("• <code>{}</code>".format, modules))
        )

        return await message.answer(text)

    @loader.command()
    async def blockmodule(self, app: Client, message: types.Message):
        """It will block the module the next time u cannot load it"""

        reply = message.reply_to_message
        args = message.get_args_raw()

        if not reply and not args:
            return await message.answer(self.strings("spec_action"))

        if reply:
            file = (
                message
                if message.document
                else reply
                if reply and reply.document
                else None
            )

            source = await reply.download()

            with open(source, "r", encoding="utf-8") as file:
                module_source = file.read()

            module_name = await self.all_modules.load_module(
                module_source, only_ban=True
            )

            if not module_name:
                return await message.answer(self.strings("not_module"))

            await message.answer(self.strings("module_banned").format(module_name))

        if args:
            r = await utils.run_sync(requests.get, args)

            if r.status_code != 200:
                raise requests.exceptions.ConnectionError

            module_name = await self.all_modules.load_module(
                r.text, r.url, only_ban=True
            )

            if not module_name:
                return await message.answer(self.strings("not_module"))

            await message.answer(self.strings("module_banned").format(module_name))

    @loader.command()
    async def unblockmodule(self, app: Client, message: types.Message):
        """Unblock the module"""

        args = message.get_args_raw()

        if not args:
            return await message.answer(self.strings("specify_to_unblock"))

        if args in self.db.get("shizu.loader", "banned", []):
            self.db.set(
                "shizu.loader",
                "banned",
                list(set(self.db.get("shizu.loader", "banned", [])) - {args}),
            )
            return await message.answer(self.strings("unblocked").format(args))
