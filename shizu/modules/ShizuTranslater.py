# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru

import translators as ts

from pyrogram import types, Client
from .. import loader, utils


@loader.module("ShizuTranslater", "hikamoru", 1.0)
class ShizuTranslater(loader.Module):
    """Core Shizu translate module"""

    @loader.command()
    async def tr(self, app: Client, message: types.Message):
        """[lang] [text/reply]"""
        args = utils.get_args_raw(message)

        if message.reply_to_message and (
            message.reply_to_message.text or message.reply_to_message.caption
        ):
            text = message.reply_to_message.text or message.reply_to_message.caption
        else:
            text = args.split(maxsplit=1)[1] if args and len(args) > 2 else None

        lang = args.split(maxsplit=1)[0].lower() if args and len(args) > 1 else "en"

        try:
            await message.answer(ts.translate_text(text, to_language=lang))
        except Exception:
            await message.answer(ts.translate_text(text, to_language="en"))
