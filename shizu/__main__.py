import asyncio
import sys
import os
import logging

if sys.version_info < (3, 7, 0):
    print("🚫 Error: you are using Python version < 3.7")
    sys.exit(1)

elif __package__ != "shizu":
    print("🚫 Error: you cannot run this as a script; you must execute as a package")
    sys.exit(1)

else:
    try:
        import pyrogram
        from .version import __version__
        from . import main
        from .logger import setup_logger

        setup_logger("INFO")

        banner = (
            "\n█▀ █ █ █ ▀█ █ █"
            "\n▄█ █▀█ █ █▄ █▄█\n\n"
            f"🐙 Shuzu v{__version__} is starting...\n"
            f"🐍 Python v{sys.version}\n"
            f"👾 Pyrogram v{pyrogram.__version__}\n"
            "🤝 Support chat: @shizu_talks\n"
        )
        logging.info(banner)
        asyncio.run(main.main())
    except ModuleNotFoundError as module:
        print(f"🚫 Error: {module} is not installed")
        print(
            "🔁 Trying to install it automatically...\n"
            "⌛ Attempting dependencies installation... Just wait."
        )
        os.popen("pip3 install -r requirements.txt").read()
        print("👍 Dependencies installed")
        print("🔁 Retrying to run bot again please wait..")
