# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru

import logging
import requests

from . import utils

logger = logging.getLogger(__name__)


class Translator:
    def __init__(self, client, db):
        self._client = client
        self.db = db

    async def init(self) -> bool:
        self._data = {}
        if lang := self.db.get("shizu.me", "lang", False):
            for language in lang.split(" "):
                if utils.check_url(language):
                    try:
                        ndata = (await utils.run_sync(requests.get, language)).json()
                    except Exception:
                        logger.exception(f"Unable to decode {language}")
                        continue

                    data = ndata.get("data", ndata)

                    if all(isinstance(i, str) for i in data.values()):
                        self._data |= data

        return bool(self._data)

    def getkey(self, key):
        return self._data.get(key, False)

    def gettext(self, text):
        return self.getkey(text) or text


class Strings:
    def __init__(self, mod, translator, db):
        self._mod = mod
        self._translator = translator
        self._db = db
        self._base_strings = mod.strings

    def __getitem__(self, key: str) -> str:
        current_language = self._db.get("shizu.me", "lang", "en")
        supported_languages = ["en", "ru", "uz", "jp"]

        for lang in supported_languages:
            strings_dict_name = f"strings_{lang}"
            if (
                current_language == lang
                and hasattr(self._mod, strings_dict_name)
                and isinstance(getattr(self._mod, strings_dict_name), dict)
                and key in getattr(self._mod, strings_dict_name)
            ):
                return getattr(self._mod, strings_dict_name)[key]

        return self._base_strings.get(key, "Unknown strings")

    def __call__(self, key: str) -> str:
        return self.__getitem__(key)

    def __iter__(self):
        return self._base_strings.__iter__()
