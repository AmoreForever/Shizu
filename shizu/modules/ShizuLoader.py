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


import re
import requests
import base64
import logging
from typing import List
from pyrogram import Client, types
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

logger = logging.BASIC_FORMAT


async def get_git_raw_link(repo_url: str):
    """Get raw link to repository"""

    match = GIT_REGEX.search(repo_url)
    if not match:
        return False

    repo_path = match.group(1)
    branch = match.group(2)
    path = match.group(3)

    r = await utils.run_sync(requests.get, f"https://api.github.com/repos{repo_path}")
    if r.status_code != 200:
        return False

    branch = branch or r.json()["default_branch"]

    return f"https://raw.githubusercontent.com{repo_path}/{branch}{path or ''}/"


@loader.module(name="ShizuLoader", author="shizu")
class Loader(loader.Module):
    """Module loader"""

    strings = {
        "invalid_repo": "❌ Invalid repository link.\n",
        "no_all": "❌ The all.txt file was not found in the <a href='{}'>repository</a>.\n",
        "mods_in_repo": "<emoji id=5974220038956124904>📥</emoji> <b>List of available modules with <a href='{}'>repository</a></b>:\n\n",
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
        "aelis_enabled": "<emoji id=4908971422589649873>👍</emoji> Enabled, now you can load modules from <a href='https://t.me/aelis_msbot'>Aelis bot</a>",
        "aelis_disabled": "<emoji id=4900283627167810560>👎</emoji> Disabled, now you cannot load nodules from <a href='https://t.me/aelis_msbot'>Aelis bot</a>",
    }

    strings_ru = {
        "invalid_repo": "❌ Недопустимый репозиторий.\n",
        "no_all": "❌ Не найдено all.txt в репозитории <a href='{}'>repository</a>.\n",
        "mods_in_repo": "<emoji id=5974220038956124904>📥</emoji> <b>Список доступных модулей в <a href='{}'>repository</a></b>:\n\n",
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
        "aelis_enabled": "<emoji id=4908971422589649873>👍</emoji> Включено, теперь вы можете загружать модули с <a href='https://t.me/aelis_msbot'>Aelis бота</a>",
        "aelis_disabled": "<emoji id=4900283627167810560>👎</emoji> Отключено, теперь вы не можете загружать модули с <a href='https://t.me/aelis_msbot'>Aelis бота</a>",
    }

    strings_uz = {
        "invalid_repo": "❌ Xatolik yuz berdi.\n",
        "no_all": "❌ All.txt fayl mavjud emas <a href='{}'>repository</a>.\n",
        "mods_in_repo": "<emoji id=5974220038956124904>📥</emoji> <b>Modullar ro'yhati <a href='{}'>repository</a></b>:\n\n",
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
        "aelis_enabled": "<emoji id=4908971422589649873>👍</emoji> Endi siz modullarni botdan yuklashingiz mumkun <a href='https://t.me/aelis_msbot'>Bot</a>",
        "aelis_disabled": "<emoji id=4900283627167810560>👎</emoji> Endi siz modullarni botdan yuklay olmaysiz <a href='https://t.me/aelis_msbot'>Bot</a>",
    }

    strings_jp = {
        "invalid_repo": "❌ 無効なリポジトリ.\n",
        "no_all": "❌ all.txtファイルが<a href='{}'>repository</a>に見つかりませんでした.\n",
        "mods_in_repo": "<emoji id=5974220038956124904>📥</emoji> <b>リポジトリの利用可能なモジュールのリスト <a href='{}'>repository</a></b>:\n\n",
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
        "aelis_enabled": "<emoji id=4908971422589649873>👍</emoji> 有効になりました。これで<a href='https://t.me/aelis_msbot'>Aelis bot</a>からモジュールをロードできます",
        "aelis_disabled": "<emoji id=4900283627167810560>👎</emoji> 無効になりました。これで<a href='https://t.me/aelis_msbot'>Aelis bot</a>からモジュールをロードできなくなります",
    }

    @loader.command()
    async def dlmod(self, app: Client, message: types.Message, args: str):
        """Download module by link. Usage: dlmod <link or all or nothing>"""

        bot_username = (await self.bot.bot.get_me()).username
        dop_help = "<emoji id=5100652175172830068>▫️</emoji>"
        modules_repo = self.db.get(
            "shizu.loader", "repo", "https://github.com/AmoreForever/ShizuMods"
        )

        api_result = await get_git_raw_link(modules_repo)
        if not api_result:
            return await message.answer(self.strings("invalid_repo"))
        raw_link = api_result
        modules = await utils.run_sync(requests.get, f"{raw_link}all.txt")
        if modules.status_code != 200:
            return await message.answer(
                self.strings("no_all").format(raw_link), disable_web_page_preview=True
            )

        modules: List[str] = modules.text.splitlines()

        if not args:
            text = self.strings("mods_in_repo").format(modules_repo) + "\n".join(
                map("<code>{}</code>".format, modules)
            )
            return await message.answer(text, disable_web_page_preview=True)

        error_text: str = None
        module_name: str = None

        if args in modules:
            args = raw_link + args + ".py"

        try:
            r = await utils.run_sync(requests.get, args)
            if r.status_code != 200:
                raise requests.exceptions.ConnectionError

            await message.answer(self.strings("check"))
            module_name = await self.all_modules.load_module(r.text, r.url)
            if module_name == "DAR":
                error_text = self.strings("found_delete_")
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

        self.db.set(
            "shizu.loader",
            "modules",
            list(set(self.db.get("shizu.loader", "modules", []) + [args])),
        )

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
    async def set_dl_repo(self, app: Client, message: types.Message):
        """Set the repository for downloading modules. Usage: set_dl_repo <link>"""
        self.db.set("shizu.loader", "repo", message.get_args_raw())
        return await message.answer(self.strings("repo_set"))

    @loader.command()
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
            return await message.answer(self.strings("core_unload"))

        return await message.answer(self.strings("unloaded").format(module_name))

    @loader.command()
    async def aelis_load(self, app: Client, message: types.Message, args: str):
        """Enable or disable loading from Aelis bot [on/off]"""
        if not args:
            return await message.answer(self.strings("spec_action"))
        if "on" in args:
            self.db.set("shizu.loader", "aelis", True)
            await message.answer(self.strings("aelis_enabled"))
        if "off" in args:
            self.db.set("shizu.loader", "aelis", False)
            await message.answer(self.strings("aelis_disabled"))

    @loader.on(lambda _, __, m: m and m.chat.id == 6417188473)
    async def watcher(self, app: Client, message: types.Message):
        if self.db.get("shizu.loader", "aelis") == False:
            return
        try:
            if not message.text.startswith("#"):
                return
            load_string = base64.b64decode(message.text.split("\n")[0]).decode("utf-8")
            await message.delete()
            r = await utils.run_sync(requests.get, load_string)

            if r.status_code == 200:
                module_name = await self.all_modules.load_module(r.text, r.url)
                if module_name is True:
                    return await message.answer(self.strings("dep_installed_req_res"))

                if not module_name:
                    return await message.answer(self.strings("not_module"))

                if module_name == "DAR":
                    return await message.answer(self.strings("found_delete_"))

                module = self.all_modules.get_module(module_name, True)
                self.db.set(
                    "shizu.loader",
                    "modules",
                    list(
                        set(self.db.get("shizu.loader", "modules", []) + [load_string])
                    ),
                )
                return await message.answer(f"#loaded:{module.name}:{message.id -1}")
        except AttributeError:
            logging.info("I see a message without text heh, just ignore this message")
