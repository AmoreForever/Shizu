# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru

from .. import loader, utils
from pyrogram import Client, types


@loader.module(name="ShizuSettings", author="shizu")
class ShizuSettings(loader.Module):
    """Settings for Shizu userbot"""

    strings = {
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
    }

    strings_ru = {
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
    }

    strings_uz = {
        "which_alias": "❔ Kanday alias qo'shmoqchisiz?",
        "ch_prefix": "❔ Qaysi prefiksni o'rnatmoqchisiz?",
        "prefix_changed": "✅ Prefix {} ga ozgardi",
        "inc_args": "❌ Parametrlar xato.\n✅ Tog'ri: addalias <yangi alias> <komanda>",
        "alias_already": "❌ Bu alias mavjud",
        "no_command": "❌ Bu komanda mavjud emas",
        "alias_done": "✅ Alias <code>{}</code> bu komanda uchun yaratildi <code>{}</code>",
        "which_delete": "❔ Kanday alias o'chirmoqchisiz?",
        "no_such_alias": "❌ Bu alias mavjud emas",
        "alias_removed": "✅ Alias <code>{}</code> o'chirildi",
    }

    strings_jp = {
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
    }

    strings_ua = {
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
    }

    strings_kz = {
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
    }

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
