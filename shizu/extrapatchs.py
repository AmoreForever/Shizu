# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru

import loguru
from .utils import (
    answer,
    answer_eor,
    get_args,
    get_args_raw,
    get_args_html,
)

logger = loguru.logger


class MessageMagic:
    def __init__(self, message) -> None:
        self.message = message
        self._init_msg()

    def _init_msg(self):
        try:
            self.message.answer = answer
            self.message.answer_eor = answer_eor
            self.message.get_args = get_args
            self.message.get_args_raw = get_args_raw
            self.message.get_args_html = get_args_html
            logger.success("MessageMagic initialized")
        except Exception as e:
            logger.error(f"Error initializing MessageMagic: {str(e)}")


