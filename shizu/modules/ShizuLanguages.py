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


import shutil
import os
from .. import loader, utils, translator


@loader.module("ShizuLanguages", "hikamoru", 1.0)
class ShizuLanguages(loader.Module):
    """To change language of Shizu"""

    strings = {
        "incorrect_language": "<emoji id=5807626765874499116>🚫</emoji> <b>Incorrect language</b>",
        "language_saved": "{} <b>Language saved</b>",
        "reply_to": "<emoji id=5870903672937911120>👀</emoji> <b>Reply to language pack</b>",
        "must_be_json": "<emoji id=5257965810634202885>📁</emoji> <b>Language pack must be json</b>",
        "downloading": "<emoji id=5361615491884398003>🔽</emoji> <b>Downloading...</b>",
    }

    strings_ru = {
        "incorrect_language": "<emoji id=5807626765874499116>🚫</emoji> <b>Неверный язык</b>",
        "language_saved": "{} <b>Язык сохранен</b>",
        "reply_to": "<emoji id=5870903672937911120>👀</emoji> <b>Ответь на языковой пакет</b>",
        "must_be_json": "<emoji id=5257965810634202885>📁</emoji> <b>Языковой пакет должен быть json</b>",
        "downloading": "<emoji id=5361615491884398003>🔽</emoji> <b>Загрузка...</b>",
    }

    strings_uz = {
        "incorrect_language": "<emoji id=5807626765874499116>🚫</emoji> <b>Noto'g'ri til</b>",
        "language_saved": "{} <b>Til saqlandi</b>",
        "reply_to": "<emoji id=5870903672937911120>👀</emoji> <b>Til paketiga javob bering</b>",
        "must_be_json": "<emoji id=5257965810634202885>📁</emoji> <b>Til paketi json bo'lishi kerak</b>",
        "downloading": "<emoji id=5361615491884398003>🔽</emoji> <b>Yuklab olinmoqda...</b>",
    }

    strings_jp = {
        "incorrect_language": "<emoji id=5807626765874499116>🚫</emoji> <b>言語が間違っています</b>",
        "language_saved": "{} <b>言語が保存されました</b> ",
        "reply_to": "<emoji id=5870903672937911120>👀</emoji> <b>言語パックに返信する</b>",
        "must_be_json": "<emoji id=5257965810634202885>📁</emoji> <b>言語パックはjsonである必要があります</b>",
        "downloading": "<emoji id=5361615491884398003>🔽</emoji> <b>ダウンロード中...</b>",
    }

    strings_ua = {
        "incorrect_language": "<emoji id=5807626765874499116>🚫</emoji> <b>Неправильна мова</b>",
        "language_saved": "{} <b>Мова збережена</b>",
        "reply_to": "<emoji id=5870903672937911120>👀</emoji> <b>Відповідь на мовний пакет</b>",
        "must_be_json": "<emoji id=5257965810634202885>📁</emoji> <b>Мовний пакет повинен бути json</b>",
        "downloading": "<emoji id=5361615491884398003>🔽</emoji> <b>Завантаження...</b>",
    }

    strings_kz = {
        "incorrect_language": "<emoji id=5807626765874499116>🚫</emoji> <b>Дұрыс тіл емес</b>",
        "language_saved": "{} <b>Тіл сақталды</b> ",
        "reply_to": "<emoji id=5870903672937911120>👀</emoji> <b>Тіл пакетіне жауап беріңіз</b>",
        "must_be_json": "<emoji id=5257965810634202885>📁</emoji> <b>Тіл пакеті json болуы керек</b>",
        "downloading": "<emoji id=5361615491884398003>🔽</emoji> <b>Жүктелуде...</b>",
    }

    strings_kr = {
        "incorrect_language": "<emoji id=5807626765874499116>🚫</emoji> <b>잘못된 언어</b>",
        "language_saved": "{} <b>언어가 저장되었습니다</b>",
        "reply_to": "<emoji id=5870903672937911120>👀</emoji> <b>언어 팩에 응답</b>",
        "must_be_json": "<emoji id=5257965810634202885>📁</emoji> <b>언어 팩은 json이어야합니다</b>",
        "downloading": "<emoji id=5361615491884398003>🔽</emoji> <b>다운로드 중...</b>",
    }


    async def setlangcmd(self, app, message):
        """Change default language"""
        args = utils.get_args_raw(message)
        if not args or any(len(i) != 2 for i in args.split(" ")):
            await utils.answer(message, self.strings("incorrect_language"))
            return

        self.db.set("shizu.me", "lang", args.lower())

        await message.answer(
            self.strings("language_saved").format(utils.get_lang_flag(args.lower()))
        )

    async def loadlgpackcmd(self, app, message):
        """Load language pack (reply to file .json and write language code)"""
        reply = message.reply_to_message
        args = utils.get_args_raw(message)
        if not reply or not reply.document:
            await utils.answer(message, self.strings("reply_to"))
            return

        if not reply.document.file_name.endswith(".json"):
            await utils.answer(message, self.strings("must_be_json"))
            return

        await message.answer(self.strings("downloading"))
        mm = await app.download_media(reply, f"{args.lower()}.json")
        check_dir = f"{utils.get_base_dir()}/langpacks"
        if not os.path.exists(check_dir):
            os.mkdir(check_dir)
        langpack_path = f"{utils.get_base_dir()}/langpacks/{args.lower()}.json"
        shutil.move(mm, langpack_path)

        await message.answer("<b>Downloaded</b>")
        tr = translator.Translator(app, self.db)
        await tr.init()
        await message.answer(
            self.strings("language_saved").format(utils.get_lang_flag(args.lower()))
        )

    @loader.command()
    async def langs(self, app, message):
        """Available languages"""
        langs = ["us", "ru", "kz", "ua", "uz", "jp", "kr"]
        await message.answer(
            "🌍 <b>Available languages:</b>\n"
            + "\n".join(
                f"{utils.get_lang_flag(lang)} <code>{lang}</code>" for lang in langs
            ),
            reply_markup=utils.chunks(
                [
                    {
                        "text": f"{utils.get_lang_flag(lang)} {lang}",
                        "callback": self.setlang_cb,
                        "args": (lang,),
                    }
                    for lang in langs
                ],
                3,
            ),
        )

    async def setlang_cb(self, app, lang):
        self.db.set("shizu.me", "lang", lang)
        await app.edit(self.strings("language_saved").format(utils.get_lang_flag(lang)))
