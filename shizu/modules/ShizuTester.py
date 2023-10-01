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


import time
import io
import os
import sys
import atexit

import logging
from .. import logger

from pyrogram import Client, types
from pyrogram.raw import functions, types as typ
from .. import loader, utils


@loader.module(name="ShizuTester", author="shizu")
class TesterMod(loader.Module):
    """Execute activities based on userbot self-testing"""

    @loader.command()
    async def logs(self, app: Client, message: types.Message, args: str):
        """To get logs. Usage: logs (verbosity level)"""
        lvl = 40  # ERROR

        if args and not (lvl := logger.get_valid_level(args)):
            return await message.answer("Invalid verbosity level")

        handler = logging.getLogger().handlers[0]
        logs = ("\n".join(handler.dumps(lvl))).encode("utf-8")
        if not logs:
            return await message.answer(
                f"❕ You don't have any logs at verbosity  {lvl} ({logging.getLevelName(lvl)})",
            )

        logs = io.BytesIO(logs)
        logs.name = "shizu.log"

        await message.delete()
        return await message.answer(
            logs,
            doc=True,
            caption=f"🐙 Shizu logs with verbosity {lvl} ({logging.getLevelName(lvl)})",
        )

    @loader.command()
    async def setprefix(self, app: Client, message: types.Message, args: str):
        """To change the prefix, you can have several pieces separated by a space. Usage: setprefix (prefix) [prefix, ...]"""
        if not (args := args.split()):
            return await message.answer("❔ Which prefix should I change to?")

        self.db.set("shizu.loader", "prefixes", list(set(args)))
        prefixes = ", ".join(f"<code>{prefix}</code>" for prefix in args)
        return await message.answer(f"✅ Prefix has been changed to {prefixes}")

    @loader.command()
    async def addalias(self, app: Client, message: types.Message, args: str):
        """Add an alias. Usage: addalias (new alias) (command)"""
        if not (args := args.lower().split(maxsplit=1)):
            return await message.answer("❔ Which alias should I add?")

        if len(args) != 2:
            return await message.answer(
                "❌ The arguments are incorrect."
                "✅ Correct: addalias <new alias> <command>",
            )

        aliases = self.all_modules.aliases
        if args[0] in aliases:
            return await message.answer("❌ Тsuch an alias already exists")

        if not self.all_modules.command_handlers.get(args[1]):
            return await message.answer("❌ There is no such command")

        aliases[args[0]] = args[1]
        self.db.set("shizu.loader", "aliases", aliases)

        return await message.answer(
            f"✅ Alias <code>{args[0]}</code> for the command <code>{args[1]}</code> has been added",
        )

    @loader.command()
    async def delalias(self, app: Client, message: types.Message, args: str):
        """Delete the alias. Usage: delalas (alias)"""
        if not (args := args.lower()):
            return await message.answer("❔ Which alias should I delete?")

        aliases = self.all_modules.aliases
        if args not in aliases:
            return await message.answer("❌ There is no such alias")

        del aliases[args]
        self.db.set("shizu.loader", "aliases", aliases)

        return await message.answer(f"✅ Alias <code>{args}</code> has been deleted")

    @loader.command()
    async def aliases(self, app: Client, message: types.Message):
        """Show all aliases"""
        if aliases := self.all_modules.aliases:
            return await message.answer(
                "🗄 List of all aliases:\n"
                + "\n".join(
                    f"• <code>{alias}</code> ➜ {command}"
                    for alias, command in aliases.items()
                ),
            )
        else:
            return await message.answer("Алиасов нет")

    @loader.command()
    async def ping(self, app: Client, message: types.Message, args: str):
        """Checks the response rate of the user bot"""
        start = time.perf_counter_ns()
        await message.answer("<emoji id=5267444331010074275>▫️</emoji>")
        ping = round((time.perf_counter_ns() - start) / 10**6, 3)
        await message.answer(
            f"<emoji id=5220226955206467824>⚡️</emoji> <b>Telegram Response Rate:</b> <code>{ping}</code> <b>ms</b>",
        )

    async def on_load(self, app: Client):
        """Create Folder"""
        if self.db.get("shizu.folder", "folder"):
            return

        logging.info("Trying to create folder")
        app.me = await app.get_me()
        folder_id = 250
        logs_id = (
            await utils.create_chat(
                app,
                "Shizu-logs",
                "📫 Shizu-logs do not delete this group, otherwise bot will be broken",
                True,
                True,
                True,
            )
        ).id

        backup_id = (
            await utils.create_chat(
                app,
                "Shizu-backup",
                "📫 Backup-logs do not delete this group, otherwise bot will be broken",
                True,
                True,
                True,
            )
        ).id

        logs = await app.resolve_peer(logs_id)
        backup = await app.resolve_peer(backup_id)

        await app.set_chat_photo(chat_id=logs_id, photo="assets/logs.jpg")
        await app.set_chat_photo(chat_id=backup_id, photo="assets/backups.jpg")

        await app.invoke(
            functions.messages.UpdateDialogFilter(
                id=folder_id,
                filter=typ.DialogFilter(
                    id=folder_id,
                    title="Shizu",
                    include_peers=[logs, backup],
                    pinned_peers=[],
                    exclude_peers=[],
                    emoticon="❤️",
                ),
            )
        )

        logging.info("Folder created")
        self.db.set("shizu.folder", "folder", True)
        self.db.set("shizu.chat", "logs", logs_id)
        self.db.set("shizu.chat", "backup", backup_id)
        atexit.register(os.execl(sys.executable, sys.executable, "-m", "shizu"))
