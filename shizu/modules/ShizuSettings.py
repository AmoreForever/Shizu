# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru

import re
from .. import loader, utils
from pyrogram import Client, types

from telethon import TelegramClient
from telethon.errors import FloodWaitError, SessionPasswordNeededError


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
        "are_you_sure": "🚸 <b>Are you sure you want to enable telethon? We will not be responsible for your actions, even if you are banned. Enabling telethon may result in unintended consequences or violations of our policies. Please proceed with caution and ensure that you use this feature responsibly and in accordance with our guidelines. Any misuse of telethon may lead to disciplinary actions, up to and including account suspension or permanent bans.</b>",
        "yes_button": "✅ Totally sure",
        "no_button": "❌ No",
        "type_code": "⌨️ Please type code that you received from Telegram",
        "code_number": "#️⃣ Type code",
        "congratulations": "🎉 <b>Congratulations! You have successfully enabled telethon!</b>\n<i>But you need to restart bot to apply changes</i>",
        "already_enabled": "🧞 <b>Telethon is already enabled</b>",
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
        "are_you_sure": "🚸 <b>Вы уверены, что хотите включить telethon? Мы не несем ответственности за ваши действия, даже если вы забанены. Включение telethon может привести к непреднамеренным последствиям или нарушениям наших политик. Пожалуйста, действуйте осторожно и убедитесь, что вы используете эту функцию ответственно и в соответствии с нашими руководствами. Любое неправильное использование telethon может привести к дисциплинарным мерам, вплоть до приостановки учетной записи или постоянной блокировки.</b>",
        "yes_button": "✅ Полностью уверен",
        "no_button": "❌ Нет",
        "type_code": "⌨️ Пожалуйста, введите код, который вы получили от Telegram",
        "code_number": "#️⃣ Введите код",
        "congratulations": "🎉 <b>Поздравляем! Вы успешно включили telethon!</b>\n<i>Но вам нужно перезапустить бота, чтобы изменения вступили в силу</i>",
        "already_enabled": "🧞 <b>Telethon уже включен</b>",
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
        "are_you_sure": "🚸 <b>Telethonni yoqingizga ishonchingiz komilmi? Biz sizning amallaringizdan javobgar emas, hatto agar siz bloklangansiz. Telethonni yoqish, noma'lum natijalarga yoki bizning siyosatimizni buzishga olib kelishi mumkin. Iltimos, ehtiyotkorlik bilan harakat qiling va ushbu xususiyatni siz mas'uliyat bilan va bizning ko'rsatmalarimizga muvofiq mas'ul foydalaning. Telethonni noto'g'ri foydalanish, hisobni to'xtatish yoki doimiy bloklanganligiga qadar shikoyatlarga olib kelishi mumkin.</b>",
        "yes_button": "✅ To'liq ishonch",
        "no_button": "❌ Yo'q",
        "type_code": "⌨️ Iltimos, Telegramdan olingan kodni kiriting",
        "code_number": "#️⃣ Code kiriting",
        "congratulations": "🎉 <b>Tabriklaymiz! Siz telethonni muvaffaqiyatli yoqdingiz!</b>\n<i>Lekin o'zgarishlarni amalga oshirish uchun botni qayta ishga tushirishingiz kerak</i> ",
        "already_enabled": "🧞 <b>Telethon allaqachon yoqingan</b>",
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
        "are_you_sure": "🚸 <b>telethonを有効にしますか？ あなたの行動に責任を負いません。 telethonを有効にすると、意図しない結果や当社のポリシーの違反が発生する可能性があります。 慎重に行動し、この機能を責任を持って、当社のガイドラインに従って使用することを確認してください。 telethonの誤用は、アカウントの停止または永久に禁止されるなどの処分措置につながる可能性があります。</b>",
        "yes_button": "✅ 完全に確信している",
        "no_button": "❌ いいえ",
        "type_code": "⌨️ Telegram から受け取ったコードを入力してください",
        "code_number": "#️⃣ コードを入力してください",
        "congratulations": "🎉 <b>おめでとうございます！ telethonを正常に有効にしました！</b>\n<i>ただし、変更を適用するにはボットを再起動する必要があります</i>",
        "already_enabled": "🧞 <b>telethonはすでに有効になっています</b>",
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
        "are_you_sure": "🚸 <b>Ви впевнені, що хочете увімкнути telethon? Ми не несемо відповідальності за ваші дії, навіть якщо ви заблоковані. Увімкнення telethon може призвести до непередбачуваних наслідків або порушень наших політик. Будь ласка, дійте обережно і переконайтеся, що ви використовуєте цю функцію відповідально і відповідно до наших вказівок. Будь-яке зловживання telethon може призвести до дисциплінарних заходів, включаючи призупинення облікового запису або постійну блокування.</b>",
        "yes_button": "✅ Повністю впевнений",
        "no_button": "❌ Ні",
        "type_code": "⌨️ Будь ласка, введіть код, який ви отримали від Telegram",
        "code_number": "#️⃣ Введіть код",
        "congratulations": "🎉 <b>Вітаємо! Ви успішно увімкнули telethon!</b>\n<i>Але вам потрібно перезапустити бота, щоб зміни набули чинності</i>",
        "already_enabled": "🧞 <b>Telethon вже увімкнено</b>",
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
        "are_you_sure": "🚸 <b>Телетонды қосқыңыз келеді ме? Сіздің әрекеттеріңізге жауап бермейміз, сондықтан да сіз блокталсаңыз да. Телетонды қосу нәтижесінде немесе біздің саясатымызды алдын ала алуы мүмкін. Қатты есепке алмастыру үшін қажет етеді және бұл функцияны қолдануға жауапкершілікті және біздің нұсқауларымызға сәйкес қолдануға көз жеткізіңіз. Телетонды дұрыс қолданбайтын, тікелей қарау немесе толықтыруға дейін есептелу мүмкіндігі бар.</b>",
        "yes_button": "✅ Толық сенімдімін",
        "no_button": "❌ Жоқ",
        "type_code": "⌨️ Телеграммен алған кодты енгізіңіз",
        "code_number": "#️⃣ Кодты енгізіңіз",
        "congratulations": "🎉 <b>Құттықтаймыз! Сіз телетонды сәтті қосдыңыз!</b>\n<i>Бірақ өзгерістерді қолдану үшін ботты қайта іске қосу қажет</i>",
        "already_enabled": "🧞 <b>Телетон әлі қосылған</b>",
    }

    async def on_load(self, app):
        me = self.db.get("shizu.me", "me", None)
        if not me:
            id_ = (await app.get_me()).id
            self.db.set("shizu.me", "me", id_)
        app.is_tl_enabled = utils.is_tl_enabled()

    def markup_(self):
        return [
            [
                {
                    "text": self.strings["yes_button"],
                    "callback": self.yes,
                },
                {
                    "text": self.strings["no_button"],
                    "callback": self.close,
                },
            ]
        ]

    async def close(self, call):
        await call.delete()

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

    async def yes(self, call):
        phone = phone = f"+{(await self.app.get_me()).phone_number}"
        api_id = self.app.api_id
        api_hash = self.app.api_hash
        client = TelegramClient("shizu-tl", api_id, api_hash)
        await client.connect()
        try:
            login = await client.send_code_request(phone=phone)
            await client.disconnect()
        except FloodWaitError as e:
            return await call.edit(f"Too many attempts, please wait  {e.seconds}")

        async for message in self.app.get_chat_history(777000, limit=1, offset_id=-1):
            t = message.text

        code = re.findall(r"(\d{5})", t)[0]
        client = TelegramClient("shizu-tl", api_id, api_hash, device_model="Shizu-Tl")
        await client.connect()
        try:
            await client.sign_in(
                phone=f"+{(await self.app.get_me()).phone_number}",
                code=code,
                phone_code_hash=login.phone_code_hash,
            )
            await client.disconnect()
            await call.edit(self.strings["congratulations"])
        except SessionPasswordNeededError:
            await call.edit(
                "\n\nPlease temporarily disable 2FA\n\n <i># Hikamoru too lazy to extend this module</i>"
            )

    @loader.command()
    async def enabletlmode(self, app, message):
        """Enable telethon mode"""
        if utils.is_tl_enabled() is False:
            return await message.answer(
                self.strings["are_you_sure"]
                + "\n\nPlease temporarily disable 2FA\n\n <i># Hikamoru too lazy to extend this module</i>",
                reply_markup=self.markup_(),
            )
        await message.answer(self.strings["already_enabled"])