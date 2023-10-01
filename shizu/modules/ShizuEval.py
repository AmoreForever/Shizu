# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru


import sys
import re
import logging
from meval import meval
from pyrogram import Client, types

from .. import loader, utils, logger


class DeleteAccountIsForbidden(Exception):
    """For prohibited actions"""

    def __init__(self, message):
        super().__init__(message)


@loader.module(name="ShizuEval", author="hikamoru")
class EvaluatorMod(loader.Module):
    """Выполняет python-код"""

    @loader.command()
    async def eval(self, app: Client, message: types.Message):
        """Execute python code and return result"""

        args = message.get_args_raw()
        try:
            delete_account_re = re.compile(r"DeleteAccount", re.IGNORECASE)
            if delete_account_re.search(args):
                logging.error(
                    "DO NOT TRY TO DELETE ACCOUNT, IF YOU WHAT YOU MAY DO IT HERE: https://my.telegram.org/auth"
                )
                raise DeleteAccountIsForbidden("DeleteAccount is forbidden")
            result = await meval(args, globals(), **self.getattrs(app, message))
            return await message.answer(
                "<b><emoji id=4985626654563894116>🖥</emoji> Code:</b>\n"
                f"<code>{args}</code>\n\n"
                f"<emoji id=5021905410089550576>✅</emoji> <b>Result:</b>\n"
                f"<code>{result}</code>",
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
                "<b><emoji id=4985626654563894116>🖥</emoji> Code:</b>\n"
                f"<code>{args}</code>\n\n"
                "<emoji id=5877477244938489129>🚫</emoji> <b>Result:</b>\n"
                f"{exc}",
            )

    def getattrs(self, app: Client, message: types.Message):
        return {
            "self": self,
            "db": self.db,
            "app": app,
            "c": app,
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
