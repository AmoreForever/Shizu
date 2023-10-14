"""
    █ █ ▀ █▄▀ ▄▀█ █▀█ ▀    ▄▀█ ▀█▀ ▄▀█ █▀▄▀█ ▄▀█
    █▀█ █ █ █ █▀█ █▀▄ █ ▄  █▀█  █  █▀█ █ ▀ █ █▀█

    Copyright 2022 t.me/hikariatama
    Licensed under the GNU GPLv3
"""


# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru

import ast
import contextlib
from .. import loader, utils
from pyrogram.types import Message
import logging
from typing import Union, List

logger = logging.getLogger(__name__)


def chunks(lst: Union[list, tuple, set], n: int) -> List[list]:
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


@loader.module("ShizuConfig", "hikamoru")
class ShizuConfig(loader.Module):
    """Interactive configurator for Shizu"""

    strings = {
        "configure": "⚙️ <b>Here you can configure your modules' configs</b>",
        "configuring_mod": "⚙️ <b>Choose config option for mod</b> <code>{}</code>",
        "configuring_option": "⚙️ <b>Configuring option </b><code>{}</code><b> of mod </b><code>{}</code>\n<i>ℹ️ {}</i>\n\n<b>📔 Default: </b><code>{}</code>\n\n<b>▫️ Current: </b><code>{}</code>",
        "option_saved": "⚙️ <b>Configuring option </b><code>{}</code><b> of mod </b><code>{}</code><b> saved!</b>\n<b>Current: </b><code>{}</code>",
        "back": "⬅️ Back",
        "close": "🚫 Close",
        "enter_value": "✍️ Enter new configuration value for this option",
        "ent_value": "✍️ Enter value",
    }

    strings_ru = {
        "configure": "⚙️ <b>Здесь вы можете настроить конфиги модулей</b>",
        "configuring_mod": "⚙️ <b>Выберите опцию для модуля</b> <code>{}</code>",
        "configuring_option": "⚙️ <b>Настройка опции </b><code>{}</code><b> модуля </b><code>{}</code>\n<i>ℹ️ {}</i>\n\n<b>📔 По умолчанию: </b><code>{}</code>\n\n<b>▫️ Текущее: </b><code>{}</code>",
        "option_saved": "⚙️ <b>Настройка опции </b><code>{}</code><b> модуля </b><code>{}</code><b> сохранена!</b>\n<b>Текущее: </b><code>{}</code>",
        "back": "⬅️ Назад",
        "close": "🚫 Закрыть",
        "enter_value": "✍️ Введите новое значение конфигурации для этой опции",
        "ent_value": "✍️ Введите значение",
    }

    strings_uz = {
        "configure": "⚙️ <b>Bu erda modullaringizning konfiguratsiyasini sozlash mumkin</b>",
        "configuring_mod": "⚙️ <b>Mod uchun konfiguratsiya variantini tanlang</b> <code>{}</code>",
        "configuring_option": "⚙️ <b>Mod </b><code>{}</code><b> uchun konfiguratsiya variantini tanlang</b><code>{}</code>\n<i>ℹ️ {}</i>\n\n<b>📔 Standart: </b><code>{}</code>\n\n<b>▫️ Hozirgi: </b><code>{}</code>",
        "option_saved": "⚙️ <b>Mod </b><code>{}</code><b> uchun konfiguratsiya varianti saqlandi!</b>\n<b>Hozirgi: </b><code>{}</code>",
        "back": "⬅️ Orqaga",
        "close": "🚫 Yopish",
        "enter_value": "✍️ Ushbu variant uchun yangi konfiguratsiya qiymatini kiriting",
        "ent_value": "✍️ Qiymatni kiriting",
    }

    strings_jp = {
        "configure": "⚙️ <b>ここでは、モジュールの設定を変更できます</b>",
        "configuring_mod": "⚙️ <b>モジュールの設定オプションを選択</b> <code>{}</code>",
        "configuring_option": "⚙️ <b>モジュール </b><code>{}</code><b> の設定オプションを選択</b><code>{}</code>\n<i>ℹ️ {}</i>\n\n<b>📔 デフォルト: </b><code>{}</code>\n\n<b>▫️ 現在: </b><code>{}</code>",
        "option_saved": "⚙️ <b>モジュール </b><code>{}</code><b> の設定オプションが保存されました！</b>\n<b>現在: </b><code>{}</code>",
        "back": "⬅️ 戻る",
        "close": "🚫 閉じる",
        "enter_value": "✍️ このオプションの新しい設定値を入力してください",
        "ent_value": "✍️ 値を入力",
    }

    strings_ua = {
        "configure": "⚙️ <b>Тут ви можете налаштувати конфіги модулів</b>",
        "configuring_mod": "⚙️ <b>Виберіть опцію для модуля</b> <code>{}</code>",
        "configuring_option": "⚙️ <b>Налаштування опції </b><code>{}</code><b> модуля </b><code>{}</code>\n<i>ℹ️ {}</i>\n\n<b>📔 За замовчуванням: </b><code>{}</code>\n\n<b>▫️ Поточне: </b><code>{}</code>",
        "option_saved": "⚙️ <b>Налаштування опції </b><code>{}</code><b> модуля </b><code>{}</code><b> збережено!</b>\n<b>Поточне: </b><code>{}</code>",
        "back": "⬅️ Назад",
        "close": "🚫 Закрити",
        "enter_value": "✍️ Введіть нове значення конфігурації для цієї опції",
        "ent_value": "✍️ Введіть значення",
    }

    strings_kz = {
        "configure": "⚙️ <b>Мұнда модульдерді конфигурациялауға болады</b>",
        "configuring_mod": "⚙️ <b>Модуль үшін конфиг опциясын таңдаңыз</b> <code>{}</code>",
        "configuring_option": "⚙️ <b>Модуль </b><code>{}</code><b> үшін конфиг опциясын таңдаңыз</b><code>{}</code>\n<i>ℹ️ {}</i>\n\n<b>📔 Әдепкі: </b><code>{}</code>\n\n<b>▫️ Ағымдағы: </b><code>{}</code>",
        "option_saved": "⚙️ <b>Модуль </b><code>{}</code><b> үшін конфиг опциясы сақталды!</b>\n<b>Ағымдағы: </b><code>{}</code>",
        "back": "⬅️ Артқа",
        "close": "🚫 Жабу",
        "enter_value": "✍️ Осы опция үшін жаңа конфигурация мәнін енгізіңіз",
        "ent_value": "✍️ Мәнді енгізіңіз",
    }

    async def inline__close(self, call: "aiogram.types.CallbackQuery") -> None:
        await call.delete()

    async def inline__set_config(
        self,
        call: "aiogram.types.CallbackQuery",
        query: str,
        mod: str,
        option: str,
        inline_message_id: str,
    ) -> None:
        with contextlib.suppress(Exception):
            for module in self.all_modules.modules:
                if module.name == mod:
                    module.config[option] = query
                    if query:
                        with contextlib.suppress(ValueError, SyntaxError):
                            query = ast.literal_eval(query)
                        self.db.set(
                            module.__class__.__name__,
                            "__config__",
                            {option: query},
                        )
                    else:
                        with contextlib.suppress(KeyError):
                            self.db.pop(module.__class__.__name__, "__config__")

                self.reconfmod(module, self.db)
                self.db.save()

        await call.edit(
            self.strings("option_saved").format(mod, option, query),
            reply_markup=[
                [
                    {
                        "text": self.strings("back"),
                        "callback": self.inline__configure,
                        "args": (mod,),
                    },
                    {"text": self.strings("close"), "callback": self.inline__close},
                ]
            ],
            inline_message_id=inline_message_id,
        )

    async def inline__configure_option(
        self, call: "aiogram.types.CallbackQuery", mod: str, config_opt: str
    ) -> None:
        for module in self.all_modules.modules:
            if module.name == mod:
                await call.edit(
                    self.strings("configuring_option").format(
                        utils.escape_html(config_opt),
                        utils.escape_html(mod),
                        utils.escape_html(module.config.getdoc(config_opt)),
                        utils.escape_html(module.config.getdef(config_opt)),
                        utils.escape_html(module.config[config_opt]),
                    ),
                    reply_markup=[
                        [
                            {
                                "text": self.strings("ent_value"),
                                "input": self.strings("enter_value"),
                                "handler": self.inline__set_config,
                                "args": (mod, config_opt, call.inline_message_id),
                            }
                        ],
                        [
                            {
                                "text": self.strings("back"),
                                "callback": self.inline__configure,
                                "args": (mod,),
                            },
                            {
                                "text": self.strings("close"),
                                "callback": self.inline__close,
                            },
                        ],
                    ],
                )

    async def inline__configure(
        self, call: "aiogram.types.CallbackQuery", mod: str
    ) -> None:
        btns = []
        with contextlib.suppress(Exception):
            for module in self.all_modules.modules:
                if module.name == mod:
                    for param in module.config:
                        btns += [
                            {
                                "text": param,
                                "callback": self.inline__configure_option,
                                "args": (mod, param),
                            }
                        ]
        await call.edit(
            self.strings("configuring_mod").format(utils.escape_html(mod)),
            reply_markup=list(chunks(btns, 2))
            + [
                [
                    {
                        "text": self.strings("back"),
                        "callback": self.inline__global_config,
                    },
                    {"text": self.strings("close"), "callback": self.inline__close},
                ]
            ],
        )

    async def inline__global_config(
        self, call: Union[Message, "aiogram.types.CallbackQuery"]
    ) -> None:
        to_config = [
            mod.name for mod in self.all_modules.modules if hasattr(mod, "config")
        ]
        kb = []
        for mod_row in chunks(to_config, 3):
            row = [
                {"text": btn, "callback": self.inline__configure, "args": (btn,)}
                for btn in mod_row
            ]
            kb += [row]

        kb += [[{"text": self.strings("close"), "callback": self.inline__close}]]

        if isinstance(call, Message):
            await call.answer(self.strings("configure"), reply_markup=kb)
        else:
            await call.edit(self.strings("configure"), reply_markup=kb)

    async def configcmd(self, app, message: Message) -> None:
        """Configure modules"""
        await self.inline__global_config(message)

    async def watcher(self, app, message: Message) -> None:
        if (
            not getattr(message, "via_bot", False)
            or message.via_bot.id != (await self.bot.bot.get_me()).id
            or "This message is gonna be deleted..." not in getattr(message, "text", "")
        ):
            return

        await message.delete()
