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

import inspect

from pyrogram import Client, types
from .. import loader, utils


@loader.module("ShizuModulesHelper", "hikamoru")
class ModulesLinkMod(loader.Module):
    """Link or file of the installed module"""

    @loader.command()
    async def ml(self, app: Client, message: types.Message, args: str):
        """Get a link or a module file. Usage: ml <module name or command>"""
        if not args:
            return await message.answer(
                "<emoji id=5190748314026385859>🤷‍♂️</emoji> No arguments are specified (module name or command)",
            )

        m = await message.answer(
            "<emoji id=5188311512791393083>🔎</emoji> <b>Module search...</b>"
        )

        if not (module := self.all_modules.get_module(args, True, True)):
            return await message.answer(
                "<emoji id=5346063050233360577>😮</emoji> <b>Couldn't find the module</b>",
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
