import argparse
import logging

from bot import GothBot

from handlers.nice import NiceHandler

from command_modules.minecraft import MinecraftCommandModule

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="GothBot")
    parser.add_argument("-t", "--token", type=str, help="Discord token", required=True)
    parser.add_argument("-v", "--verbose", action="store_true")

    parsed_args = parser.parse_args()

    if parsed_args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    special_handlers = [NiceHandler()]

    command_modules = [
        MinecraftCommandModule(
            minecraft_host="mc.gothhunters.xyz", minecraft_port=25565
        )
    ]

    client = GothBot()

    for handler_instance in special_handlers:
        client.register_special_handler(handler_instance)

    for command_module_instance in command_modules:
        client.register_command_module(command_module_instance)

    client.run(parsed_args.token)
