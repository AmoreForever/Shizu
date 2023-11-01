# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru

import logging
import os
import atexit
import sys
import pyrogram
import asyncio
import subprocess
from pyrogram.methods.utilities.idle import idle
from pyrogram import types
from . import auth, database, loader, utils, extrapatchs


async def main():
    """Main function"""

    me, app, tapp = await auth.Auth().authorize()
    await app.initialize()
    db = database.db

    modules = loader.ModulesManager(app, db, me)
    extrapatchs.MessageMagic(types.Message)
    if utils.is_tl_enabled():
        asyncio.ensure_future(tapp.start())
        app.tl = tapp
    else:
        app.tl = "Not enabled"
    await modules.load(app)

    if not db.get("shizu.me", "me", None):
        id_ = (await app.get_me()).id
        db.set("shizu.me", "me", id_)
    if pyrogram.__version__ != "2.0.106.8":
        logging.info("Installing shizu-pyrogram...")
        subprocess.run(
            "pip install https://github.com/AmoreForever/Shizu-Pyro/archive/dev.zip --force-reinstall",
            shell=True,
            check=True,
        )
        logging.info("Successfully installed shizu-pyrogram!")
        logging.info("Restarting...")
        return atexit.register(os.execl(sys.executable, sys.executable, "-m", "shizu"))
    await idle()

    logging.info("Shizu is shutting down...")
    return True
