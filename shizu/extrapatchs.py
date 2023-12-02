# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru

import logging
from .utils import (
    answer,
    get_args,
    get_args_raw,
    get_args_html,
)


logging = logging.getLogger(__name__)


class MessageMagic:
    def __init__(self, message) -> None:
        self.message = message
        self._init_msg()

    def _init_msg(self):
        """
        Initializes the `message` object with various methods and attributes.

        Parameters:
            None

        Returns:
            None

        Raises:
            Exception: If there is an error initializing the `MessageMagic` module.

        Side Effects:
            Sets the `answer` attribute of the `message` object.
            Sets the `get_args` attribute of the `message` object.
            Sets the `get_args_raw` attribute of the `message` object.
            Sets the `get_args_html` attribute of the `message` object.
            Logs a success message if initialization is successful.
            Logs an error message if there is an error initializing `MessageMagic`.
        """
        try:
            self.message.answer = answer
            self.message.get_args = get_args
            self.message.get_args_raw = get_args_raw
            self.message.get_args_html = get_args_html

        except Exception as e:
            logging.error(f"Error initializing MessageMagic: {str(e)}")
