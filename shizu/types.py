# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru

from types import FunctionType
from typing import Any, Dict, List, Union

from . import database

from pyrogram import Client, types


from logging import getLogger

logger = getLogger(__name__)

import asyncio


class Module:
    """Описание модуля"""

    name: str
    author: str
    version: Union[int, float]

    async def on_load(self, app: Client) -> Any:
        """called when loading the module"""


class ModulesManager:
    """Manager of modules"""

    def __init__(self) -> None:
        self.modules: List[Module]
        self.watcher_handlers: List[FunctionType]

        self.command_handlers: Dict[str, FunctionType]
        self.message_handlers: Dict[str, FunctionType]
        self.inline_handlers: Dict[str, FunctionType]
        self.callback_handlers: Dict[str, FunctionType]

        self._local_modules_path: str
        self.me: types.User
        self._db: database.Database

        self.aliases: Dict[str, str]

        self.dp
        self.bot_manager


class StopLoop(Exception):
    """Stops the loop, in which is raised"""


class InfiniteLoop:
    _task = None
    status = False

    def __init__(
        self,
        func: FunctionType,
        interval: int,
        autostart: bool,
        wait_before: bool,
    ):
        self.func = func
        self.interval = interval
        self.autostart = autostart
        self._wait_before = wait_before
        self.module_instance = None
        self._task = None
        if autostart:
            self.start()

    def _stop(self, *args, **kwargs):
        self._wait_for_stop.set()

    async def stop(self, *args, **kwargs) -> bool:
        if self._task:
            logger.info("Stopped loop for method %s", self.func)
            self._wait_for_stop = asyncio.Event()
            self.status = False
            self._task.add_done_callback(self._stop)
            self._task.cancel()
            return await self._wait_for_stop.wait()

        logger.info("Loop is not running")
        return True

    def start(self, *args, **kwargs):
        if not self._task:
            self._task = asyncio.ensure_future(self.actual_loop(*args, **kwargs))
        else:
            logger.info("Attempted to start already running loop")

    async def actual_loop(self, *args, **kwargs):
        self.status = True

        while self.status:
            if self._wait_before:
                await asyncio.sleep(self.interval)

            try:
                await self.func(self.module_instance, *args, **kwargs)
            except StopLoop:
                break
            except Exception:
                logger.exception("Error running loop!")

            if not self._wait_before:
                await asyncio.sleep(self.interval)

        self._wait_for_stop.set()

        self.status = False

    def __del__(self):
        self.stop()
