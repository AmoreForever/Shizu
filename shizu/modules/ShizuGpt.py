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
    async def set_gpt_key(self, app: Client, message: types.Message):
        """Set GPT key"""
        if args := message.get_args_raw():
            self.db.set("shizu.gpt", "token", args)
            await message.answer(
                "<emoji id=5021905410089550576>✅</emoji> <b>GPT key has been set</b>"
            )
        else:
            return await message.answer(
                "<emoji id=5789703785743912485>❔</emoji> What should I set?"
            )

    @loader.command()
    async def gpt(self, app: Client, message: types.Message):
        """Ask question to GPT"""
        args = message.get_args_raw()
        if not args:
            return await message.answer(
                "<emoji id=5789703785743912485>❔</emoji> What should I ask?"
            )
        token = self.db.get("shizu.gpt", "token", None)
        if not token:
            return await message.answer(
                "<emoji id=5789703785743912485>❔</emoji> Token not set."
            )
        await message.answer(
            "<emoji id=5819167501912640906>❔</emoji> <b>Your Question was:</b> <code>{}</code>\n\n<emoji id=5372981976804366741>🤖</emoji> <b>Answer: </b> Wait...".format(
                args
            )
        )
        answer = await self._get_chat_completion(args, token)
        await message.answer(
            "<emoji id=5819167501912640906>❔</emoji> <b>Your Question was:</b> <code>{}</code>\n\n<emoji id=5372981976804366741>🤖</emoji> <b>Answer:</b> {}".format(
                args, self._process_code_tags(answer)
            )
        )
