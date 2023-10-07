# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru


try:
    import translators as ts
except ModuleNotFoundError:
    ts = None

from pyrogram import types, Client
from .. import loader, utils


@loader.module("ShizuTranslater", "hikamoru", 1.0)
class ShizuTranslater(loader.Module):
    """Core Shizu translate module"""

    @loader.command()
    async def tr(self, app: Client, message: types.Message):
        """[lang] [text/reply]"""
        if not ts:
            return await message.answer(
                f"<emoji id=5807626765874499116>🚫</emoji> <code>translators</code> module is not installed.\n\nYou can install it by command <code>{self.prefix[0]}terminal pip install translators</code>"
            )

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
