# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru


from .. import loader, utils
import logging
from pyrogram import types, Client
from pyrogram.raw.base.help import UserInfo


logger = logging.getLogger('Security')


@loader.module("ShizuSecurity", "shizu")
class ShizuSecurityMod(loader.Module):
    """This is in order to give the owner the right to manage the bot"""

    @loader.command()
    async def addowner(self, app: Client, message: types.Message):
        """Give out the owner - a replay of the user's message"""
        reply = message.reply_to_message
        users = self.db.get("shizu.me", "owners", [])
        if not reply:
            return await message.edit("There is no reply to the user's message")
        if reply.from_user.id == (await app.get_me()).id:
            return await message.edit("You can't give ownership to yourself")
        if reply.from_user.id in users:
            return await message.edit("This user is already an owner")
        users.append(reply.from_user.id)
        self.db.set("shizu.me", "owners", users)
        await utils.answer(
            message,
            f"<emoji id=5467406098367521267>👑</emoji> Congratulations, {reply.from_user.mention} is now an owner",
        )

    @loader.command()
    async def delowner(self, app: Client, message: types.Message):
        """Del the owner - a replay of the user's message"""
        reply = message.reply_to_message
        users = self.db.get("shizu.me", "owners", [])
        if not reply:
            return await utils.answer(
                message, "There is no reply to the user's message"
            )
        if reply.from_user.id == (await app.get_me()).id:
            return await utils.answer(
                message, "You can't remove yourself from the owner list"
            )
        if reply.from_user.id not in users:
            return await utils.answer(message, "This user is not an owner")
        users.remove(reply.from_user.id)
        self.db.set("shizu.me", "owners", users)
        await utils.answer(
            message,
            f"<emoji id=5021905410089550576>✅</emoji> Unfortunately, {reply.from_user.mention} is no longer an owner",
        )
        
    @loader.command()
    async def ownerslist(self, app: Client, message: types.Message):
        """List of owners"""
        if owners := self.db.get("shizu.me", "owners", []):
            await utils.answer(
                message,
                "👑 List of owners:\n"+ "\n".join(  
                    f"<code>{owner}</code>"
                    for owner in owners
                ),
                )
        else:
            return await utils.answer(message, "There is no owner")