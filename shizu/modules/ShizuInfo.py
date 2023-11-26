"""
    █ █ ▀ █▄▀ ▄▀█ █▀█ ▀    ▄▀█ ▀█▀ ▄▀█ █▀▄▀█ ▄▀█
    █▀█ █ █ █ █▀█ █▀▄ █ ▄  █▀█  █  █▀█ █ ▀ █ █▀█

    Copyright 2022 t.me/hikariatama
    Licensed under the GNU GPLv3
"""

# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru

import requests

from pyrogram import Client, types
from .. import loader, utils, version


@loader.module("ShizuInfo", "hikamoru")
class InformationMod(loader.Module):
    """Info"""

    strings = {
        "custom_msg": "Custom message must have {mention}, {version}, {prefix}, {branch}, {platform} keywords",
        "custom_button": "Custom button must have text and url",
        "photo_url": "Photo url must be valid",
        "text": (
            "🐙 <b>Shizu UserBot</b>\n\n"
            "👩‍💼 <b>Owner of userbot</b>: {mention}\n"
            "👩‍🎤 <b>Inline bot</b>: @{username}\n\n"
            "• <b>Branch</b>: <code>{branch}</code>\n"
            "• <b>Version</b>: <code>{version}</code>\n"
            "• <b>Prefix</b>: «<code>{prefix}</code>»\n\n"
            "{platform}\n\n"
        ),
    }

    strings_ru = {
        "custom_msg": "Пользовательское сообщение должно содержать ключевые слова {mention}, {version}, {prefix}, {branch}, {platform}",
        "custom_button": "Пользовательская кнопка должна содержать текст и url",
        "photo_url": "URL фотографии должен быть действительным",
        "text": (
            "🐙 <b>Shizu UserBot</b>\n\n"
            "👩‍💼 <b>Владелец юзербота</b>: {mention}\n"
            "👩‍🎤 <b>Инлайн бот</b>: @{username}\n\n"
            "• <b>Ветка</b>: <code>{branch}</code>\n"
            "• <b>Версия</b>: <code>{version}</code>\n"
            "• <b>Префикс</b>: «<code>{prefix}</code>»\n\n"
            "{platform}\n\n"
        ),
    }

    strings_uz = {
        "custom_msg": "Foydalanuvchi xabari {mention}, {version}, {prefix}, {branch}, {platform} kalit so'zlarini o'z ichiga olishi kerak",
        "custom_button": "Foydalanuvchi tugmasi matn va url ni o'z ichiga olishi kerak",
        "photo_url": "Rasm url manzili to'g'ri bo'lishi kerak",
        "text": (
            "🐙 <b>Shizu UserBot</b>\n\n"
            "👩‍💼 <b>Userbot egasi</b>: {mention}\n"
            "👩‍🎤 <b>Inline bot</b>: @{username}\n\n"
            "• <b>Branch</b>: <code>{branch}</code>\n"
            "• <b>Version</b>: <code>{version}</code>\n"
            "• <b>Prefix</b>: «<code>{prefix}</code>»\n\n"
            "{platform}\n\n"
        ),
    }

    strings_jp = {
        "custom_msg": "カスタムメッセージには、{mention}、{version}、{prefix}、{branch}、{platform} のキーワードが必要です",
        "custom_button": "カスタムボタンにはテキストとURLが必要です",
        "photo_url": "写真のURLは有効である必要があります",
        "text": (
            "🐙 <b>Shizu UserBot</b>\n\n"
            "👩‍💼 <b>所有者</b>: {mention}\n"
            "👩‍🎤 <b>インラインボット</b>: @{username}\n\n"
            "• <b>ブランチ</b>: <code>{branch}</code>\n"
            "• <b>バージョン</b>: <code>{version}</code>\n"
            "• <b>プレフィックス</b>: «<code>{prefix}</code>»\n\n"
            "{platform}\n\n"
        ),
    }

    strings_ua = {
        "custom_msg": "Користувацьке повідомлення повинно містити ключові слова {mention}, {version}, {prefix}, {branch}, {platform}",
        "custom_button": "Користувацька кнопка повинна містити текст та url",
        "photo_url": "URL фотографії повинен бути дійсним",
        "text": (
            "🐙 <b>Shizu UserBot</b>\n\n"
            "👩‍💼 <b>Власник юзербота</b>: {mention}\n"
            "👩‍🎤 <b>Інлайн бот</b>: @{username}\n\n"
            "• <b>Гілка</b>: <code>{branch}</code>\n"
            "• <b>Версія</b>: <code>{version}</code>\n"
            "• <b>Префікс</b>: «<code>{prefix}</code>»\n\n"
            "{platform}\n\n"
        ),
    }

    strings_kz = {
        "custom_msg": "Қолданушы қолданбасы {mention}, {version}, {prefix}, {branch}, {platform} сөздерін қолжетімді болуы керек",
        "custom_button": "Қолданушы түймесі мәтін мен url болуы керек",
        "photo_url": "Фото URL мекен-жайы растауы керек",
        "text": (
            "🐙 <b>Shizu UserBot</b>\n\n"
            "👩‍💼 <b>Юзерботтың иесі</b>: {mention}\n"
            "👩‍🎤 <b>Инлайн бот</b>: @{username}\n\n"
            "• <b>Беті</b>: <code>{branch}</code>\n"
            "• <b>Нұсқа</b>: <code>{version}</code>\n"
            "• <b>Префикс</b>: «<code>{prefix}</code>»\n\n"
            "{platform}\n\n"
        ),
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "custom_message",
            False,
            lambda: self.strings("custom_msg"),
            "custom_buttons",
            {"text": "🤝 Support", "url": "https://t.me/shizu_talks"},
            lambda: self.strings("custom_button"),
            "photo_url",
            "https://github.com/AmoreForever/shizuassets/blob/master/shizubanner.jpg?raw=true",
            lambda: self.strings("photo_url"),
        )
        

    def text_(self, me: types.User, username):
        """Get text"""
        mention = f'<a href="tg://user?id={me.id}">{utils.escape_html((utils.get_display_name(me)))}</a>'
        prefix = ", ".join(self.prefix)

        if self.config["custom_message"]:
            return "🐙 Shizu\n" + self.config["custom_message"].format(
                mention=mention,
                version={".".join(map(str, version.__version__))},
                prefix=prefix,
                branch=version.branch,
                platform=utils.get_platform(),
            )

        return (
            self.strings("text").format(
                mention=mention,
                version=".".join(map(str, version.__version__)),
                prefix=prefix,
                branch=version.branch,
                platform=utils.get_platform(),
                username=username,
            )
        )

    @loader.command()
    async def info(self, app: Client, message: types.Message):
        """Info about Shizu"""
        if self.config["custom_buttons"]:
            await message.answer(
                response=self.text_(
                    self.me, (await self.bot.bot.get_me()).username
                ),
                reply_markup=[[self.config["custom_buttons"]]],
                photo=self.config["photo_url"],
            )
        else:
            await message.answer(
                response=self.config["photo_url"],
                photo_=True,
                caption=self.text_(
                    self.me, (await self.bot.bot.get_me()).username
                ),
            )
