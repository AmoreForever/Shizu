import asyncio
import sys
import os
import logging
import platform


try:
    import pyrogram
    from .version import __version__
    from . import main
    from .logger import setup_logger

    setup_logger("INFO")

    banner = (
        "\n█▀ █ █ █ ▀█ █ █"
        "\n▄█ █▀█ █ █▄ █▄█\n\n"
        f"🐙 Shuzu v{'.'.join(map(str, __version__))} is starting...\n"
        f"🐍 Python v{platform.python_version()}\n"
        f"👾 Pyrogram v{pyrogram.__version__}\n"
        "🤝 Support chat: @shizu_talks\n"
    )
    logging.info(banner)
    asyncio.run(main.main())
except ModuleNotFoundError as module:
    print(f"🚫 Error: {module} is not installed")
    print(
        "⌛ Attempting dependencies installation... Just wait."
    )
    os.popen("pip3 install -r requirements.txt").read()
    print("👍 Dependencies installed")
    print("🔁 Retry to run bot again please wait..")
