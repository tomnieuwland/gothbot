import argparse
import logging
import os

from dotenv import load_dotenv

from bot import GothBot

from handlers.nice import NiceHandler

from command_modules.minecraft import MinecraftCommandModule

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Loads environment variables from .env in root directory where available
    load_dotenv("../.env")

    if os.environ.get("verbose"):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    special_handlers = [NiceHandler()]

    command_modules = []

    if os.environ.get("MINECRAFT_HOST") and os.environ.get("MINECRAFT_PORT"):
        command_modules.append(
            MinecraftCommandModule(
                minecraft_host=os.environ.get("MINECRAFT_HOST"),
                minecraft_port=os.environ.get("MINECRAFT_PORT"),
                command_prefix=os.environ["COMMAND_PREFIX"],
            )
        )
    else:
        logger.warning("Missing minecraft info, not initialising")

    client = GothBot(command_prefix=os.environ["COMMAND_PREFIX"])

    for handler_instance in special_handlers:
        client.register_special_handler(handler_instance)

    for command_module_instance in command_modules:
        client.register_command_module(command_module_instance)

    client.run(os.environ["DISCORD_TOKEN"])
