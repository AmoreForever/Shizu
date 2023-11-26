# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru

import re
import requests

from pyrogram import types, Client
from .. import loader, utils

# https://raw.githubusercontent.com/MoriSummerz/ftg-mods/main/chatgpt.py


@loader.module("ShizuGpt", "hikamoru", 1.0)
class ShizuGpt(loader.Module):
    """ChatGPT AI API interaction"""

    strings = {
        "set": "<emoji id=5021905410089550576>✅</emoji> <b>GPT key has been set</b>",
        "what": "<emoji id=5789703785743912485>❔</emoji> What should I set?",
        "what_ask": "<emoji id=5789703785743912485>❔</emoji> What should I ask?",
        "no_token": "<emoji id=5789703785743912485>❔</emoji> Token not set.",
        "pending": "<emoji id=5819167501912640906>❔</emoji> <b>Your Question was:</b> <code>{}</code>\n\n<emoji id=5372981976804366741>🤖</emoji> <b>Answer: </b> Wait...",
        "answer": "<emoji id=5819167501912640906>❔</emoji> <b>Your Question was:</b> <code>{}</code>\n\n<emoji id=5372981976804366741>🤖</emoji> <b>Answer:</b> {}",
        "cfg_doc": "Here you can set your GPT key, you can get it here: https://platform.openai.com/",
    }

    strings_ru = {
        "set": "<emoji id=5021905410089550576>✅</emoji> <b>GPT ключ установлен</b>",
        "what": "<emoji id=5789703785743912485>❔</emoji> Что нужно установить?",
        "what_ask": "<emoji id=5789703785743912485>❔</emoji> Что нужно задать?",
        "no_token": "<emoji id=5789703785743912485>❔</emoji> Токен не установлен.",
        "pending": "<emoji id=5819167501912640906>❔</emoji> <b>Ваш вопрос:</b> <code>{}</code>\n\n<emoji id=5372981976804366741>🤖</emoji> <b>Ответ:</b> Ожидание...",
        "answer": "<emoji id=5819167501912640906>❔</emoji> <b>Ваш вопрос:</b> <code>{}</code>\n\n<emoji id=5372981976804366741>🤖</emoji> <b>Ответ:</b> {}",
        "cfg_doc": "Здесь вы можете установить свой GPT ключ, вы можете получить его здесь: https://platform.openai.com/",
    }

    strings_uz = {
        "set": "<emoji id=5021905410089550576>✅</emoji> <b>GPT kalit ornatildi</b>",
        "what": "<emoji id=5789703785743912485>❔</emoji> Nma ornatishim kerak?",
        "what_ask": "<emoji id=5789703785743912485>❔</emoji> Nma qoldiring?",
        "no_token": "<emoji id=5789703785743912485>❔</emoji> Token not set.",
        "pending": "<emoji id=5819167501912640906>❔</emoji> <b>Yozuv:</b> <code>{}</code>\n\n<emoji id=5372981976804366741>🤖</emoji> <b>Javob:</b> O'qiyapman...",
        "answer": "<emoji id=5819167501912640906>❔</emoji> <b>Yozuv:</b> <code>{}</code>\n\n<emoji id=5372981976804366741>🤖</emoji> <b>Javob:</b> {}",
        "cfg_doc": "Bu erda siz o'zingizning GPT kalitingizni o'rnatishingiz mumkin, uni ushbu manzilda olishingiz mumkin: https://platform.openai.com/",
    }

    strings_jp = {
        "set": "<emoji id=5021905410089550576>✅</emoji> <b>GPTキーが設定されました</b>",
        "what": "<emoji id=5789703785743912485>❔</emoji> 何を設定する必要がありますか？",
        "what_ask": "<emoji id=5789703785743912485>❔</emoji> 何を尋ねる必要がありますか？",
        "no_token": "<emoji id=5789703785743912485>❔</emoji> トークンが設定されていません。",
        "pending": "<emoji id=5819167501912640906>❔</emoji> <b>あなたの質問は:</b> <code>{}</code>\n\n<emoji id=5372981976804366741>🤖</emoji> <b>答え:</b> 待ってください...",
        "answer": "<emoji id=5819167501912640906>❔</emoji> <b>あなたの質問は:</b> <code>{}</code>\n\n<emoji id=5372981976804366741>🤖</emoji> <b>答え:</b> {}",
        "cfg_doc": "ここではGPTキーを設定できます。ここで取得できます：https://platform.openai.com/",
    }

    strings_ua = {
        "set": "<emoji id=5021905410089550576>✅</emoji> <b>GPT ключ встановлено</b>",
        "what": "<emoji id=5789703785743912485>❔</emoji> Що потрібно встановити?",
        "what_ask": "<emoji id=5789703785743912485>❔</emoji> Що потрібно запитати?",
        "no_token": "<emoji id=5789703785743912485>❔</emoji> Токен не встановлено.",
        "pending": "<emoji id=5819167501912640906>❔</emoji> <b>Ваш запитання:</b> <code>{}</code>\n\n<emoji id=5372981976804366741>🤖</emoji> <b>Відповідь:</b> Очікування...",
        "answer": "<emoji id=5819167501912640906>❔</emoji> <b>Ваш запитання:</b> <code>{}</code>\n\n<emoji id=5372981976804366741>🤖</emoji> <b>Відповідь:</b> {}",
        "cfg_doc": "Тут ви можете встановити свій GPT ключ, ви можете отримати його тут: https://platform.openai.com/",
    }

    strings_kz = {
        "set": "<emoji id=5021905410089550576>✅</emoji> <b>GPT тіркелді</b>",
        "what": "<emoji id=5789703785743912485>❔</emoji> Нені орнату керек?",
        "what_ask": "<emoji id=5789703785743912485>❔</emoji> Нені сұрау керек?",
        "no_token": "<emoji id=5789703785743912485>❔</emoji> Токен орнатылмаған.",
        "pending": "<emoji id=5819167501912640906>❔</emoji> <b>Сұрағыңыз:</b> <code>{}</code>\n\n<emoji id=5372981976804366741>🤖</emoji> <b>Жауабы:</b> Күту...",
        "answer": "<emoji id=5819167501912640906>❔</emoji> <b>Сұрағыңыз:</b> <code>{}</code>\n\n<emoji id=5372981976804366741>🤖</emoji> <b>Жауабы:</b> {}",
        "cfg_doc": "Мұнда сіз оған түсініктеме беретін GPT тіркелгіңізді орнатуға болады: https://platform.openai.com/",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "GPT_KEY", None, lambda m: self.strings("cfg_doc")
        )

    async def _make_request(
        self,
        method: str,
        url: str,
        headers: dict,
        data: dict,
    ) -> dict:
        """
        Makes an asynchronous HTTP request using the specified method, URL,
        headers, and data.

        Parameters:
            method (str): The HTTP method to use for the request.
            url (str): The URL to send the request to.
            headers (dict): The headers to include in the request.
            data (dict): The JSON data to include in the request body.

        Returns:
            dict: The JSON response from the server.
        """
        resp = await utils.run_sync(
            requests.request,
            method,
            url,
            headers=headers,
            json=data,
        )
        return resp.json()

    def _process_code_tags(self, text: str) -> str:
        return re.sub(
            r"`(.*?)`",
            r"<code>\1</code>",
            re.sub(r"```(.*?)```", r"<code>\1</code>", text, flags=re.DOTALL),
            flags=re.DOTALL,
        )

    async def _get_chat_completion(self, prompt: str, token: str) -> str:
        resp = await self._make_request(
            method="POST",
            url="https://api.openai.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
            data={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
            },
        )
        if resp.get("error", None):
            return f"🚫 {resp['error']['message']}"

        return resp["choices"][0]["message"]["content"]

    @loader.command()
    async def gpt(self, app: Client, message: types.Message):
        """Ask question to GPT"""
        args = message.get_args_raw()

        if not args:
            return await message.answer(self.strings("what_ask"))

        token = self.config["GPT_KEY"]
        if not token:
            return await message.answer(self.strings("no_token"))
        await message.answer(self.strings("pending").format(args))
        answer = await self._get_chat_completion(args, self.config["GPT_KEY"])
        await message.answer(
            self.strings("answer").format(args, self._process_code_tags(answer))
        )
