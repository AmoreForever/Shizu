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

from subprocess import check_output
from pyrogram import Client, types

from .. import loader, utils
from ..wrappers import wrap_function_to_async


@wrap_function_to_async
def bash_exec(args: str):
    try:
        output = check_output(args.strip(), shell=True)
        output = output.decode()

        return output
    except UnicodeDecodeError:
        return check_output(args.strip(), shell=True)
    except Exception as error:
        return error


@loader.module(name="ShizuTerminal", author="shizu")
class TerminalMod(loader.Module):
    """Terminal"""
    
    @loader.command()
    async def terminal(self, app: Client, message: types.Message, args: str):
        await utils.answer(
            message, "<emoji id=5325822763447884498>💠</emoji> <b>wait...</b>"
        )
        output = await bash_exec(args)

        await utils.answer(
            message,
            f"<emoji id=5472111548572900003>⌨️</emoji> <b>Команда:</b> <code>{args.strip()}</code>\n"
            f"💾 <b>Вывод:</b>\n<code>"
            f"{output}"
            f"</code>",
        )
