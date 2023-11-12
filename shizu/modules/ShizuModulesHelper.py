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


import io
import os
import requests
import inspect

from aiogram.types import CallbackQuery
from pyrogram import Client, types, emoji

from .. import loader, utils


@loader.module("ShizuModulesHelper", "hikamoru")
class ModulesLinkMod(loader.Module):
    """Link or file of the installed module"""

    strings = {
        "what_": "<emoji id=5190748314026385859>🤷‍♂️</emoji> No arguments are specified (module name or command)",
        "search_": "<emoji id=5188311512791393083>🔎</emoji> <b>Module search...</b>",
        "nope_": "<emoji id=5346063050233360577>😮</emoji> <b>Couldn't find the module</b>",
        "module_": (
            "🪭 <b><a href='{}'>{}</a></b>\n"
            "ℹ️ <i>{}</i>\n\n"
            "▫️ <b>Commands</b>: {}\n\n"
            "⛩ <b>Download link:</b> <code>{}</code>"
        ),
        "success": "✅ Installed",
        "install": "🌘 Install",
        "restart": "🔄 Restart required",
        "error": "🚫 Error",
        "source": "📁 Source",
    }

    strings_ru = {
        "what_": "<emoji id=5190748314026385859>🤷‍♂️</emoji> Нет аргументов (имя модуля или команда)",
        "search_": "<emoji id=5188311512791393083>🔎</emoji> <b>Поиск модуля...</b>",
        "nope_": "<emoji id=5346063050233360577>😮</emoji> <b>Не удалось найти модуль</b>",
        "module_": (
            "🪭 <b><a href='{}'>{}</a></b>\n"
            "ℹ️ <i>{}</i>\n\n"
            "▫️ <b>Команды</b>: {}\n\n"
            "⛩ <b>Ссылка на скачивание:</b> <code>{}</code>"
        ),
        "success": "✅ Установлен",
        "install": "🌘 Установить",
        "restart": "🔄 Требуется перезагрузка",
        "error": "🚫 Ошибка",
        "source": "📁 Исходный код",
    }

    strings_uz = {
        "what_": "<emoji id=5190748314026385859>🤷‍♂️</emoji> Yozuv mavjud emas",
        "search_": "<emoji id=5188311512791393083>🔎</emoji> <b>Qidiruv...</b>",
        "nope_": "<emoji id=5346063050233360577>😮</emoji> <b>Qidiruv topilmadi</b>",
        "module_": (
            "🪭 <b><a href='{}'>{}</a></b>\n"
            "ℹ️ <i>{}</i>\n\n"
            "▫️ <b>Buyruqlar</b>: {}\n\n"
            "⛩ <b>Yuklab olish linki:</b> <code>{}</code>"
        ),
        "success": "✅ O'rnatildi",
        "install": "🌘 O'rnatish",
        "restart": "🔄 Qayta yuklash talab qilinadi",
        "error": "🚫 Xato",
        "source": "📁 Manba",
    }

    strings_jp = {
        "what_": "<emoji id=5190748314026385859>🤷‍♂️</emoji> 引数がありません（モジュール名またはコマンド）",
        "search_": "<emoji id=5188311512791393083>🔎</emoji> <b>モジュール検索...</b>",
        "nope_": "<emoji id=5346063050233360577>😮</emoji> <b>モジュールが見つかりませんでした</b>",
        "module_": (
            "🪭 <b><a href='{}'>{}</a></b>\n"
            "ℹ️ <i>{}</i>\n\n"
            "▫️ <b>コマンド</b>: {}\n\n"
            "⛩ <b>ダウンロードリンク:</b> <code>{}</code>"
        ),
        "success": "✅ インストール済み",
        "install": "🌘 インストール",
        "restart": "🔄 再起動が必要",
        "error": "🚫 エラー",
        "source": "📁 ソース",
    }

    strings_ua = {
        "what_": "<emoji id=5190748314026385859>🤷‍♂️</emoji> Немає аргументів (ім'я модуля або команда)",
        "search_": "<emoji id=5188311512791393083>🔎</emoji> <b>Пошук модуля...</b>",
        "nope_": "<emoji id=5346063050233360577>😮</emoji> <b>Не вдалося знайти модуль</b>",
        "module_": (
            "🪭 <b><a href='{}'>{}</a></b>\n"
            "ℹ️ <i>{}</i>\n\n"
            "▫️ <b>Команди</b>: {}\n\n"
            "⛩ <b>Посилання на завантаження:</b> <code>{}</code>"
        ),
        "success": "✅ Встановлено",
        "install": "🌘 Встановити",
        "restart": "🔄 Потрібне перезавантаження",
        "error": "🚫 Помилка",
        "source": "📁 Вихідний код",
    }

    strings_kz = {
        "what_": "<emoji id=5190748314026385859>🤷‍♂️</emoji> Аргументтер жоқ (модульдің атауы немесе команда)",
        "search_": "<emoji id=5188311512791393083>🔎</emoji> <b>Модульді іздеу...</b>",
        "nope_": "<emoji id=5346063050233360577>😮</emoji> <b>Модуль табылмады</b>",
        "module_": (
            "🪭 <b><a href='{}'>{}</a></b>\n"
            "ℹ️ <i>{}</i>\n\n"
            "▫️ <b>Бұйрықтар</b>: {}\n\n"
            "⛩ <b>Жүктеу сілтемесі:</b> <code>{}</code>"
        ),
        "success": "✅ Орнатылды",
        "install": "🌘 Орнату",
        "restart": "🔄 Қайта жүктеу қажет",
        "error": "🚫 Қате",
        "source": "📁 Мәнбе",
    }

    @loader.command()
    async def ml(self, app: Client, message: types.Message, args: str):
        """Get a link or a module file. Usage: ml <module name or command>"""
        if not args:
            return await message.answer(
                self.strings("what_"),
            )

        m = await message.answer(
            self.strings("search_"),
        )

        if not (module := self.all_modules.get_module(args, True, True)):
            return await message.answer(
                self.strings("nope_"),
            )

        get_module = inspect.getmodule(module)
        origin = get_module.__spec__.origin

        try:
            source = get_module.__loader__.data
        except AttributeError:
            source = inspect.getsource(get_module).encode("utf-8")

        source_code = io.BytesIO(source)
        source_code.name = f"{module.name}.py"
        source_code.seek(0)

        caption = (
            f'<emoji id=5260730055880876557>⛓</emoji> <a href="{origin}">Link</a> of <code>{module.name}</code> module:\n\n'
            f"<b>{origin}</b>"
            if origin != "<string>" and not os.path.exists(origin)
            else f"<emoji id=5870528606328852614>📁</emoji> <b>File of <code>{module.name}</code></b>"
        )

        await m.delete()
        return await message.answer(source_code, doc=True, caption=caption)

    @loader.command()
    async def aeliscmd(self, app, message):
        """Search module in Aelis API"""
        args = message.get_args_raw()
        if not args:
            return await message.answer(self.strings("what_"))
        await message.answer(self.strings("search_"))
        module = await self.aelis.search(args)
        if not module:
            return await message.answer(self.strings("nope_"))
        text = self.strings("module_").format(
            f"https://aelis.hikamoru.uz/view/{module['name']}",
            module["name"],
            module["description"],
            ", ".join(
                [f"<code>{self.prefix[0]}{i}</code>" for i in module["commands"]]
            ),
            module["link"],
        )
        return await message.answer(
            text,
            reply_markup=[
                [
                    {
                        "text": self.strings("install"),
                        "callback": self.module_load,
                        "kwargs": {"link": module["link"], "text": text},
                    },
                ]
            ],
        )

    async def module_load(self, call: CallbackQuery, link: str, text: str):
        r = await utils.run_sync(requests.get, link)
        mod = await self.all_modules.load_module(r.text, r.url)
        module = self.all_modules.get_module(mod, True)
        if module is True:
            return await call.edit(
                text,
                reply_markup=[[{"text": self.strings("restart"), "data": "empty"}]],
            )

        if not module:
            return await call.edit(
                text, reply_markup=[[{"text": self.strings("error"), "data": "empty"}]]
            )

        if module == "DAR":
            return await call.edit(
                text, reply_markup=[[{"text": self.strings("error"), "data": "empty"}]]
            )

        self.db.set(
            "shizu.loader",
            "modules",
            list(set(self.db.get("shizu.loader", "modules", []) + [link])),
        )
        return await call.edit(
            text, reply_markup=[[{"text": self.strings("success"), "data": "empty"}]]
        )
