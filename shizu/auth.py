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


import configparser as cp
import asyncio
import logging
import base64
import sys
import os

from datetime import datetime
from getpass import getpass
from typing import NoReturn, Tuple, Union

from pyrogram import Client, errors, types, raw
from pyrogram.session.session import Session
from pyrogram.raw.functions.auth.export_login_token import ExportLoginToken

from telethon import TelegramClient

from qrcode.main import QRCode
from . import utils

Session.notice_displayed: bool = True


def colored_input(prompt: str = "", hide: bool = False) -> str:
    frame = sys._getframe(1)
    return (getpass if hide else input)(
        "\x1b[32m{time:%Y-%m-%d %H:%M:%S}\x1b[0m | "
        "\x1b[1m{level: <8}\x1b[0m | "
        "\x1b[36m{name}\x1b[0m:\x1b[36m{function}\x1b[0m:\x1b[36m{line}\x1b[0m - \x1b[1m{prompt}\x1b[0m".format(
            time=datetime.now(),
            level="INPUT",
            name=frame.f_globals["__name__"],
            function=frame.f_code.co_name,
            line=frame.f_lineno,
            prompt=prompt,
        )
    )


class Auth:
    def __init__(self, session_name: str = "../shizu") -> None:
        self._check_api_tokens()

        cfg = cp.ConfigParser()
        cfg.read("./config.ini")

        try:
            device_model = cfg["pyrogram"]["device_model"]
        except KeyError:
            device_model = utils.get_random_smartphone()

            cfg["pyrogram"]["device_model"] = device_model

            with open("./config.ini", "w", encoding="utf-8") as file:
                cfg.write(file)

        self.app = Client(
            name=session_name,
            api_id=cfg.get("pyrogram", "api_id"),
            api_hash=cfg.get("pyrogram", "api_hash"),
            device_model=device_model,
            session_string=(
                cfg.get("pyrogram", "string_session")
                if "JAMHOST" in os.environ
                else None
            ),
        )

        if utils.is_tl_enabled():
            self.tapp = TelegramClient(
                "shizu-tl",
                api_id=cfg.get("pyrogram", "api_id"),
                api_hash=cfg.get("pyrogram", "api_hash"),
                device_model="Shizu-TL",
            )

    def _check_api_tokens(self) -> bool:
        cfg = cp.ConfigParser()
        if not cfg.read("./config.ini"):
            cfg["pyrogram"] = {
                "api_id": colored_input("Enter API ID: "),
                "api_hash": colored_input("Enter API hash: "),
                "device_model": utils.get_random_smartphone(),
            }
            with open("./config.ini", "w", encoding="utf-8") as file:
                cfg.write(file)

        return True

    async def send_code(self) -> Tuple[str, str]:
        while True:
            error_text: str = ""
            try:
                phone = colored_input("Enter phone number: ")
                return phone, (await self.app.send_code(phone)).phone_code_hash
            except errors.PhoneNumberInvalid:
                error_text = "Invalid phone number, please try again"
            except errors.PhoneNumberBanned:
                error_text = "Phone number is banned"
            except errors.PhoneNumberFlood:
                error_text = "Phone number is flood protected"
            except errors.PhoneNumberUnoccupied:
                error_text = "Phone number is not registered"
            except errors.BadRequest as error:
                error_text = f"An unknown error occurred: {error}"
            if error_text:
                logging.error(error_text)

    async def enter_code(
        self, phone: str, phone_code_hash: str
    ) -> Union[types.User, bool]:
        try:
            code = colored_input("Enter confirmation code: ")
            return await self.app.sign_in(phone, phone_code_hash, code)
        except errors.SessionPasswordNeeded:
            return False

    async def enter_2fa(self) -> types.User:
        while True:
            try:
                passwd = colored_input(
                    "Enter two-factor authentication password: ", True
                )
                return await self.app.check_password(passwd)
            except errors.BadRequest:
                logging.error("Incorrect password, please try again")

    async def authorize(self) -> Union[Tuple[types.User, Client], NoReturn]:
        await self.app.connect()
        try:
            me = await self.app.get_me()
        except errors.AuthKeyUnregistered:
            cfg = cp.ConfigParser()
            cfg.read("config.ini")
            qr = colored_input("Login with QR-CODE? y/n").lower().split()
            if qr[0] == "y":
                api_id = int(cfg.get("pyrogram", "api_id"))
                api_hash = cfg.get("pyrogram", "api_hash")
                tries = 0
                while True:
                    try:
                        r = await self.app.invoke(
                            ExportLoginToken(
                                api_id=api_id, api_hash=api_hash, except_ids=[]
                            )
                        )
                    except errors.exceptions.unauthorized_401.SessionPasswordNeeded:
                        me: types.User = (
                            await self.app.get_me()
                            if logged
                            else await self.enter_2fa()
                        )
                        break
                    if isinstance(
                        r, raw.types.auth.login_token_success.LoginTokenSuccess
                    ):
                        break
                    if (
                        isinstance(r, raw.types.auth.login_token.LoginToken)
                        and tries % 30 == 0
                    ):
                        print("Scan QR code below:")
                        qr = QRCode(error_correction=1)
                        qr.add_data(
                            f"tg://login?token={base64.urlsafe_b64encode(r.token).decode('utf-8').rstrip('=')}"
                        )
                        qr.make(fit=True)
                        qr.print_ascii()
                    tries += 1
                    await asyncio.sleep(1)
            else:
                phone, phone_code_hash = await self.send_code()
                logged = await self.enter_code(phone, phone_code_hash)

                me: types.User = (
                    await self.app.get_me() if logged else await self.enter_2fa()
                )

                if "JAMHOST" in os.environ:
                    cfg["pyrogram"][
                        "string_session"
                    ] = await self.app.export_session_string()
                    with open("./config.ini", "w", encoding="utf-8") as file:
                        cfg.write(file)

        except errors.SessionRevoked:
            logging.error(
                "Session has been revoked, delete the session and run the start command again"
            )
            await self.app.disconnect()
            return sys.exit(64)

        if utils.is_tl_enabled():
            return me, self.app, self.tapp

        return me, self.app, None
