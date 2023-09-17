# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru


from .. import loader, utils
from pyrogram import Client


@loader.module("ShizuStart", "hikamoru")
class ShizuStart(loader.Module):
    """
    Module doesn't do anything just for notification that Shizu started first time
    """

    text = """
    🐙 Hello. You've just installed <u>Shizu userbot</u>.

❓ <b>Need help? Feel free to join our support chat. We help everyone.

📣 We always announce new updates in our channel. Join it to be the first to know about new features: @shizuhub

🛡 And also we have made protection against Account Deletion</b>

💁‍♀️ Quickstart:

1️⃣ Type <code>.help</code> to see modules list
2️⃣ Type <code>.help (ModuleName/command)</code> to see help of module ModuleName
3️⃣ Type <code>.dlmod (link)</code> to load module from link
4️⃣ Type <code>.loadmod</code> with reply to file to install module from it
5️⃣ Type <code>.unloadmod (ModuleName)</code> to unload module ModuleName
    """  # i'm too lazy write this text thos i copied from Hikka

    async def on_load(self, app: Client):
        if not self.db.get("shizu.me", "started", None):
            await self._bot.send_message(self.me.id, self.text)
            self.db.set("shizu.me", "started", True)
