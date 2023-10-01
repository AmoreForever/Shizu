# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru


import logging
import requests
import traceback
import os
import typing
import contextlib
import json
import html
import re
import time


from typing import Union
from aiogram.utils.exceptions import NetworkError
from loguru._better_exceptions import ExceptionFormatter
from loguru._colorizer import Colorizer
from loguru import logger

from .database import db

FORMAT_FOR_FILES = "[{level}] {name}: {message}"

FORMAT_FOR_TGLOG = logging.Formatter(
    fmt="[%(levelname)s] %(name)s: %(message)s",
    datefmt=None,
    style="%",
)


def get_valid_level(level: Union[str, int]):
    return int(level) if level.isdigit() else getattr(logging, level.upper(), None)


def send_message(message: str, chat_id: int):
    with contextlib.suppress(NetworkError):
        requests.post(
            f"https://api.telegram.org/bot{db.get('shizu.bot', 'token')}/sendMessage",
            data={"chat_id": chat_id, "text": message, "parse_mode": "HTML"},
            timeout=10,
        )


class CustomException:
    def __init__(
        self,
        message: str,
        local_vars: str,
        full_stack: str,
        sysinfo: typing.Optional[
            typing.Tuple[object, Exception, traceback.TracebackException]
        ] = None,
    ):
        self.message = message
        self.local_vars = local_vars
        self.full_stack = full_stack
        self.sysinfo = sysinfo
        self.debug_url = None

    @classmethod
    def from_exc_info(
        cls, exc_type: object, exc_value: Exception, tb: traceback.TracebackException
    ) -> "CustomException":
        def to_hashable(dictionary: dict) -> dict:
            dictionary = dictionary.copy()
            for key, value in dictionary.items():
                if isinstance(value, dict):
                    dictionary[key] = to_hashable(value)
                else:
                    try:
                        if (
                            getattr(getattr(value, "__class__", None), "__name__", None)
                            == "Database"
                        ):
                            dictionary[key] = "<Database>"
                        elif len(str(value)) > 512:
                            dictionary[key] = f"{str(value)[:512]}..."
                        else:
                            dictionary[key] = str(value)
                    except Exception:
                        dictionary[key] = f"<{value.__class__.__name__}>"

            return dictionary

        full_stack = traceback.format_exc().replace(
            "Traceback (most recent call last):\n", ""
        )

        line_regex = r'  File "(.*?)", line ([0-9]+), in (.+)'

        def format_line(line: str) -> str:
            filename_, lineno_, name_ = re.search(line_regex, line).groups()
            with contextlib.suppress(Exception):
                filename_ = os.path.basename(filename_)

            return (
                f"👉 <code>{html.escape(filename_)}:{lineno_}</code> <b>in</b>"
                f" <code>{html.escape(name_)}</code>"
            )

        filename, lineno, name = next(
            (
                re.search(line_regex, line).groups()
                for line in reversed(full_stack.splitlines())
                if re.search(line_regex, line)
            ),
            (None, None, None),
        )

        full_stack = "\n".join(
            [
                format_line(line)
                if re.search(line_regex, line)
                else f"<code>{html.escape(line)}</code>"
                for line in full_stack.splitlines()
            ]
        )

        with contextlib.suppress(Exception):
            filename = os.path.basename(filename)

        return CustomException(
            message=override_text(exc_value)
            or (
                f"<b>🗄 Where:</b>  "
                f"<code>{html.escape(filename)}:{lineno}</code>"
                f"<b>in </b><code>{html.escape(name)}</code>\n<b>❓ What:</b>"
                f" <code>{html.escape(''.join(traceback.format_exception_only(exc_type, exc_value)).strip())}</code>"
            ),
            local_vars=(
                f"<code>{html.escape(json.dumps(to_hashable(tb.tb_frame.f_locals), indent=4))}</code>"
            ),
            full_stack=full_stack,
            sysinfo=(exc_type, exc_value, tb),
        )


class StreamHandler(logging.Handler):
    """Обработчик логирования в поток"""

    def __init__(self, lvl: int = logging.INFO):
        super().__init__(lvl)

    def format(self, record: logging.LogRecord):
        """Форматирует логи под нужный формат"""
        exception_lines = ""
        stripped_formatter = Colorizer.prepare_format(
            FORMAT_FOR_FILES + "{exception}"
        ).strip()

        if record.exc_info:
            exception_formatter = ExceptionFormatter(
                encoding="utf-8",
                backtrace=True,
                prefix="\n",
                hidden_frames_filename=logger.catch.__code__.co_filename,
            )

            type_, value, tb = record.exc_info
            exception_list = exception_formatter.format_exception(type_, value, tb)
            exception_lines = "".join(exception_list)

        return stripped_formatter.format(
            level=record.levelname,
            name=record.name,
            function=record.funcName,
            message=record.msg,
            exception=exception_lines,
        )


class MemoryHandler(logging.Handler):
    """Memory Logging handler"""

    def __init__(self, lvl: int = logging.INFO):
        super().__init__(0)
        self.target = StreamHandler(lvl)
        self.lvl = lvl

        self.capacity = 500
        self.buffer = []
        self.handled_buffer = []

    def dumps(self, lvl: int):
        """Returns a list of all incoming logs by minimum level"""
        sorted_logs = list(
            filter(lambda record: record.levelno >= lvl, self.handled_buffer)
        )
        self.handled_buffer = list(set(self.handled_buffer) ^ set(sorted_logs))
        return map(self.target.format, sorted_logs)

    def emit(self, record: logging.LogRecord):
        """Emit a log record"""
        if len(self.buffer + self.handled_buffer) >= self.capacity:
            if self.handled_buffer:
                del self.handled_buffer[0]
            else:
                del self.buffer[0]

        self.buffer.append(record)
        if record.levelno >= self.lvl >= 0:
            self.acquire()
            try:
                self.dop_log(record)
            finally:
                self.release()

    def dop_log(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )

        self.handled_buffer = (
            self.handled_buffer[-(self.capacity - len(self.buffer)) :] + self.buffer
        )
        self.buffer = []


class Telegramhandler(logging.Handler):
    """Logging handler for telegram"""

    def __init__(self, lvl: int = logging.INFO):
        super().__init__(lvl)
        self.target = StreamHandler(lvl)
        self.lvl = lvl
        self.capacity = 500
        self.buffer = []
        self.handled_buffer = []
        self.msgs = []
        self.token = db.get("shizu.bot", "token")
        self.chat = db.get("shizu.chat", "logs")
        self.last_log_time = None
        self.time_threshold = 1

    def dumps(self, lvl: int):
        """Returns a list of all incoming logs by minimum level"""
        sorted_logs = list(
            filter(lambda record: record.levelno >= lvl, self.handled_buffer)
        )
        self.handled_buffer = list(set(self.handled_buffer) ^ set(sorted_logs))
        return map(self.target.format, sorted_logs)

    def emit(self, record: logging.LogRecord):
        current_time = time.time()

        if self.last_log_time is None:
            self.last_log_time = current_time

        self.msgs.append(f"<code>{FORMAT_FOR_TGLOG.format(record)}</code>")

        if current_time - self.last_log_time >= self.time_threshold and self.msgs:
            send_message("\n".join(self.msgs), self.chat)
            self.msgs.clear()
            self.last_log_time = current_time


def override_text(exception: Exception) -> typing.Optional[str]:
    """Returns error-specific description if available, else `None`"""
    if isinstance(exception, NetworkError):
        return "✈️ <b>You have problems with internet connection on your server.</b>"

    return None


def setup_logger(level: Union[str, int]):
    """Setup logger"""

    level = get_valid_level(level) or 20
    handler = MemoryHandler(level)
    tg = Telegramhandler(level)
    logging.getLogger().addHandler(tg)
    logging.basicConfig(handlers=[handler, tg], level=level, force=True)

    for ignore in [
        "pyrogram.session",
        "pyrogram.connection",
        "pyrogram.methods.utilities.idle",
    ]:
        logger.disable(ignore)
    logging.captureWarnings(True)
