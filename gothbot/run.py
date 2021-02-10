import argparse
import logging

from dotenv import dotenv_values

from bot import GothBot

from handlers.nice import NiceHandler

from command_modules.minecraft import MinecraftCommandModule

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    config = dotenv_values("../.env")

    if config.get("verbose"):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    special_handlers = [NiceHandler()]

    command_modules = []

    if config.get("MINECRAFT_HOST") and config.get("MINECRAFT_PORT"):
        command_modules.append(
            MinecraftCommandModule(
                minecraft_host=config.get("MINECRAFT_HOST"),
                minecraft_port=config.get("MINECRAFT_PORT"),
                command_prefix=config["COMMAND_PREFIX"],
            )
        )
    else:
        logger.warning("Missing minecraft info, not initialising")

    client = GothBot(command_prefix=config["COMMAND_PREFIX"])

    for handler_instance in special_handlers:
        client.register_special_handler(handler_instance)

    for command_module_instance in command_modules:
        client.register_command_module(command_module_instance)

    client.run(config["DISCORD_TOKEN"])
