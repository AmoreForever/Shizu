# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru

import contextlib
import logging
import time
import os
import atexit
import sys
import pyrogram
from pyrogram.methods.utilities.idle import idle
from pyrogram import types
import subprocess
from . import auth, database, loader, utils, extrapatchs
from .bot import core
from .translater import Translator


async def main():
    """Main function"""
    me, app = await auth.Auth().authorize()
    await app.initialize()
    db = database.db
    modules = loader.ModulesManager(app, db, me)
    extrapatchs.MessageMagic(types.Message)
    tr = Translator(app, db)

    await modules.load(app)
    await tr.init()
    with contextlib.suppress(Exception):
        app.inline_bot = core.bot
        app.bot = modules.bot_manager.bot
    me = db.get("shizu.me", "me", None)

    if not me:
        id_ = (await app.get_me()).id
        db.set("shizu.me", "me", id_)
    if pyrogram.__version__ != "2.0.112":
        logging.info("Installing shizu-pyrogram...")
        subprocess.run(
            "pip install https://github.com/AmoreForever/pyrogram/archive/dev.zip --force-reinstall",
            shell=True,
            check=True,
        )
        logging.info("Successfully installed shizu-pyrogram!")
        logging.info("Restarting...")
        return atexit.register(os.execl(sys.executable, sys.executable, "-m", "shizu"))
    await idle()

    logging.info("Shizu is shutting down...")
    return True
