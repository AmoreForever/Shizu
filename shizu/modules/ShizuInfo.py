# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru


from pyrogram import Client, types
from .. import loader, utils, version


@loader.module("ShizuInfo", "sh1tn3t")
class InformationMod(loader.Module):
    """Info"""

    def text_(self, me: types.User):
        mention = f'<a href="tg://user?id={me.id}">{utils.get_display_name(me)}</a>'
        prefix = ", ".join(self.prefix)
        if (
            self.db.get("shizu.info", "text", None)
            and self.db.get("shizu.info", "text", None) != "default"
        ):
            return (
                "<emoji id=6334457642064283339>🐙</emoji> Shizu\n"
                + self.db.get("shizu.info", "text", None)
            ).format(
                mention=mention,
                version={".".join(map(str, version.__version__))},
                prefix=prefix,
                branch=version.branch,
                platform=utils.get_platform(),
            )
        else:
            return (
                "<emoji id=6334457642064283339>🐙</emoji> <b>Shizu UserBot</b>\n\n"
                f"<emoji id=5467406098367521267>👑</emoji> <b>Owner</b>: {mention}\n\n"
                f"<emoji id=5449918202718985124>🌳</emoji> <b>Branch</b>: <code>{version.branch}</code>\n"
                f"<emoji id=5445096582238181549>🦋</emoji> <b>Version</b>: <code>{'.'.join(map(str, version.__version__))}</code>\n\n"
                f"<emoji id=6334316848741352906>⌨️</emoji> <b>Prefix</b>: <code>{prefix}</code>\n"
                f"{utils.get_platform()}"
            )

    @loader.command()
    async def info(self, app: Client, message: types.Message):
        """Info about Shizu"""
        await message.answer(
            self.db.get("shizu.info", "pic", None) or "https://0x0.st/HOP4.jpg",
            caption=self.text_(message.from_user),
            photo=True,
        )

    @loader.command()
    async def setinfo(self, app: Client, message: types.Message):
        """[-t] - Change text of info, kwargs: (mention, version, prefix, branch, platform) | [-p] - Change photo of info"""
        args = message.get_args_raw()
        if not args:
            return await message.answer("❔ What should I change?")
        if "-t" in args:
            self.db.set("shizu.info", "text", args)
            return await message.answer(
                "<emoji id=5963242192741863664>📝</emoji> <b>Info has been changed...</b>"
            )
        if "-p" in args:
            if not args.split()[1].startswith("http"):
                return await message.answer(
                    "<emoji id=5780722455077196625>🔗</emoji> <b>Please put a link</b>"
                )
            self.db.set("shizu.info", "pic", args.split()[1])
            return await message.answer(
                "<emoji id=5960603218806312857>🖼</emoji> <b>Info photo has been changed...</b>"
            )

    @loader.command()
    async def wuserbot(self, app: Client, message: types.Message):
        """What is a userbot?"""
        text = """<emoji id=5188377234380954537>🌘</emoji> <b>Userbot</b>

<emoji id=5472238129849048175>😎</emoji> A userbot can be characterized as a <b>third-party software application</b> that engages with the Telegram API in order to execute <b>automated operations on behalf of an end user</b>. These userbots possess the capability to streamline a variety of tasks, encompassing activities such as <b>dispatching messages, enrolling in channels, retrieving media files, and more</b>.

<emoji id=5474667187258006816>😎</emoji> Diverging from conventional Telegram bots, <b>userbots operate within the confines of a user's account</b> rather than within a dedicated bot account. This particular distinction empowers userbots with enhanced accessibility to a broader spectrum of functionalities and a heightened degree of flexibility in executing actions.

<emoji id=5472267631979405211>🚫</emoji> It is imperative to underscore, however, that <b>userbots do not receive official endorsement from the Telegram platform</b>, and their utilization may potentially infringe upon the terms of service established by the platform. Consequently, <b>users are advised to exercise discernment and prudence when deploying userbots</b>, ensuring that their usage remains devoid of any malevolent intent or misconduct.
        """
        await message.answer(text)
