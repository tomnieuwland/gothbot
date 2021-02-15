import argparse
import logging
import os

from dotenv import load_dotenv

from bot import GothBot

from handlers.repeat import RepeatHandler

from command_modules.minecraft import MinecraftCommandModule

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Loads environment variables from .env in root directory where available
    load_dotenv("../.env")

    if os.environ.get("verbose"):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    regex_handlers = [
        RepeatHandler(
            r"^[nN]\s{0,2}[iI]\s{0,2}[cC]\s{0,2}[eE]\s{0,2}[!?]*$", name="NiceHandler"
        ),
        RepeatHandler(r"^fuck$", name="FuckHandler", cooldown_minutes=60),
    ]

    command_modules = []

    if os.environ.get("MINECRAFT_HOST") and os.environ.get("MINECRAFT_PORT"):
        command_modules.append(
            MinecraftCommandModule(
                minecraft_host=os.environ.get("MINECRAFT_HOST"),
                minecraft_port=int(os.environ.get("MINECRAFT_PORT")),
            )
        )
    else:
        logger.warning("Missing minecraft info, not initialising")

    client = GothBot(command_prefix=os.environ["COMMAND_PREFIX"])

    for handler_instance in regex_handlers:
        client.register_regex_handler(handler_instance)

    for command_module_instance in command_modules:
        client.register_command_module(command_module_instance)

    client.run(os.environ["DISCORD_TOKEN"])
