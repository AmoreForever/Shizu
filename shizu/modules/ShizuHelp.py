# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru

from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

from pyrogram import Client, types
import re
from .. import loader, utils


@loader.module(name="ShizuHelp", author="shizu")
class Help(loader.Module):
    """[module] - Show help"""

    async def support_inline_handler(self, app: Client, inline_query: InlineQuery):
        """Responds to inline queries"""
        message = InputTextMessageContent("✨ Do you need help? don't be shy :)")

        return await inline_query.answer(
            [
                InlineQueryResultArticle(
                    id=utils.random_id(),
                    title="Support Chat",
                    input_message_content=message,
                    reply_markup=(
                        InlineKeyboardMarkup().add(
                            InlineKeyboardButton(
                                text="🧑‍💻 Support Chat", url="https://t.me/shizu_talks"
                            )
                        )
                    ),
                )
            ],
            cache_time=0,
        )

    @loader.command()
    async def help(self, app: Client, message: types.Message):
        """Список всех модулей"""

        args = utils.get_args(message)
        dop_help = (
            "<emoji id=5100652175172830068>☁️</emoji>"
            if message.from_user.is_premium
            else "🔸"
        )
        bot_username = self.db.get("shizu.bot", "username", None)

        sorted_modules = sorted(
            self.all_modules.modules,
            key=lambda mod: (not mod.name.startswith("Shizu"), len(mod.name)),
        )

        if not args:
            text = ""
            for module in sorted_modules:
                if module.name.lower() == "help":
                    continue
                commands = inline = ""
                commands += " <b>|</b> ".join(
                    f"<code>{command}</code>" for command in module.command_handlers
                )
                if module.inline_handlers:
                    if commands:
                        inline += " <b><emoji id=5258093637450866522>🤖</emoji></b> "
                    else:
                        inline += "<b><emoji id=5258093637450866522>🤖</emoji></b>: "

                inline += " <b>|</b> ".join(
                    f"<code>{inline_command}</code>"
                    for inline_command in module.inline_handlers
                )

                if commands or inline:
                    module_emoji = (
                        "<emoji id=5100862156123931478>▪️</emoji>"
                        if module.name.startswith("Shizu")
                        else "<emoji id=5100652175172830068>▫️</emoji>"
                    )
                    text += (
                        f"\n<b>{module_emoji} {module.name}</b> - [ "
                        + (commands or "")
                        + (inline or "")
                        + " ]"
                    )

            help_emoji = "<emoji id=6334457642064283339>🐙</emoji>"

            return await utils.answer(
                message,
                f"{help_emoji} <b>{len(self.all_modules.modules)-1} modules available</b>\n"
                f"{text}",
            )

        if not (module := self.all_modules.get_module(args.lower(), True, True)):
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
        modname = module.name
        header = (
            f"<emoji id=6334457642064283339>🐙</emoji> <b>{modname}</b>\n"
            f"<emoji id=5787544344906959608>ℹ️</emoji>"
            f" {module.__doc__ or 'No description'}\n\n"
        )

        return await utils.answer(
            message, header + command_descriptions + "\n" + inline_descriptions
        )

    @loader.command()
    async def support(self, app, message):
        """Support"""
        await message.delete()
        await utils.answer_inline(message, "support")
 