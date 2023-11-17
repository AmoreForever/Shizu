"""
    █ █ ▀ █▄▀ ▄▀█ █▀█ ▀    ▄▀█ ▀█▀ ▄▀█ █▀▄▀█ ▄▀█
    █▀█ █ █ █ █▀█ █▀▄ █ ▄  █▀█  █  █▀█ █ ▀ █ █▀█

    Copyright 2022 t.me/hikariatama
    Licensed under the GNU GPLv3
"""

# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru


from pyrogram import Client
from .. import loader, utils


@loader.module("ShizuStart", "hikamoru")
class ShizuStart(loader.Module):
    """
    Module doesn't do anything just for notification that Shizu started first time
    """

    text = """
    👋 Hey there! Congratulations on installing the <u>Shizu userbot</u>. Need a hand with anything?

❓ Don't hesitate to reach out to our support chat if you have questions. We're here to assist everyone. @shizu_talks   

🔒 Plus, we've beefed up security to protect against <b>Account Deletion</b>.

💁‍♀️ Let's get you started quickly:

▫️ Just enter <code>.help</code> to see all available modules.
▫️ If you need help with a specific module, try <code>.help (ModuleName/command)</code>.
▫️ Want to grab a module from a link? Easy, just use <code>.dlmod (link)</code>.
▫️ To install a module from a file, reply with <code>.loadmod</code> to the file.
▫️ Deactivate a specific module by using <code>.unloadmod (ModuleName)</code>.
▫️ If you're searching for modules by name, give <code>.aelis (ModuleName)</code> a shot.
▫️ Explore available languages with <code>.langs</code>, and switch your language with <code>.setlang (lang)</code>.

📢 Stay tuned for exciting updates in our channel. Join us at @shizuhub to be the first to know about our latest features.

    """

    async def on_load(self, app: Client):
        mymakr = self.bot._generate_markup(
            [
                [
                    {
                        "text": "📢 Channel",
                        "url": "https://t.me/shizuhub",
                    },
                    {
                        "text": "👥 Support",
                        "url": "https://t.me/shizu_talks",
                    },
                ]
            ]
        )
        if not self.db.get("shizu.me", "notified", None):
            await self._bot.send_animation(
                self.me.id,
                "https://i.gifer.com/Qipy.gif",
                caption=self.text,
                reply_markup=mymakr,
            )
            self.db.set("shizu.me", "notified", True)
