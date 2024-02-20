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

import ast
import contextlib
import logging

from typing import Union
from pyrogram.types import Message

from .. import loader, utils

logger = logging.getLogger(__name__)


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
        "restore_def_button": "🦖 Restore default",
        "restored": "🦖 <b>Configurations restored to default!</b>",
        "advanced_button": "🔧 Advanced",
        "advanced": "⚙️ <b>Advanced configuration of module <code>{}</code></b>",
        "true_false_button": "📟 True/False",
        "true_false": "⚙️ <b>Choose True or False</b>",
        "add_value_to_list_button": "➕ Add value to list",
        "remove_value_from_list_button": "➖ Remove value from list",
        "true": "✅ True",
        "false": "❌ False",
        "add_delete_button": "🔌 Add/Delete",
        "option_added": "⚙️ <b>Option </b><code>{}</code><b> added!</b>",
        "option_removed": "⚙️ <b>Option </b><code>{}</code><b> removed!</b>",
        "choose_button": "🎛 Choose",
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
        "restore_def_button": "🦖 Восстановить по умолчанию",
        "restored": "🦖 <b>Конфигурации восстановлены по умолчанию!</b>",
        "advanced_button": "🔧 Расширенный",
        "advanced": "⚙️ <b>Расширенная конфигурация модуля <code>{}</code></b>",
        "true_false_button": "📟 True/False",
        "true_false": "⚙️ <b>Выберите True или False</b>",
        "add_delete": "⚙️ <b>Значение для списка</b>",
        "add_value_to_list_button": "➕ Добавить значение в список",
        "remove_value_from_list_button": "➖ Удалить значение из списка",
        "true": "✅ True",
        "false": "❌ False",
        "add_delete_button": "🔌 Добавить/Удалить",
        "option_added": "⚙️ <b>Опция </b><code>{}</code><b> добавлена!</b>",
        "option_removed": "⚙️ <b>Опция </b><code>{}</code><b> удалена!</b>",
        "choose_button": "🎛 Выбрать",
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
        "restore_def_button": "🦖 Standartga tiklash",
        "restored": "🦖 <b>Konfiguratsiya standartga tiklandi!</b>",
        "advanced_button": "🔧 Kengaytirilgan",
        "advanced": "⚙️ <b>Modul <code>{}</code> kengaytirilgan konfiguratsiyasi</b>",
        "true_false_button": "📟 True/False",
        "true_false": "⚙️ <b>True yoki False ni tanlang</b>",
        "add_value_to_list_button": "➕ Ro'yxatga qiymat qo'shing",
        "remove_value_from_list_button": "➖ Ro'yxatdan qiymatni olib tashlang",
        "true": "✅ True",
        "false": "❌ False",
        "add_delete": "⚙️ <b>Ro'yxat uchun qiymat</b>",
        "add_delete_button": "🔌 Qo'shish/Olib tashlash",
        "option_added": "⚙️ <b>Varianta </b><code>{}</code><b> qo'shildi!</b>",
        "option_removed": "⚙️ <b>Varianta </b><code>{}</code><b> olib tashlandi!</b>",
        "choose_button": "🎛 Tanlash",
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
        "restore_def_button": "🦖 デフォルトに戻す",
        "restored": "🦖 <b>設定がデフォルトに戻されました！</b>",
        "advanced_button": "🔧 詳細-",
        "advanced": "⚙️ <b>モジュール <code>{}</code> の詳細設定</b>",
        "true_false_button": "📟 True/False",
        "true_false": "⚙️ <b>True または False を選択</b>",
        "add_value_to_list_button": "➕ リストに値を追加",
        "remove_value_from_list_button": "➖ リストから値を削除",
        "true": "✅ True",
        "false": "❌ False",
        "add_delete": "⚙️ <b>リストの値</b>",
        "add_delete_button": "🔌 追加/削除",
        "option_added": "⚙️ <b>オプション </b><code>{}</code><b> が追加されました！</b>",
        "option_removed": "⚙️ <b>オプション </b><code>{}</code><b> が削除されました！</b>",
        "choose_button": "🎛 選択",
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
        "restore_def_button": "🦖 Відновити за замовчуванням",
        "restored": "🦖 <b>Конфігурації відновлено за замовчуванням!</b>",
        "advanced_button": "🔧 Розширений",
        "advanced": "⚙️ <b>Розширена конфігурація модуля <code>{}</code></b>",
        "true_false_button": "📟 True/False",
        "true_false": "⚙️ <b>Виберіть True або False</b>",
        "add_value_to_list_button": "➕ Додати значення до списку",
        "remove_value_from_list_button": "➖ Видалити значення зі списку",
        "true": "✅ True",
        "false": "❌ False",
        "add_delete": "⚙️ <b>Значення для списку</b>",
        "add_delete_button": "🔌 Додати/Видалити",
        "option_added": "⚙️ <b>Опція </b><code>{}</code><b> додана!</b>",
        "option_removed": "⚙️ <b>Опція </b><code>{}</code><b> видалена!</b>",
        "choose_button": "🎛 Вибрати",
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
        "restore_def_button": "🦖 Әдепкіге қайта орнату",
        "restored": "🦖 <b>Конфигурация әдепкіге қайтарылды!</b>",
        "advanced_button": "🔧 Кеңейтілген",
        "advanced": "⚙️ <b>Модуль <code>{}</code> кеңейтілген конфигурациясы</b>",
        "true_false_button": "📟 True/False",
        "true_false": "⚙️ <b>True не False таңдаңыз</b>",
        "add_value_to_list_button": "➕ Тізімге мән қосу",
        "remove_value_from_list_button": "➖ Тізімнен мәнді алып тастау",
        "true": "✅ True",
        "false": "❌ False",
        "add_delete": "⚙️ <b>Тізім үшін мән</b>",
        "add_delete_button": "🔌 Қосу/Алып тастау",
        "option_added": "⚙️ <b>Опция </b><code>{}</code><b> қосылды!</b>",
        "option_removed": "⚙️ <b>Опция </b><code>{}</code><b> алып тасталды!</b>",
        "choose_button": "🎛 Таңдау",
    }

    strings_kr = {
        "configure": "⚙️ <b>여기에서 모듈의 구성을 구성할 수 있습니다</b>",
        "configuring_mod": "⚙️ <b>모듈의 구성 옵션을 선택</b> <code>{}</code>",
        "configuring_option": "⚙️ <b>모듈 </b><code>{}</code><b> 의 구성 옵션을 선택</b><code>{}</code>\n<i>ℹ️ {}</i>\n\n<b>📔 기본값: </b><code>{}</code>\n\n<b>▫️ 현재: </b><code>{}</code>",
        "option_saved": "⚙️ <b>모듈 </b><code>{}</code><b> 의 구성 옵션이 저장되었습니다!</b>\n<b>현재: </b><code>{}</code>",
        "back": "⬅️ 뒤로",
        "close": "🚫 닫기",
        "enter_value": "✍️ 이 옵션에 대한 새 구성 값을 입력하십시오",
        "ent_value": "✍️ 값을 입력하십시오",
        "restore_def_button": "🦖 기본값으로 복원",
        "restored": "🦖 <b>구성이 기본값으로 복원되었습니다!</b>",
        "advanced_button": "🔧 고급",
        "advanced": "⚙️ <b>모듈 <code>{}</code> 고급 구성</b>",
        "true_false_button": "📟 True/False",
        "true_false": "⚙️ <b>True 또는 False 선택</b>",
        "add_value_to_list_button": "➕ 목록에 값 추가",
        "remove_value_from_list_button": "➖ 목록에서 값 제거",
        "true": "✅ True",
        "false": "❌ False",
        "add_delete": "⚙️ <b>목록 값</b>",
        "add_delete_button": "🔌 추가/제거",
        "option_added": "⚙️ <b>옵션 </b><code>{}</code><b> 추가되었습니다!</b>",
        "option_removed": "⚙️ <b>옵션 </b><code>{}</code><b> 제거되었습니다!</b>",
        "choose_button": "🎛 선택",
    }

    async def inline__close(self, call: "aiogram.types.CallbackQuery") -> None:
        await call.delete()

    async def inline__set_to_default(
        self,
        call: "aiogram.types.CallbackQuery",
        mod: str,
        option: str,
        inline_message_id: str,
    ) -> None:
        for module in self.all_modules.modules:
            if module.name == mod:
                with contextlib.suppress(KeyError):
                    del self.db.setdefault(module.name, {}).setdefault(
                        "__config__", {}
                    )[option]
                self.reconfmod(module, self.db)
                self.db.save()

        await call.edit(
            self.strings("restored"),
            reply_markup=[
                [
                    {
                        "text": self.strings("back"),
                        "callback": self.inline__configure_option,
                        "args": (mod, option),
                    },
                    {"text": self.strings("close"), "callback": self.inline__close},
                ]
            ],
            inline_message_id=inline_message_id,
        )

    async def inline__set_config(
        self,
        call: "aiogram.types.CallbackQuery",
        query: str,
        mod: str,
        option: str,
        inline_message_id: str,
    ) -> None:
        with contextlib.suppress(ValueError, SyntaxError):
            query = ast.literal_eval(query)

        for module in self.all_modules.modules:
            if module.name == mod:
                if query:
                    self.db.setdefault(module.name, {}).setdefault("__config__", {})[
                        option
                    ] = query
                    module.config[option] = query
                else:
                    with contextlib.suppress(KeyError):
                        del self.db.setdefault(module.name, {}).setdefault(
                            "__config__", {}
                        )[option]

            self.reconfmod(module, self.db)
            self.db.save()

        await call.edit(
            self.strings("option_saved").format(mod, option, query),
            reply_markup=[
                [
                    {
                        "text": self.strings("back"),
                        "callback": self.inline__configure_option,
                        "args": (mod, option),
                    },
                    {"text": self.strings("close"), "callback": self.inline__close},
                ]
            ],
            inline_message_id=inline_message_id,
        )

    async def inline__add_item(
        self,
        call: "aiogram.types.CallbackQuery",
        query: str,
        mod: str,
        option: str,
        inline_message_id: str,
    ) -> None:
        with contextlib.suppress(ValueError, SyntaxError):
            query = ast.literal_eval(query)

        for module in self.all_modules.modules:
            if module.name == mod:
                try:
                    self.db.setdefault(module.name, {}).setdefault("__config__", {})[
                        option
                    ] += [query]

                except KeyError:
                    self.db.setdefault(module.name, {}).setdefault("__config__", {})[
                        option
                    ] = module.config[option] + [query]

                self.reconfmod(module, self.db)
                self.db.save()

        await call.edit(
            self.strings("option_added").format(query),
            reply_markup=[
                [
                    {
                        "text": self.strings("back"),
                        "callback": self.inline__add_delete,
                        "args": (mod, option),
                    },
                    {"text": self.strings("close"), "callback": self.inline__close},
                ]
            ],
            inline_message_id=inline_message_id,
        )

    async def inline__remove_item(
        self,
        call: "aiogram.types.CallbackQuery",
        query: str,
        mod: str,
        option: str,
        inline_message_id: str,
    ) -> None:
        with contextlib.suppress(ValueError, SyntaxError):
            query = ast.literal_eval(query)

        for module in self.all_modules.modules:
            if module.name == mod:
                try:
                    self.db.setdefault(module.name, {}).setdefault("__config__", {})[
                        option
                    ].remove(query)

                except KeyError:
                    self.db.setdefault(module.name, {}).setdefault("__config__", {})[
                        option
                    ] = module.config[option].remove(query)

                self.reconfmod(module, self.db)
                self.db.save()

        await call.edit(
            self.strings("opeion_removed").format(query),
            reply_markup=[
                [
                    {
                        "text": self.strings("back"),
                        "callback": self.inline__add_delete,
                        "args": (mod, option),
                    },
                    {"text": self.strings("close"), "callback": self.inline__close},
                ]
            ],
            inline_message_id=inline_message_id,
        )

    async def inline__true_false(
        self, call: "aiogram.types.CallbackQuery", mod: str, config_opt: str
    ) -> None:
        for module in self.all_modules.modules:
            if module.name == mod:
                if isinstance(module.config[config_opt], bool):
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
                                    "text": self.strings("false")
                                    if module.config[config_opt]
                                    else self.strings("true"),
                                    "callback": self.inline__true_false_set,
                                    "args": (
                                        not module.config[config_opt],
                                        mod,
                                        config_opt,
                                        call.inline_message_id,
                                    ),
                                }
                            ],
                            [
                                {
                                    "text": self.strings("back"),
                                    "callback": self.inline_advanced,
                                    "args": (mod, config_opt),
                                },
                                {
                                    "text": self.strings("close"),
                                    "callback": self.inline__close,
                                },
                            ],
                        ],
                    )
                else:
                    return await call.answer("This option doesn't have a boolean type!")

    async def inline__true_false_set(
        self,
        call: "aiogram.types.CallbackQuery",
        query: bool,
        mod: str,
        option: str,
        inline_message_id: str,
    ) -> None:
        for module in self.all_modules.modules:
            if module.name == mod:
                self.db.setdefault(module.name, {}).setdefault("__config__", {})[
                    option
                ] = query
                module.config[option] = query
                self.reconfmod(module, self.db)
                self.db.save()

        await self.inline__true_false(call, mod, option)

    async def inline__add_delete(
        self, call: "aiogram.types.CallbackQuery", mod: str, config_opt: str
    ) -> None:
        for module in self.all_modules.modules:
            if module.name == mod:
                if isinstance(module.config[config_opt], list):
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
                                    "text": self.strings("add_value_to_list_button"),
                                    "input": self.strings("enter_value"),
                                    "handler": self.inline__add_item,
                                    "args": (mod, config_opt, call.inline_message_id),
                                },
                                {
                                    "text": self.strings(
                                        "remove_value_from_list_button"
                                    ),
                                    "input": self.strings("enter_value"),
                                    "handler": self.inline__remove_item,
                                    "args": (mod, config_opt, call.inline_message_id),
                                },
                            ],
                            [
                                {
                                    "text": self.strings("back"),
                                    "callback": self.inline_advanced,
                                    "args": (mod, config_opt),
                                },
                                {
                                    "text": self.strings("close"),
                                    "callback": self.inline__close,
                                },
                            ],
                        ],
                    )
                else:
                    return await call.answer("This option doesn't have a list type!")

    async def inline_advanced(
        self, call: "aiogram.types.CallbackQuery", mod: str, config_opt: str
    ) -> None:
        for module in self.all_modules.modules:
            if module.name == mod:
                await call.edit(
                    self.strings("advanced").format(utils.escape_html(mod)),
                    reply_markup=[
                        [
                            {
                                "text": self.strings("true_false_button"),
                                "callback": self.inline__true_false,
                                "args": (mod, config_opt),
                            },
                            {
                                "text": self.strings("add_delete_button"),
                                "callback": self.inline__add_delete,
                                "args": (mod, config_opt),
                            },
                        ],
                        [
                            {
                                "text": self.strings("choose_button"),
                                "callback": self.inline__choose,
                                "args": (mod, config_opt),
                            }
                        ],
                        [
                            {
                                "text": self.strings("back"),
                                "callback": self.inline__configure_option,
                                "args": (mod, config_opt),
                            },
                            {
                                "text": self.strings("close"),
                                "callback": self.inline__close,
                            },
                        ],
                    ],
                )

    async def inline__choose(
        self, call: "aiogram.types.CallbackQuery", mod: str, config_opt: str
    ) -> None:
        for module in self.all_modules.modules:
            if module.name == mod:
                if not isinstance(module.config[config_opt], list):
                    return await call.answer("This option doesn't have a default list!")

                if not self.db.get(module.name, "__config__", {}).get(config_opt):
                    self.db.setdefault(module.name, {}).setdefault("__config__", {})[
                        config_opt
                    ] = module.config.getdef(config_opt)[:]

                    self.reconfmod(module, self.db)
                    self.db.save()

                kb = []
                ops = [str(i) for i in module.config[config_opt]]
                v = module.config.getdef(config_opt)[:]

                for mod_row in utils.chunks(v, 3):
                    row = [
                        {
                            "text": f"{'✅' if btn in ops else '❌'} {btn}",
                            "callback": self.inline__choose_set,
                            "args": (mod, config_opt, btn),
                        }
                        for btn in mod_row
                    ]
                    kb += [row]

                kb += [
                    [
                        {
                            "text": self.strings["back"],
                            "callback": self.inline_advanced,
                            "args": (mod, config_opt),
                        },
                        {
                            "text": self.strings["close"],
                            "callback": self.inline__close,
                        },
                    ]
                ]

                await call.edit(
                    self.strings("configuring_option").format(
                        utils.escape_html(config_opt),
                        utils.escape_html(mod),
                        utils.escape_html(module.config.getdoc(config_opt)),
                        utils.escape_html(module.config.getdef(config_opt)),
                        utils.escape_html(module.config[config_opt]),
                    ),
                    reply_markup=kb,
                )

    async def inline__choose_set(
        self,
        call: "aiogram.types.CallbackQuery",
        mod: str,
        option: str,
        value: str,
    ) -> None:
        for module in self.all_modules.modules:
            if module.name == mod:
                if value in module.config[option]:
                    module.config[option] = [
                        v for v in module.config[option] if v != value
                    ]
                else:
                    module.config[option].append(value)

                self.db.setdefault(module.name, {}).setdefault("__config__", {})[
                    option
                ] = module.config[option][:]

                self.reconfmod(module, self.db)
                self.db.save()

                await self.inline__choose(call, mod, option)

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
                            },
                            {
                                "text": self.strings("restore_def_button"),
                                "callback": self.inline__set_to_default,
                                "args": (mod, config_opt, call.inline_message_id),
                            },
                        ],
                        [
                            {
                                "text": self.strings("advanced_button"),
                                "callback": self.inline_advanced,
                                "args": (mod, config_opt),
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
            reply_markup=list(utils.chunks(btns, 2))
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
        for mod_row in utils.chunks(to_config, 3):
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
        with contextlib.suppress(Exception):
            if (
                not getattr(message, "via_bot", False)
                or message.via_bot.id != (await self.bot.bot.get_me()).id
                or "This message is gonna be deleted..." not in getattr(message, "text", "")
            ):
                return

            await message.delete()