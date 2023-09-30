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
        """Информация о боте"""
        await utils.answer(
            message,
            "https://0x0.st/HOP4.jpg",
            caption=self.text_(message.from_user),
            photo=True
        )