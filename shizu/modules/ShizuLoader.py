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


import re
import requests
from typing import List
from pyrogram import Client, types
from .. import loader, utils

VALID_URL = r"[-[\]_.~:/?#@!$&'()*+,;%<=>a-zA-Z0-9]+"

VALID_PIP_PACKAGES = re.compile(
    r"^\s*# required:(?: ?)((?:{url} )*(?:{url}))\s*$".format(url=VALID_URL),
    re.MULTILINE,
)
GIT_REGEX = re.compile(
    r"^https?://github\.com((?:/[a-z0-9-]+){2})(?:/tree/([a-z0-9-]+)((?:/[a-z0-9-]+)*))?/?$",
    flags=re.IGNORECASE,
)


async def get_git_raw_link(repo_url: str):
    """Get raw link to repository"""

    match = GIT_REGEX.search(repo_url)
    if not match:
        return False

    repo_path = match.group(1)
    branch = match.group(2)
    path = match.group(3)

    r = await utils.run_sync(requests.get, f"https://api.github.com/repos{repo_path}")
    if r.status_code != 200:
        return False

    branch = branch or r.json()["default_branch"]

    return f"https://raw.githubusercontent.com{repo_path}/{branch}{path or ''}/"


@loader.module(name="ShizuLoader", author="shizu")
class Loader(loader.Module):
    """Module loader"""

    @loader.command()
    async def dlmod(self, app: Client, message: types.Message, args: str):
        """Download module by link. Usage: dlmod <link or all or nothing>"""

        bot_username = (await self.bot.bot.get_me()).username
        dop_help = (
            "<emoji id=5100652175172830068>🔸</emoji>"
            if message.from_user.is_premium
            else "🔸"
        )
        modules_repo = self.db.get(
            "shizu.loader", "repo", "https://github.com/sh1tn3t/sub-modules"
        )
        api_result = await get_git_raw_link(modules_repo)
        if not api_result:
            return await utils.answer(message, "❌ Invalid repository link.\n")

        raw_link = api_result
        modules = await utils.run_sync(requests.get, f"{raw_link}all.txt")
        if modules.status_code != 200:
            return await utils.answer(
                message,
                (
                    f'❌ The all.txt file was not found in the <a href="{modules_repo}">repository</a>'
                ),
                disable_web_page_preview=True,
            )

        modules: List[str] = modules.text.splitlines()

        if not args:
            text = (
                f'📥 List of available modules with <ahref="{modules_repo}">repository</a>:\n\n'
                + "<code>all</code> - loads all modules\n"
                + "\n".join(map("<code>{}</code>".format, modules))
            )
            return await utils.answer(message, text, disable_web_page_preview=True)

        error_text: str = None
        module_name: str = None
        count = 0

        if args in modules:
            args = raw_link + args + ".py"

        try:
            r = await utils.run_sync(requests.get, args)
            if r.status_code != 200:
                raise requests.exceptions.ConnectionError

            await utils.answer(
                message,
                "<emoji id=5280506417478903827>🛡</emoji> Analyzing the module..",
            )
            module_name = await self.all_modules.load_module(r.text, r.url)
            if module_name == "DAR":
                error_text = "<emoji id=5203929938024999176>🛡</emoji> <b><u>Shizu</u> protected your account from</b> <code>DeleteAccount</code>.\n<emoji id=5404380425416090434>ℹ️</emoji> <b>This module contains a dangerous code that can delete your account.</b>"
            if module_name is True:
                error_text = "✅ Dependencies are installed. Reboot required"
            if not module_name:
                error_text = "❌ Failed to load the module. See the logs for details"
        except requests.exceptions.MissingSchema:
            error_text = "❌ The link is incorrect"
        except requests.exceptions.ConnectionError:
            error_text = "❌ The module is not available by the link"
        except requests.exceptions.RequestException:
            error_text = "❌ An unexpected error has occurred. See the logs for details"

        if error_text:
            return await utils.answer(message, error_text)

        self.db.set(
            "shizu.loader",
            "modules",
            list(set(self.db.get("shizu.loader", "modules", []) + [args])),
        )

        if not (module := self.all_modules.get_module(module_name, True)):
            return await utils.answer(
                message,
                "<b><emoji id=5465665476971471368>❌</emoji> There is no such module</b>",
            )

        prefix = self.db.get("shizu.loader", "prefixes", ["."])[0]
        command_descriptions = "\n".join(
            f"{dop_help} <code>{prefix + command}</code> - {module.command_handlers[command].__doc__ or 'No description'}"
            for command in module.command_handlers
        )
        inline_descriptions = "\n".join(
            f"{dop_help} <code>@{bot_username} {command}</code> - {module.inline_handlers[command].__doc__ or 'No description'}"
            for command in module.inline_handlers
        )
        modname = str(module.name).capitalize()

        header = (
            f"<emoji id=5267468588985363056>✔️</emoji> Module <b>{modname}</b> loaded\n"
            f"<emoji id=5787544344906959608>ℹ️</emoji> <b>Description:</b>"
            f" {module.__doc__ or 'No description'}\n\n"
        )
        footer = (
            f"<emoji id=5190458330719461749>🧑‍💻</emoji> <code>{module.author}</code>"
            if module.author
            else ""
        )
        return await utils.answer(
            message,
            header + command_descriptions + "\n" + inline_descriptions + "\n" + footer,
        )

    @loader.command()
    async def loadmod(self, app: Client, message: types.Message):
        """Load the module by file. Usage: <replay per file>"""
        reply = message.reply_to_message
        bot_username = (await self.bot.bot.get_me()).username
        dop_help = (
            "<emoji id=5100652175172830068>🔸</emoji>"
            if message.from_user.is_premium
            else "🔸"
        )
        file = (
            message if message.document else reply if reply and reply.document else None
        )

        if not file:
            return await utils.answer(message, "❌ Нет реплая на файл")

        await utils.answer(
            message,
            "<emoji id=5215493819641895305>🚛</emoji> <b>Loading the module..</b>",
        )
        file = await reply.download()

        modules = [
            "ShizuBackuper",
            "ShizuHelp",
            "ShizuLoader",
            "ShizuTerminal",
            "ShizuTester",
            "ShizuUpdater",
            "ShizuEval",
            "ShizuModulesHelper",
            "ShizuStart",
            "ShizuSecurty",
        ]

        for mod in modules:
            if file == mod:
                return await utils.answer(
                    message, "❌ It is not allowed to load core modules"
                )

        try:
            with open(file, "r", encoding="utf-8") as file:
                module_source = file.read()
        except UnicodeDecodeError:
            return await utils.answer(message, "❌ Incorrect file encoding")
        await utils.answer(
            message, "<emoji id=5280506417478903827>🛡</emoji> Analyzing the module.."
        )

        module_name = await self.all_modules.load_module(module_source)

        if module_name is True:
            return await utils.answer(
                message, "✅ Dependencies are installed. Reboot required"
            )

        if not module_name:
            return await utils.answer(
                message, "❌ Failed to load the module. See the logs for details"
            )

        if module_name == "DAR":
            return await utils.answer(
                message,
                "<emoji id=5203929938024999176>🛡</emoji> <b><u>Shizu</u> protected your account from</b> <code>DeleteAccount</code>.\n<emoji id=5404380425416090434>ℹ️</emoji> <b>This module contains a dangerous code that can delete your account.</b>",
            )

        module = "_".join(module_name.lower().split())
        with open(f"shizu/modules/{module}.py", "w", encoding="utf-8") as file:
            file.write(module_source)

        if not (module := self.all_modules.get_module(module_name, True)):
            return await utils.answer(
                message,
                "<b><emoji id=5465665476971471368>❌</emoji> There is no such module</b>",
            )

        prefix = self.db.get("shizu.loader", "prefixes", ["."])[0]
        command_descriptions = "\n".join(
            f"{dop_help} <code>{prefix + command}</code> - {module.command_handlers[command].__doc__ or 'No description'}"
            for command in module.command_handlers
        )
        inline_descriptions = "\n".join(
            f"{dop_help} <code>@{bot_username} {command}</code> - {module.inline_handlers[command].__doc__ or 'No description'}"
            for command in module.inline_handlers
        )
        modname = str(module.name).capitalize()

        header = (
            f"<emoji id=5267468588985363056>✔️</emoji> Module <b>{modname}</b> loaded\n"
            f"<emoji id=5787544344906959608>ℹ️</emoji> <b>Description:</b>"
            f" {module.__doc__ or 'No description'}\n\n"
        )
        footer = (
            f"<emoji id=5190458330719461749>🧑‍💻</emoji> <code>{module.author}</code>"
            if module.author
            else ""
        )
        return await utils.answer(
            message,
            header + command_descriptions + "\n" + inline_descriptions + "\n" + footer,
        )

    @loader.command()
    async def unloadmod(self, app: Client, message: types.Message, args: str):
        """Unload the module. Usage: unloadmod <module name>"""
        if not (module_name := self.all_modules.unload_module(args)):
            return await utils.answer(message, "❌ Incorrect module name")

        modules = [
            "ShizuBackuper",
            "ShizuHelp",
            "ShizuLoader",
            "ShizuTerminal",
            "ShizuTester",
            "ShizuUpdater",
            "ShizuEval",
            "ShizuModulesHelper",
            "ShizuStart",
            "ShizuSecurty",
        ]

        if module_name in modules:
            return await utils.answer(
                message,
                "<emoji id=5364241851500997604>⚠️</emoji> You cannot unload the core modules",
            )

        return await utils.answer(
            message,
            f"<emoji id=6334471265700546607>🧹</emoji> Module <code>{module_name}</code> unloaded",
        )
