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


# ---------------------------------------------------------------------------


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


import time
import io

import logging

from pyrogram import Client, types

from .. import loader, utils, logger


@loader.module(name="ShizuTester", author="shizu")
class TesterMod(loader.Module):
    """Execute activities based on userbot self-testing"""

    strings = {
        "ping": "<emoji id=5220226955206467824>⚡️</emoji> <b>Telegram Response Rate:</b> <code>{}</code> <b>ms</b>",
        "no_logs_": "❕ You don't have any logs at verbosity  {} ({})",
        "invalid_verb": "Invalid verbosity level",
        "suspend": "<emoji id=5452023368054216810>🥶</emoji> <b>Shizu has been suspended for {} seconds</b>",
        "suspend_invalid_time": "<emoji id=5807626765874499116>🚫</emoji> <b>Invalid time to suspend</b>",
    }

    strings_ru = {
        "ping": "<emoji id=5220226955206467824>⚡️</emoji> <b>Скорость ответа Telegram:</b> <code>{}</code> <b>мс</b>",
        "no_logs_": "❕ У вас нет логов с уровнем {} ({})",
        "invalid_verb": "Недопустимый уровень вывода",
        "suspend": "<emoji id=5452023368054216810>🥶</emoji> <b>Shizu был приостановлен на {} секунд</b>",
        "suspend_invalid_time": "<emoji id=5807626765874499116>🚫</emoji> <b>Недопустимое время приостановки</b>",
    }

    strings_uz = {
        "ping": "<emoji id=5220226955206467824>⚡️</emoji> <b>Telegramga javob tezligi:</b> <code>{}</code> <b>ms</b>",
        "no_logs_": "❕ <b>Shu xil xatolik mavjud emas</b> ({})",
        "invalid_verb": "Bunday xil xatolik yoq",
        "suspend": "<emoji id=5452023368054216810>🥶</emoji> <b>Shizu {} soniya uchun to'xtatildi</b>",
        "suspend_invalid_time": "<emoji id=5807626765874499116>🚫</emoji> <b>To'xtatish uchun noto'g'ri vaqt</b>",
    }

    strings_jp = {
        "ping": "<emoji id=5220226955206467824>⚡️</emoji> <b>Telegramの応答速度:</b> <code>{}</code> <b>ms</b>",
        "no_logs_": "❕ あなたは {} ({}) レベルのログを持っていません",
        "invalid_verb": "このようなエラーはありません",
        "suspend": "<emoji id=5452023368054216810>🥶</emoji> <b>Shizu は {} 秒間停止されました</b>",
        "suspend_invalid_time": "<emoji id=5807626765874499116>🚫</emoji> <b>無効な一時停止時間</b>",
    }

    strings_ua = {
        "ping": "<emoji id=5220226955206467824>⚡️</emoji> <b>Швидкість відповіді Telegram:</b> <code>{}</code> <b>мс</b>",
        "no_logs_": "❕ У вас немає логів з рівнем {} ({})",
        "invalid_verb": "Недопустимий рівень виводу",
        "suspend": "<emoji id=5452023368054216810>🥶</emoji> <b>Shizu був призупинений на {} секунд</b>",
        "suspend_invalid_time": "<emoji id=5807626765874499116>🚫</emoji> <b>Недопустимий час призупинення</b>",
    }

    strings_kz = {
        "ping": "<emoji id=5220226955206467824>⚡️</emoji> <b>Telegramға жауап беру тездігі:</b> <code>{}</code> <b>мс</b>",
        "no_logs_": "❕ <b>Сізде бұл деңгейдегі журналдар жоқ</b> {} ({})",
        "invalid_verb": "Бұлдай қате жоқ",
        "suspend": "<emoji id=5452023368054216810>🥶</emoji> <b>Shizu {} секунд үшін тоқтатылды</b>",
        "suspend_invalid_time": "<emoji id=5807626765874499116>🚫</emoji> <b>Тоқтату уақыты жарамсыз</b>",
    }

    strings_kr = {
        "ping": "<emoji id=5220226955206467824>⚡️</emoji> <b>Telegram 응답 속도:</b> <code>{}</code> <b>ms</b>",
        "no_logs_": "❕ {} ({}) 레벨의 로그가 없습니다",
        "invalid_verb": "이런 오류는 없습니다",
        "suspend": "<emoji id=5452023368054216810>🥶</emoji> <b>Shizu는 {} 초 동안 중지되었습니다</b>",
        "suspend_invalid_time": "<emoji id=5807626765874499116>🚫</emoji> <b>잘못된 일시 중지 시간</b>",
    }

    @loader.command()
    async def logs(self, app: Client, message: types.Message):
        """To get logs. Usage: logs (verbosity level)"""

        args = message.get_args()

        lvl = 40

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
    async def ping(self, app: Client, message: types.Message):
        """Checks the response rate of the user bot"""
        start = time.perf_counter_ns()

        ms = await message.answer("<emoji id=5267444331010074275>▫️</emoji>")

        ping = round((time.perf_counter_ns() - start) / 10**6, 3)

        await ms.edit(
            self.strings("ping").format(ping),
        )

    @loader.command()
    async def suspend(self, app: Client, message: types.Message):
        """Suspend the userbot for a certain time (n seconds)"""

        try:
            await message.answer(
                self.strings("suspend").format(int(message.get_args()))
            )
            time.sleep(int(message.get_args()))

        except ValueError:
            await message.answer(self.strings("suspend_invalid_time"))
