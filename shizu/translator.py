"""
    █ █ ▀ █▄▀ ▄▀█ █▀█ ▀    ▄▀█ ▀█▀ ▄▀█ █▀▄▀█ ▄▀█
    █▀█ █ █ █ █▀█ █▀▄ █ ▄  █▀█  █  █▀█ █ ▀ █ █▀█

    Copyright 2022 t.me/hikariatama
    Licensed under the GNU GPLv3
"""

# Shizu Copyright (C) 2023-2024  AmoreForever

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import json

from . import utils


class Translator:
    def __init__(self, client, db):
        self._client = client
        self.db = db

    async def init(self) -> bool:
        return True

    def getkey(self, key):
        lang = self.db.get("shizu.me", "lang", "en")
        langpack_path = os.path.join(utils.get_base_dir(), f"langpacks/{lang}.json")

        if os.path.isfile(langpack_path):
            with open(langpack_path, "r", encoding="utf-8") as f:
                lang_data = json.load(f)
                return lang_data.get(key, False)

        return False

    def gettext(self, text):
        return self.getkey(text) or text

class Strings:
    def __init__(self, mod, translator, db):
        self._mod = mod
        self._translator = translator
        self._db = db
        self._base_strings = mod.strings

    def __getitem__(self, key: str) -> str:
        return (
            self._translator.getkey(f"{self._mod.__module__}.{key}")
            if self._translator is not None
            else False
        ) or (
            getattr(
                self._mod,
                f"strings_{self._db.get('shizu.me', 'lang', 'en')}",
                self._base_strings,
            )
            if self._translator is not None
            else self._base_strings
        ).get(
            key,
            self._base_strings.get(key, "Unknown strings"),
        )

    def __call__(self, key: str) -> str:
        return self.__getitem__(key)

    def __iter__(self):
        return self._base_strings.__iter__()
