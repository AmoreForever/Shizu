# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru

from pyrogram import Client, types
from .. import loader, utils


@loader.module(name="ShizuHelp", author="shizu")
class Help(loader.Module):
    """[module] - Show help"""

    strings = {
        "available": "{} <b>{} modules available</b>\n{}",
        "support": "🧑‍🔬 <b>If you have any questions, suggestions or bug reports, please let us know in our support chat: @shizu_talks</b>",
        "button": "🗼 Support chat",
    }

    strings_ru = {
        "available": "{} <b>{} модулей доступно</b>\n{}",
        "support": "🧑‍🔬 <b>Если у вас есть вопросы, предложения или сообщения об ошибках, сообщите нам в нашем чате поддержки: @shizu_talks</b>",
        "button": "🗼 Чат поддержки",
    }

    strings_uz = {
        "available": "{} <b>{} modullar mavjud</b>\n{}",
        "support": "🧑‍🔬 <b>Savollaringiz, takliflaringiz yoki xatolaringiz bo'lsa, iltimos, bizga yordam beruvchi chatga xabar bering: @shizu_talks</b>",
        "button": "🗼 Yordam chati",
    }

    strings_jp = {
        "available": "{} <b>利用可能な {} のモジュールがあります</b>\n{}",
        "support": "🧑‍🔬 <b>質問、提案、バグ報告がある場合は、サポートチャットでお知らせください: @shizu_talks</b>",
        "button": "🗼 サポートチャット",
    }

    strings_ua = {
        "available": "{} <b>{} модулів доступно</b>\n{}",
        "support": "🧑‍🔬 <b>Якщо у вас є питання, пропозиції або повідомлення про помилки, повідомте нам у нашому чаті підтримки: @shizu_talks</b>",
        "button": "🗼 Чат підтримки",
    }

    strings_kz = {
        "available": "{} <b>{} модуль қолжетімді</b>\n{}",
        "support": "🧑‍🔬 <b>Сұрақтарыңыз, ұсыныстарыңыз немесе қателер туралы хабарласу үшін, біздің қолдау құрамасында хабарласыңыз: @shizu_talks</b>",
        "button": "🗼 Қолдау құрамасы",
    }

    @loader.command()
    async def help(self, app: Client, message: types.Message):
        """Show help"""

        args = message.get_args()
        dop_help = (
            "<emoji id=5100652175172830068>☁️</emoji>"
            if message.from_user.is_premium
            else "🔸"
        )
        bot_username = self.db.get("shizu.bot", "username", None)
        sorted_modules = sorted(
            self.all_modules.modules,
            key=lambda mod: (mod.name not in self.cmodules, len(mod.name)),
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
                    module_emoji = "🀄️" if module.name in self.cmodules else "🎴"
                    text += (
                        f"\n<b>{module_emoji} {module.name}</b> - [ "
                        + (commands or "")
                        + (inline or "")
                        + " ]"
                    )

            help_emoji = "<emoji id=6334457642064283339>🐙</emoji>"

            return await message.answer(
                self.strings("available").format(
                    help_emoji, len(self.all_modules.modules) - 1, text
                )
            )

        if not (module := self.all_modules.get_module(args.lower(), True, True)):
            return await message.answer(
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

        return await message.answer(
            header + command_descriptions + "\n" + inline_descriptions
        )

    @loader.command()
    async def support(self, app, message):
        """Support"""
        await message.answer(
            self.strings("support"),
            reply_markup=[
                [{"text": self.strings("button"), "url": "https://t.me/shizu_talks"}]
            ],
            prev=True,
        )
