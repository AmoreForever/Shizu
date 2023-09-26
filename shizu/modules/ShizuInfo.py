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

import configparser

import platform
import psutil

from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)


from pyrogram import Client, types
from .. import loader, utils, version

@loader.module("ShizuInfo", "sh1tn3t")
class InformationMod(loader.Module):
    """Информаци"""

    def text_(self, me: types.User):
        mention = f'<a href="tg://user?id={me.id}">{utils.get_display_name(me)}</a>'
        prefix = ", ".join(self.prefix)
        return (
            "<emoji id=6334457642064283339>🐙</emoji> <b>Shizu UserBot</b>\n\n"
            f"<emoji id=5467406098367521267>👑</emoji> <b>Owner</b>: {mention}\n\n"
            f"<emoji id=5449918202718985124>🌳</emoji> <b>Branch</b>: <code>{version.branch}</code>\n"
            f"<emoji id=5445096582238181549>🦋</emoji> <b>Version</b>: <code>{'.'.join(map(str, version.__version__))}</code>\n\n"
            f"<emoji id=6334316848741352906>⌨️</emoji> <b>Prefix</b>: <code>{prefix}</code>\n"
            f"{utils.get_platform()}"
        )
    
    @loader.command()
    async def info(self, app: Client, message: types.Message):
        """Информация о боте"""
        await utils.answer(
            message,
            "https://0x0.st/HOP4.jpg",
            caption=self.text_(message.from_user),
            photo=True
        )