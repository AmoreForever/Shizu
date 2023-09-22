# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru

import git
import os
import atexit
import sys
from .. import utils, loader, version
from pyrogram import Client
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery



@loader.module("ShizuNotificator", "hikamoru")
class ShizuNotificator(loader.Module):
    """Notify about new commits in the repo by sending a message to the bot """
    
    strings = {
        'more': "<b>... and more {}</b>",
        'update_required': "🆕 <b>Shizu Update available!</b>\n\nNew Shizu version released.\n🔮 <b>Shizu <s>{}</s> -> {}</b>\n\n{}",
        'updaing': "🔄 Updating...",
    }
    _notified = None
    
    def update_keyboard(self):
        markup = InlineKeyboardMarkup()
        upd = InlineKeyboardButton("🔄 Update", callback_data="update")
        markup.add(upd)
        return markup
    
    
    def get_changelog(self) -> str:
        try:
            repo = git.Repo()

            for remote in repo.remotes:
                remote.fetch()

            if not (
                diff := repo.git.log([f"HEAD..origin/{version.branch}", "--oneline"])
            ):
                return False
        except Exception:
            return False

        res = "\n".join(
            f"<b>{commit.split()[0]}</b>:"
            f" <i>{utils.escape_html(' '.join(commit.split()[1:]))}</i>"
            for commit in diff.splitlines()[:10]
        )

        if diff.count("\n") >= 10:
            res += self.strings["more"].format(len(diff.splitlines()) - 10)

        return res
    
    def get_latest(self) -> str:
        try:
            return next(
                git.Repo().iter_commits(f"origin/{version.branch}", max_count=1)
            ).hexsha
        except Exception:
            return ""
        
    @loader.on_bot(lambda self, app, call: call.data == "update")
    async def update_callback_handler(self, app: Client, call: CallbackQuery):
        await self.bot.bot.send_message(
            self.tg_id,
            self.strings["updaing"]
            )
        os.system("git pull")
        await self.bot.bot.send_message(
            self.tg_id,
            '🧑‍🔬 Restart...'
        )
        
        atexit.register(os.execl(sys.executable, sys.executable, "-m", "shizu"))
        return sys.exit(0)
        
    @loader.loop(interval=20, autostart=True)
    async def check_updst(self) -> None:
        self._pending = self.get_latest()
        if self._pending not in {utils.get_git_hash(), self._notified}:
            await self.bot.bot.send_animation(
                self.tg_id,
                "https://t.me/hikamoru_assets/28",
                caption=self.strings["update_required"].format(
                    utils.get_git_hash()[:6],
                    f'<a href="https://github.com/AmoreForever/Shizu/compare/{utils.get_git_hash()[:12]}...{self.get_latest()[:12]}">{self.get_latest()[:6]}</a>',
                    self.get_changelog(),
                ),
                reply_markup=self.update_keyboard(),
            )

            self._notified = self._pending
            self.db.set("ignore_permanent", False)