# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru

from .. import loader, utils

import logging


logger = logging.getLogger(__name__)


@loader.module("ShizuSecurity", "hikamoru")
class ShizuSecurity(loader.Module):
    """Give owner permissions to users"""

    strings = {
        "who": "<emoji id=5780801684338905670>🕶</emoji> <b>Whom i must give owner permissions?</b>",
        "whod": "<emoji id=5780801684338905670>🕶</emoji> <b>Whom i must remove owner permissions?</b>",
        "done": "<emoji id=5780722455077196625>🔗</emoji> {} <b>user now owner!</b>",
        "doned": "<emoji id=5780722455077196625>🔗</emoji> {} <b>user now not owner!</b>",
        "already": "<emoji id=5780689203440390462>1️⃣</emoji> <b>This user is already owner</b>",
        "owners": "<emoji id=5467406098367521267>👑</emoji> <b>Owners:</b>\n{}",
        "not_owner": "<emoji id=5780689203440390462>1️⃣</emoji> <b>This user is not owner</b>",
        "no_owners": "<emoji id=5963242192741863664>📝</emoji> <b>There are no owners</b>",
        "owner_on": "👑 <b>Owner mode enabled</b>",
        "owner_off": "👑 <b>Owner mode disabled</b>",
        "button_on": "🔓 Enable",
        "button_off": "🔐 Disable",
        "add_owner": "➕ Add owner",
        "enter_id": "🆔 Enter user id",
        "back": "🔙 Back",
        "successfull": "✅ Successfully",
        "advanced_security": "🌗 Advanced security",
        "del_owner": "➖ Remove owner",
        "close": "🚫 Close",
    }

    strings_ru = {
        "who": "<emoji id=5780801684338905670>🕶</emoji> <b>Кому я должен дать права владельца?</b>",
        "whod": "<emoji id=5780801684338905670>🕶</emoji> <b>Кому я должен забрать права владельца?</b>",
        "done": "<emoji id=5780722455077196625>🔗</emoji> {} <b>пользователь теперь владелец!</b>",
        "doned": "<emoji id=5780722455077196625>🔗</emoji> {} <b>пользователь больше не владелец!</b>",
        "already": "<emoji id=5780689203440390462>1️⃣</emoji> <b>Этот пользователь уже владелец</b>",
        "owners": "<emoji id=5467406098367521267>👑</emoji> <b>Владельцы:</b>\n{}",
        "not_owner": "<emoji id=5780689203440390462>1️⃣</emoji> <b>Этот пользователь не владелец</b>",
        "no_owners": "<emoji id=5963242192741863664>📝</emoji> <b>Владельцев нет</b>",
        "owner_on": "👑 <b>Режим владельца включен</b>",
        "owner_off": "👑 <b>Режим владельца отключен</b>",
        "button_on": "🔓 Включить",
        "button_off": "🔐 Отключить",
        "add_owner": "➕ Добавить владельца",
        "enter_id": "🆔 Введите id пользователя",
        "back": "🔙 Назад",
        "successfull": "✅ Успешно",
        "advanced_security": "🌗 Расширенная безопасность",
        "del_owner": "➖ Удалить владельца",
        "close": "🚫 Закрыть",
    }

    strings_uz = {
        "who": "<emoji id=5780801684338905670>🕶</emoji> <b>Kimni egasi huquqini berishim kerak?</b>",
        "whod": "<emoji id=5780801684338905670>🕶</emoji> <b>Kimni egasi huquqini olib tashlashim kerak?</b>",
        "done": "<emoji id=5780722455077196625>🔗</emoji> {} <b>foydalanuvchi hozir egasi!</b>",
        "doned": "<emoji id=5780722455077196625>🔗</emoji> {} <b>foydalanuvchi artik egasi emas!</b>",
        "already": "<emoji id=5780689203440390462>1️⃣</emoji> <b>Ushbu foydalanuvchi allaqachon egasi</b>",
        "owners": "<emoji id=5467406098367521267>👑</emoji> <b>Egalar:</b>\n{}",
        "not_owner": "<emoji id=5780689203440390462>1️⃣</emoji> <b>Ushbu foydalanuvchi egasi emas</b>",
        "no_owners": "<emoji id=5963242192741863664>📝</emoji> <b>Egalar yo'q</b>",
        "owner_on": "👑 <b>Egasi rejimi yoqilgan</b>",
        "owner_off": "👑 <b>Egasi rejimi o'chirilgan</b>",
        "button_on": "🔓 Yoqish",
        "button_off": "🔐 O'chirish",
        "add_owner": "➕ Egani qo'shish",
        "enter_id": "🆔 Foydalanuvchi id sini kiriting",
        "back": "🔙 Orqaga",
        "successfull": "✅ Muvaffaqiyatli",
        "advanced_security": "🌗 Kengaytirilgan xavfsizlik",
        "del_owner": "➖ Egani o'chirish",
        "close": "🚫 Yopish",
    }

    strings_jp = {
        "who": "<emoji id=5780801684338905670>🕶</emoji> <b>誰に所有者の権限を与える必要がありますか？</b>",
        "whod": "<emoji id=5780801684338905670>🕶</emoji> <b>誰から所有者の権限を削除する必要がありますか？</b>",
        "done": "<emoji id=5780722455077196625>🔗</emoji> {} <b>ユーザーは所有者です！</b>",
        "doned": "<emoji id=5780722455077196625>🔗</emoji> {} <b>ユーザーは所有者ではありません！</b>",
        "already": "<emoji id=5780689203440390462>1️⃣</emoji> <b>このユーザーはすでに所有者です</b>",
        "owners": "<emoji id=5467406098367521267>👑</emoji> <b>所有者：</b>\n{}",
        "not_owner": "<emoji id=5780689203440390462>1️⃣</emoji> <b>このユーザーは所有者ではありません</b>",
        "no_owners": "<emoji id=5963242192741863664>📝</emoji> <b>所有者はいません</b>",
        "owner_on": "👑 <b>所有者モードが有効になっています</b>",
        "owner_off": "👑 <b>所有者モードが無効になっています</b>",
        "button_on": "🔓 有効にする",
        "button_off": "🔐 無効にする",
        "add_owner": "➕ 所有者を追加",
        "enter_id": "🆔 ユーザーIDを入力してください",
        "back": "🔙 戻る",
        "successfull": "✅ 成功",
        "advanced_security": "🌗 拡張セキュリティ",
        "del_owner": "➖ 所有者を削除",
        "close": "🚫 閉じる",
    }

    strings_kz = {
        "who": "<emoji id=5780801684338905670>🕶</emoji> <b>Кімге қолданушының құқығын беру керек?</b>",
        "whod": "<emoji id=5780801684338905670>🕶</emoji> <b>Кімнің қолданушы құқығын алуы керек?</b>",
        "done": "<emoji id=5780722455077196625>🔗</emoji> {} <b>пайдаланушы қазір қолданушы!</b>",
        "doned": "<emoji id=5780722455077196625>🔗</emoji> {} <b>пайдаланушы қазір қолданушы емес!</b>",
        "already": "<emoji id=5780689203440390462>1️⃣</emoji> <b>Бұл пайдаланушы әлі де қолданушы</b>",
        "owners": "<emoji id=5467406098367521267>👑</emoji> <b>Егерлер:</b>\n{}",
        "not_owner": "<emoji id=5780689203440390462>1️⃣</emoji> <b>Бұл пайдаланушы қолданушы емес</b>",
        "no_owners": "<emoji id=5963242192741863664>📝</emoji> <b>Егерлер жоқ</b>",
        "owner_on": "👑 <b>Егер режимі қосылған</b>",
        "owner_off": "👑 <b>Егер режимі өшірілген</b>",
        "button_on": "🔓 Қосу",
        "button_off": "🔐 Өшіру",
        "add_owner": "➕ Егерді қосу",
        "enter_id": "🆔 Пайдаланушының ID-сін енгізіңіз ",
        "back": "🔙 Артқа",
        "successfull": "✅ Сәтті",
        "advanced_security": "🌗 Кеңейтілген қауіпсіздік",
        "del_owner": "➖ Егерді өшіру",
        "close": "🚫 Жабу",
    }

    strings_ua = {
        "who": "<emoji id=5780801684338905670>🕶</emoji> <b>Кому я повинен дати права власника?</b>",
        "whod": "<emoji id=5780801684338905670>🕶</emoji> <b>Кому я повинен забрати права власника?</b>",
        "done": "<emoji id=5780722455077196625>🔗</emoji> {} <b>користувач тепер власник!</b>",
        "doned": "<emoji id=5780722455077196625>🔗</emoji> {} <b>користувач більше не власник!</b>",
        "already": "<emoji id=5780689203440390462>1️⃣</emoji> <b>Цей користувач вже власник</b>",
        "owners": "<emoji id=5467406098367521267>👑</emoji> <b>Власники:</b>\n{}",
        "not_owner": "<emoji id=5780689203440390462>1️⃣</emoji> <b>Цей користувач не власник</b>",
        "no_owners": "<emoji id=5963242192741863664>📝</emoji> <b>Власників немає</b>",
        "owner_on": "👑 <b>Режим власника увімкнено</b>",
        "owner_off": "👑 <b>Режим власника вимкнено</b>",
        "button_on": "🔓 Увімкнути",
        "button_off": "🔐 Вимкнути",
        "add_owner": "➕ Додати власника",
        "enter_id": "🆔 Введіть id користувача",
        "back": "🔙 Назад",
        "successfull": "✅ Успішно",
        "advanced_security": "🌗 Розширена безпека",
        "del_owner": "➖ Видалити власника",
        "close": "🚫 Закрити",
    }

    async def close_(self, call):
        await call.delete()

    async def owner_off_on(self, call, status):
        self.db.set("shizu.owner", "status", status)
        await call.edit(
            self.strings("owner_on") if status else self.strings("owner_off"),
            reply_markup=[
                [
                    {
                        "text": self.strings("button_off")
                        if status
                        else self.strings("button_on"),
                        "callback": self.owner_off_on,
                        "kwargs": {"status": False} if status else {"status": True},
                    },
                    {
                        "text": self.strings("advanced_security"),
                        "callback": self.advanced_security,
                    },
                ],
                [{"text": self.strings("close"), "callback": self.close_}],
            ],
        )

    async def advanced_security(self, call):
        await call.edit(
            self.strings("advanced_security"),
            reply_markup=[
                [
                    {
                        "text": self.strings("add_owner"),
                        "input": self.strings("enter_id"),
                        "handler": self.add_owner_hnd,
                        "args": (call.inline_message_id,),
                    },
                    {
                        "text": self.strings("del_owner"),
                        "input": self.strings("enter_id"),
                        "handler": self.del_owner_hnd,
                        "args": (call.inline_message_id,),
                    },
                ],
                [
                    {
                        "text": self.strings("back"),
                        "callback": self.owner_off_on,
                        "kwargs": {
                            "status": self.db.get("shizu.owner", "status", False)
                        },
                    },
                    {"text": self.strings("close"), "callback": self.close_},
                ],
            ],
        )

    async def add_owner_hnd(self, call: "aiogram.types.CallbackQuery", query, cid):
        self.db.set(
            "shizu.me",
            "owners",
            list(set(self.db.get("shizu.me", "owners", []) + [int(query)])),
        )
        await call.edit(
            self.strings("successfull"),
            reply_markup=[
                [
                    {
                        "text": self.strings("back"),
                        "callback": self.advanced_security,
                    },
                    {"text": self.strings("close"), "callback": self.close_},
                ]
            ],
            inline_message_id=cid,
        )

    async def del_owner_hnd(self, call: "aiogram.types.CallbackQuery", query, cid):
        self.db.set(
            "shizu.me",
            "owners",
            list(set(self.db.get("shizu.me", "owners", [])) - {int(query)}),
        )
        await call.edit(
            self.strings("successfull"),
            reply_markup=[
                [
                    {
                        "text": self.strings("back"),
                        "callback": self.advanced_security,
                    },
                    {"text": self.strings("close"), "callback": self.close_},
                ]
            ],
            inline_message_id=cid,
        )

    @loader.command()
    async def ownermod(self, app, message):
        """Switch owner mode"""
        status = self.db.get("shizu.owner", "status", False)
        await message.answer(
            self.strings("owner_on") if status else self.strings("owner_off"),
            reply_markup=[
                [
                    {
                        "text": self.strings("button_off")
                        if status
                        else self.strings("button_on"),
                        "callback": self.owner_off_on,
                        "kwargs": {"status": False} if status else {"status": True},
                    },
                    {
                        "text": self.strings("advanced_security"),
                        "callback": self.advanced_security,
                    },
                ],
                [
                    {"text": self.strings("close"), "callback": self.close_},
                ],
            ],
        )

    @loader.command()
    async def addowner(self, app, message):
        """Give owner permissions to user - <user_id>"""
        user = int(utils.get_args(message))
        if not user:
            await utils.answer(message, self.strings("who"))
            return
        if user in self.db.get("shizu.me", "owners", []):
            await utils.answer(message, self.strings("already"))
            return
        self.db.set(
            "shizu.me",
            "owners",
            list(set(self.db.get("shizu.me", "owners", []) + [user])),
        )
        await utils.answer(
            message, self.strings("done").format((await app.get_users(user)).mention)
        )

    @loader.command()
    async def delowner(self, app, message):
        """Remove owner permissions from user - <user_id>"""
        user = utils.get_args(message)
        if not user:
            await utils.answer(message, self.strings("whod"))
            return
        if user not in self.db.get("shizu.me", "owners", []):
            await utils.answer(message, self.strings("not_owner"))
            return
        self.db.set(
            "shizu.me",
            "owner",
            list(set(self.db.get("shizu.me", "owners", [])) - {user}),
        )
        await utils.answer(
            message, self.strings("doned").format((await app.get_users(user)).mention)
        )

    @loader.command()
    async def owners(self, app, message):
        """Show owners"""
        owners = self.db.get("shizu.me", "owners", [])
        if not owners:
            await utils.answer(message, self.strings("no_owners"))
            return
        await utils.answer(
            message,
            self.strings("owners").format(
                "\n".join(
                    [f"• {(await app.get_users(user)).mention}" for user in owners]
                )
            ),
        )
