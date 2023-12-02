# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru


import sys
from meval import meval
from pyrogram import Client, types

from .. import loader, utils, logger


@loader.module(name="ShizuEval", author="hikamoru")
class EvaluatorMod(loader.Module):
    """Execute python code"""
    

    @loader.command(aliases=["e"])
    async def eval(self, app: Client, message: types.Message):
        """Execute python code and return result"""
        args = message.get_args_raw()

        try:
            result = await meval(args, globals(), **self.getattrs(app, message))

            return await message.answer(
                "<b>🖥 Code:</b>\n"
                f"<pre language='python'>{args}</pre>\n\n"
                f"✅ <b>Result:</b>\n"
                f"<pre language='result'>{utils.escape_html(result)}</pre>",
            )
        except Exception:
            item = logger.CustomException.from_exc_info(*sys.exc_info())
            exc = (
                "\n\n"
                + "\n".join(item.full_stack.splitlines()[:-1])
                + "\n\n"
                + "😵 "
                + item.full_stack.splitlines()[-1]
            )
            return await message.answer(
                "<b>🖥 Code:</b>\n"
                f"<pre language='python'>{args}</pre>\n\n"
                "🚫 <b>Result:</b>\n"
                f"<pre language='error'>{exc}</pre>",
            )

    def getattrs(self, app: Client, message: types.Message):
        return {
            "self": self,
            "db": self.db,
            "app": app,
            "c": app,
            "tl": app.tl,
            "client": app,
            "bot": app,
            "message": message,
            "m": message,
            "chat": message.chat,
            "user": message.from_user,
            "reply": message.reply_to_message,
            "r": message.reply_to_message,
            "utils": utils,
            "ruser": getattr(message.reply_to_message, "from_user", None),
        }
