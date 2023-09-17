import asyncio
import functools
import random
import string
import typing
import logging
import os
import contextlib
import aiohttp
from types import FunctionType
from typing import Any, List, Literal, Tuple, Union

# from . import __main__

from pyrogram.types import Chat, Message, User
from pyrogram import Client

from . import database

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("shizu.log"),
    ],
)

db = database.db


def get_full_command(
    message: Message,
) -> Union[Tuple[Literal[""], Literal[""], Literal[""]], Tuple[str, str, str]]:
    """Output tuple from prefix, command and arguments

    Parameters:
        message (``program.types.Message`):
    Message
    """
    message.text = str(message.text or message.caption)
    prefixes = database.db.get("shizu.loader", "prefixes", ["."])

    for prefix in prefixes:
        if (
            message.text
            and len(message.text) > len(prefix)
            and message.text.startswith(prefix)
        ):
            command, *args = message.text[len(prefix) :].split(maxsplit=1)
            break
    else:
        return "", "", ""

    return prefixes[0], command.lower(), args[-1] if args else ""


def get_args(message: typing.Union[Message, str]) -> str:
    """
    Get arguments from message.
    """
    if not (message := getattr(message, "text", message)):
        return ""

    args = message.split()[1:]
    return " ".join(args) if args else ""


def get_args_raw(message: typing.Union[Message, str]) -> str:
    """
    Get the parameters to the command as a raw string (not split)
    :param message: Message or string to get arguments from
    :return: Raw string of arguments
    """
    if not (message := getattr(message, "text", message)):
        return False

    return args[1] if len(args := message.split(maxsplit=1)) > 1 else ""


def get_args_html(message: typing.Union[Message, str]) -> str:
    """
    Get arguments from message in html format.
    """
    try:
        args = message.text.html.split(maxsplit=1)[1]
    except Exception:
        args = ""

    return args


async def invite_bot(app: Client, chat):
    """
    Invite the bot to the chat.
    """
    await app.add_chat_members(chat, [db.get("shizu.bot", "username")])


async def create_chat(
    app: Client,
    title: str = None,
    description=None,
    supergroup: bool = False,
    inline_bot: bool = False,
    promote: bool = False,
):
    """
    Create a chat in the Telegram app.

    Parameters:
    - app (Client): The Telegram client used to create the chat.
    - title (str): The title of the chat.
    - description (str, optional): The description of the chat. Defaults to None.
    - supergroup (bool, optional): Indicates if the chat is a supergroup. Defaults to False.
    - inline_bot (bool, optional): Indicates if the chat is an inline bot. Defaults to False.
    - promote (bool, optional): Indicates if the chat bot should be promoted to an administrator. Defaults to False.

    Returns:
    - chat: The created chat object.
    """

    chat = None
    title = f"shizu-{random_id(10)}" if title is None else title
        

    if not supergroup:
        chat = await app.create_group(title, "me",)
    else:
        if description is None:
            description = "This is a supergroup created by Shizu"
        chat = await app.create_supergroup(title, description)

    if inline_bot:
        bot = db.get("shizu.bot", "username")
        await app.add_chat_members(chat.id, [bot])

        if promote:
            await app.promote_chat_member(chat.id, bot)
            await app.set_administrator_title(chat.id, bot, "Shizu Inline")

    return chat


async def answer(
    message: Union[Message, List[Message]],
    response: Union[str, Any],
    chat_id: Union[str, int] = None,
    doc: bool = False,
    photo: bool = False,
    **kwargs,
) -> List[Message]:
    """Basically it's a regular message.edit, but:
        - If the message content exceeds the limit (4096 characters),
            then several split messages will be sent
        - Message.reply works if the command was not called by the account owner

    Parameters:
        message (``program.types.Message`` | ``typing.List[pyrogram.types.Message]`):
    Message

        response (`str` | `typing.Any"):
    The text or object to be sent

        chat_id (`str` | `int`, optional):
    Chat to send a message to

        doc/photo (`bool", optional):
    If `True`, the message will be sent as a document/photo or by link

        **kwargs (`dict`, optional):
    Parameters for sending a message
    """
    messages: List[Message] = []
    app: Client = message._client

    if isinstance(message, list):
        message = message[0]

    if isinstance(response, str) and not any([doc, photo]):
        outputs = [response[i : i + 4096] for i in range(0, len(response), 4096)]
        if chat_id:
            messages.append(
                await message._client.send_message(chat_id, outputs[0], **kwargs)
            )
        else:
            messages.append(
                await (
                    message.edit
                    if message.from_user.id == db.get("shizu.me", "me")
                    else message.reply
                )(outputs[0], **kwargs)
            )
        for output in outputs[1:]:
            messages.append(await messages[0].reply(output, **kwargs))

    elif doc:
        app.me = await app.get_me()
        if chat_id:
            messages.append(
                await message._client.send_document(chat_id, response, **kwargs)
            )
        else:
            messages.append(await message.reply_document(response, **kwargs))

    elif photo:
        app.me = await app.get_me()
        if chat_id:
            messages.append(
                await message._client.send_photo(chat_id, response, **kwargs)
            )
        else:
            await message.delete() 
            messages.append(await message.reply_photo(response, **kwargs))

    return messages[0]


async def answer_inline(
    message: Union[Message, List[Message]],
    query: str,
    chat_id: Union[str, int] = "",
) -> None:
    """
    Parameters:
        message (``program.types.Message`` | ``typing.List[pyrogram.types.Message]`):
    Message

            query (`str"):
    Parameters for the inline bot

            chat_id (`str` | `int`, optional):
    The chat to send the inline result to
    """

    if isinstance(message, list):
        message = message[0]

    app: Client = message._client
    message: Message

    results = await app.get_inline_bot_results((await app.inline_bot.get_me()).username, query)

    await app.send_inline_bot_result(
        chat_id or message.chat.id, results.query_id, results.results[0].id
    )


def run_sync(func: FunctionType, *args, **kwargs) -> asyncio.Future:
    """Runs asynchronously non-asink function

    Parameters:
            func (`types.FunctionType`):
    Function to run

            args (`list`):
    Arguments to the function

            kwargs (`dict`):
    Parameters to the function
    """
    return asyncio.get_event_loop().run_in_executor(
        None, functools.partial(func, *args, **kwargs)
    )


def get_display_name(entity: Union[User, Chat]) -> str:
    """Получить отображаемое имя

    Параметры:
        entity (``pyrogram.types.User`` | ``pyrogram.types.Chat``):
            Сущность, для которой нужно получить отображаемое имя
    """
    return (
        getattr(entity, "title", None)
        or entity.first_name
        or ("" + (f" {entity.last_name}" if entity.last_name else ""))
    )


def get_ram() -> float:
    """Возвращает данные о памяти."""
    try:
        import psutil

        process = psutil.Process(os.getpid())
        mem = process.memory_info()[0] / 2.0**20
        for child in process.children(recursive=True):
            mem += child.memory_info()[0] / 2.0**20
        return round(mem, 1)
    except:
        return 0


def get_cpu() -> float:
    """Возвращает данные о процессоре."""
    try:
        import psutil

        process = psutil.Process(os.getpid())
        cpu = process.cpu_percent()
        for child in process.children(recursive=True):
            cpu += child.cpu_percent()
        return round(cpu, 1)
    except:
        return 0


def get_platform() -> str:
    """Возращает платформу."""
    IS_TERMUX = "com.termux" in os.environ.get("PREFIX", "")
    IS_DOCKER = "DOCKER" in os.environ
    IS_WIN = "WINDIR" in os.environ
    IS_WSL = False

    with contextlib.suppress(Exception):
        from platform import uname

        if "microsoft-standard" in uname().release:
            IS_WSL = True

    if IS_TERMUX:
        platform = "📱 Termux"
    elif IS_DOCKER:
        platform = "🐳 Docker"
    elif IS_WSL:
        platform = "🧱 WSL"
    elif IS_WIN:
        platform = "💻 Windows"
    else:
        platform = "🖥️ VDS"

    return platform


def random_id(size: int = 10) -> str:
    """Returns a random identifier of the specified length

    Параметры:
        size (``int``, optional):
            length of the identifier
    """
    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(size)
    )


def get_random_hex() -> str:
    """Returns a random hex color"""
    return "#%06x" % random.randint(0, 0xFFFFFF)


async def paste_neko(code: str):
    try:
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)
        ) as session:
            async with session.post(
                "https://nekobin.com/api/documents",
                json={"content": code},
            ) as paste:
                paste.raise_for_status()
                result = await paste.json()
    except Exception:
        return "Pasting failed"
    else:
        return f"nekobin.com/{result['result']['key']}.py"
