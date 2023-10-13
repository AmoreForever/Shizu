#    Sh1t-UB (telegram userbot by sh1tn3t)
#    Copyright (C) 2021-2022 Sh1tN3t

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru


import time
import io
import os
import sys
import atexit

import logging
from .. import logger

from pyrogram import Client, types
from pyrogram.raw import functions, types as typ
from .. import loader, utils, translater


@loader.module(name="ShizuTester", author="shizu")
class TesterMod(loader.Module):
    """Execute activities based on userbot self-testing"""

    strings = {
        "incorrect_language": "❕ <b>Incorrect language.",
        "language_saved": "{} Language saved",
        "no_logs_": "❕ You don't have any logs at verbosity  {} ({})",
        "invalid_verb": "Invalid verbosity level",
        "which_alias": "❔ Which alias should I add?",
        "ch_prefix": "❔ Which prefix should I change to?",
        "prefix_changed": "✅ Prefix has been changed to {}",
        "inc_args": "❌ The arguments are incorrect.\n✅ Correct: addalias <new alias> <command>",
        "alias_already": "❌ Such an alias already exists",
        "no_command": "❌ There is no such command",
        "alias_done": "✅ Alias <code>{}</code> for the command <code>{}</code> has been added",
        "which_delete": "❔ Which alias should I delete?",
        "no_such_alias": "❌ There is no such alias",
        "alias_removed": "✅ Alias <code>{}</code> has been deleted",
        "ping": "<emoji id=5220226955206467824>⚡️</emoji> <b>Telegram Response Rate:</b> <code>{}</code> <b>ms</b>",
    }

    strings_ru = {
        "incorrect_language": "❕ <b>Неправильный язык.",
        "language_saved": "{} Язык сохранен",
        "no_logs_": "❕ У вас нет логов с уровнем {} ({})",
        "invalid_verb": "Недопустимый уровень вывода",
        "which_alias": "❔ Какой алиас добавить?",
        "ch_prefix": "❔ Какое префикс поставить?",
        "prefix_changed": "✅ Префикс изменен на {}",
        "inc_args": "❌ Параметры некорректны.\n✅ Правильно: addalias <новый алиас> <команда>",
        "alias_already": "❌ Такой алиас уже существует",
        "no_command": "❌ Такой команды не существует",
        "alias_done": "✅ Алиас <code>{}</code> для команды <code>{}</code> добавлен",
        "which_delete": "❔ Какой алиас удалить?",
        "no_such_alias": "❌ Такой алиас не существует",
        "alias_removed": "✅ Алиас <code>{}</code> удален",
        "ping": "<emoji id=5220226955206467824>⚡️</emoji> <b>Скорость ответа Telegram:</b> <code>{}</code> <b>мс</b>",
    }

    strings_uz = {
        "incorrect_language": "❕ <b>Bu til mavjud emas</b>",
        "language_saved": "{} Til saqlandi",
        "no_logs_": "❕ <b>Shu xil xatolik mavjud emas</b> ({})",
        "invalid_verb": "Bunday xil xatolik yoq",
        "which_alias": "❔ Kanday alias qo'shmoqchisiz?",
        "ch_prefix": "❔ Qaysi prefiksni o'rnatmoqchisiz?",
        "prefix_changed": "✅ Prefix {} ga ozgardi",
        "inc_args": "❌ Parametrlar xato.\n✅ Tog'ri: addalias <yeni alias> <komanda>",
        "alias_already": "❌ Bu alias mavjud",
        "no_command": "❌ Bu komanda mavjud emas",
        "alias_done": "✅ Alias <code>{}</code> bu komanda uchun yaratildi <code>{}</code>",
        "which_delete": "❔ Kanday alias o'chirmoqchisiz?",
        "no_such_alias": "❌ Bu alias mavjud emas",
        "alias_removed": "✅ Alias <code>{}</code> o'chirildi",
        "ping": "<emoji id=5220226955206467824>⚡️</emoji> <b>Telegramga javob tezligi:</b> <code>{}</code> <b>ms</b>",
    }

    strings_jp = {
        "incorrect_language": "❕ <b>言語が間違っています</b> .",
        "language_saved": "{} 言語が保存されました",
        "no_logs_": "❕ <b>このようなエラーはありません</b> ({})",
        "invalid_verb": "このようなエラーはありません",
        "which_alias": "❔ どのエイリアスを追加しますか？",
        "ch_prefix": "❔ どのプレフィックスを設定しますか？",
        "prefix_changed": "✅ プレフィックスが変更されました {}",
        "inc_args": "❌ パラメーターが間違っています。\n✅ 正しい: addalias <新しいエイリアス> <コマンド>",
        "alias_already": "❌ このようなエイリアスは既に存在します",
        "no_command": "❌ このようなコマンドはありません",
        "alias_done": "✅ エイリアス <code>{}</code> はコマンドのために作成されました <code>{}</code>",
        "which_delete": "❔ どのエイリアスを削除しますか？",
        "no_such_alias": "❌ このようなエイリアスはありません",
        "alias_removed": "✅ エイリアス <code>{}</code> 削除されました",
        "ping": "<emoji id=5220226955206467824>⚡️</emoji> <b>Telegramの応答速度:</b> <code>{}</code> <b>ms</b>",
    }

    strings_ua = {
        "incorrect_language": "❕ <b>Неправильна мова</b>",
        "language_saved": "{} Мова збережена",
        "no_logs_": "❕ <b>Такої помилки не існує</b> ({})",
        "invalid_verb": "Такої помилки не існує",
        "which_alias": "❔ Який аліас додати?",
        "ch_prefix": "❔ Який префікс встановити?",
        "prefix_changed": "✅ Префікс змінено на {}",
        "inc_args": "❌ Параметри некоректні.\n✅ Правильно: addalias <новий аліас> <команда>",
        "alias_already": "❌ Такий аліас вже існує",
        "no_command": "❌ Такої команди не існує",
        "alias_done": "✅ Аліас <code>{}</code> для команди <code>{}</code> додано",
        "which_delete": "❔ Який аліас видалити?",
        "no_such_alias": "❌ Такого аліасу не існує",
        "alias_removed": "✅ Аліас <code>{}</code> видалено",
        "ping": "<emoji id=5220226955206467824>⚡️</emoji> <b>Швидкість відповіді Telegram:</b> <code>{}</code> <b>мс</b>",
    }
    
    strings_kz = {
        "incorrect_language": "❕ <b>Тіл дұрыс емес</b>",
        "language_saved": "{} Тіл сақталды",
        "no_logs_": "❕ <b>Мұндай қате жоқ</b> ({})",
        "invalid_verb": "Мұндай қате жоқ",
        "which_alias": "❔ Қай алиас қосқыңыз келеді?",
        "ch_prefix": "❔ Қай префикс орнатыңыз келеді?",
        "prefix_changed": "✅ Префикс {} өзгертілді",
        "inc_args": "❌ Параметрлер қате.\n✅ Дұрыс: addalias <жаңа алиас> <бағдарлама>",
        "alias_already": "❌ Мұндай алиас бар",
        "no_command": "❌ Мұндай бағдарлама жоқ",
        "alias_done": "✅ Алиас <code>{}</code> бағдарлама үшін құрылды <code>{}</code>",
        "which_delete": "❔ Қай алиас жою керек?",
        "no_such_alias": "❌ Мұндай алиас жоқ",
        "alias_removed": "✅ Алиас <code>{}</code> жойылды",
        "ping": "<emoji id=5220226955206467824>⚡️</emoji> <b>Telegramға жауап беру тездігі:</b> <code>{}</code> <b>мс</b>",
    }

    @loader.command()
    async def logs(self, app: Client, message: types.Message, args: str):
        """To get logs. Usage: logs (verbosity level)"""
        lvl = 40  # ERROR

        if args and not (lvl := logger.get_valid_level(args)):
            return await message.answer(self.strings("invalid_verb"))

        handler = logging.getLogger().handlers[0]
        logs = ("\n".join(handler.dumps(lvl))).encode("utf-8")
        if not logs:
            return await message.answer(
                self.strings("no_logs_").format(
                    lvl,
                    logging.getLevelName(lvl),
                )
            )

        logs = io.BytesIO(logs)
        logs.name = "shizu.log"

        await message.delete()
        return await message.answer(
            logs,
            doc=True,
            caption=f"🐙 Shizu logs with verbosity {lvl} ({logging.getLevelName(lvl)})",
        )

    @loader.command()
    async def setprefix(self, app: Client, message: types.Message, args: str):
        """To change the prefix, you can have several pieces separated by a space. Usage: setprefix (prefix) [prefix, ...]"""
        if not (args := args.split()):
            return await message.answer(self.strings("ch_prefix"))

        self.db.set("shizu.loader", "prefixes", list(set(args)))
        prefixes = ", ".join(f"<code>{prefix}</code>" for prefix in args)
        return await message.answer(self.strings("prefix_changed").format(prefixes))

    @loader.command()
    async def addalias(self, app: Client, message: types.Message, args: str):
        """Add an alias. Usage: addalias (new alias) (command)"""
        if not (args := args.lower().split(maxsplit=1)):
            return await message.answer(self.strings("which_alias"))

        if len(args) != 2:
            return await message.answer(self.strings("inc_args"))

        aliases = self.all_modules.aliases
        if args[0] in aliases:
            return await message.answer(self.strings("alias_already"))

        if not self.all_modules.command_handlers.get(args[1]):
            return await message.answer(self.strings("no_command"))

        aliases[args[0]] = args[1]
        self.db.set("shizu.loader", "aliases", aliases)

        return await message.answer(
            self.strings("alias_done").format(
                args[0],
                args[1],
            )
        )

    @loader.command()
    async def delalias(self, app: Client, message: types.Message, args: str):
        """Delete the alias. Usage: delalas (alias)"""
        if not (args := args.lower()):
            return await message.answer(self.strings("which_delete"))

        aliases = self.all_modules.aliases
        if args not in aliases:
            return await message.answer(self.strings("no_such_alias"))

        del aliases[args]
        self.db.set("shizu.loader", "aliases", aliases)

        return await message.answer(self.strings("alias_removed").format(args))

    @loader.command()
    async def aliases(self, app: Client, message: types.Message):
        """Show all aliases"""
        if aliases := self.all_modules.aliases:
            return await message.answer(
                "🗄 List of all aliases:\n"
                + "\n".join(
                    f"• <code>{alias}</code> ➜ {command}"
                    for alias, command in aliases.items()
                ),
            )
        else:
            return await message.answer(self.strings("no_such_alias"))

    @loader.command()
    async def ping(self, app: Client, message: types.Message, args: str):
        """Checks the response rate of the user bot"""
        start = time.perf_counter_ns()
        await message.answer("<emoji id=5267444331010074275>▫️</emoji>")
        ping = round((time.perf_counter_ns() - start) / 10**6, 3)
        await message.answer(
            self.strings("ping").format(ping),
        )

    async def on_load(self, app: Client):
        """Create Folder"""
        if self.db.get("shizu.folder", "folder"):
            return

        logging.info("Trying to create folder")
        app.me = await app.get_me()
        folder_id = 250
        logs_id = (
            await utils.create_chat(
                app,
                "Shizu-logs",
                "📫 Shizu-logs do not delete this group, otherwise bot will be broken",
                True,
                True,
                True,
            )
        ).id

        backup_id = (
            await utils.create_chat(
                app,
                "Shizu-backup",
                "📫 Backup-logs do not delete this group, otherwise bot will be broken",
                True,
                True,
                True,
            )
        ).id

        logs = await app.resolve_peer(logs_id)
        backup = await app.resolve_peer(backup_id)

        await app.set_chat_photo(chat_id=logs_id, photo="assets/logs.jpg")
        await app.set_chat_photo(chat_id=backup_id, photo="assets/backups.jpg")

        await app.invoke(
            functions.messages.UpdateDialogFilter(
                id=folder_id,
                filter=typ.DialogFilter(
                    id=folder_id,
                    title="Shizu",
                    include_peers=[logs, backup],
                    pinned_peers=[],
                    exclude_peers=[],
                    emoticon="❤️",
                ),
            )
        )

        logging.info("Folder created")
        self.db.set("shizu.folder", "folder", True)
        self.db.set("shizu.chat", "logs", logs_id)
        self.db.set("shizu.chat", "backup", backup_id)
        atexit.register(os.execl(sys.executable, sys.executable, "-m", "shizu"))
