"""In this file we have to make contract with Aelis API"""


# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru


import logging
import asyncio
import contextlib
import httpx

from pyrogram import Client
from .database import db

logger = logging.getLogger("aelis")
logging.getLogger("httpx").propagate = False


class AelisNotAuthorized(Exception):
    def __init__(self, message):
        self.message = message


class AelisAPI:
    def __init__(self, app: Client):
        """
        Initializes an instance of the class.

        This method sets the initial values for the attributes of the class.
        - `name`: A string representing the name of the API.
        - `api`: A string representing the URL of the API.
        - `db`: An object representing the database.
        - `session`: An `httpx.AsyncClient` object used for making asynchronous HTTP requests.

        """
        self.name = "Aelis API"
        self.api = "https://aelis.hikamoru.uz"
        self.db = db
        self.session = httpx.AsyncClient()
        self.app = app
        asyncio.create_task(self.post_info())

    async def post_info(self):
        """
        Sends a POST request to the API endpoint to post information.

        :return: None
        """
        user_id = (await self.app.get_me()).id
        params = {"user_id": user_id, "userbot": "shizu"}
        url = f"{self.api}/user/"
        x = await self.session.post(url, params=params)
        self.db.set("aelis", "token", x.json()["token"])

    async def search(self, module):
        """
        Asynchronously searches for a module in the API.

        Args:
            module (str): The name of the module to search for.

        Returns:
            dict: The response from the API containing the search results.

        Raises:
            AelisNotAuthorized: If the API returns a 401 error indicating that the user is not authorized.

        """
        url = f"{self.api}/get/"
        params = {
            "mod": module,
            "token": self.db.get("aelis", "token"),
        }
        response = (await self.session.get(url, params=params)).json()
        with contextlib.suppress(Exception):
            if response["code"] == 401:
                raise AelisNotAuthorized(
                    "You are not authorized. Please contact with @hikamoru"
                )
        return response
