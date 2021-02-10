import logging
import re

import discord

from command_modules.base import BaseCommandModule
from handlers.base import BaseHandler

logger = logging.getLogger(__name__)


class GothBot(discord.Client):
    def __init__(self, *args, **kwargs):
        self.command_modules = {}
        self.special_handlers = {}
        self._command_modules_list = []

        self.COMMAND_PREFIX = "!gh"

        super().__init__(*args, **kwargs)

    async def on_ready(self):
        logger.info(f"Logged in as {self.user.name} (id={self.user.id})")
        logger.info("Ready!")

    async def on_message(self, message: discord.Message):
        # Always ignore messages sent by the bot
        if message.author == self.user:
            return

        if message.content == "!gh" or message.content == "!gh help":
            await self._handle_help(message.channel)

        elif message.content.startswith(self.COMMAND_PREFIX):
            # If a message starts with the command prefix, try to pass it off to a command module
            logger.info(
                f"Received command {message.content} from {message.author.name}"
            )
            pattern = r"!gh ([A-z]*).*"
            re_search = re.search(pattern, message.content)

            if re_search is not None:
                command_module_keyword = re_search.group(1)
                command_module = self.command_modules.get(command_module_keyword)

                if command_module is not None:
                    await command_module.handle(message)
                    return
            await message.channel.send("Unknown command.")

        elif message.content in self.special_handlers.keys():
            # One of our special handlers wants to deal with this message
            await self.special_handlers.get(message.content).handle(message)

    def register_command_module(self, module_instance: BaseCommandModule):
        logger.info(f'Registering command module "{module_instance.name}"')
        for keyword in module_instance.keywords:
            existing_command_module = self.command_modules.get(keyword)
            if existing_command_module is not None:
                raise RuntimeError(
                    f'{module_instance.name} tried to register keyword "{keyword}", but this keyword is already registered by {existing_command_module.name}'
                )
            else:
                self.command_modules[keyword] = module_instance

        self._command_modules_list.append(module_instance)

    def register_special_handler(self, handler_instance: BaseHandler):
        logger.info(f'Registering special handler "{handler_instance.name}"')
        for keyword in handler_instance.keywords:
            existing_handler = self.special_handlers.get(keyword)
            if existing_handler is not None:
                raise RuntimeError(
                    f'{handler_instance.name} tried to register keyword "{keyword}", but this keyword is already registered by {existing_handler.name}'
                )
            else:
                self.special_handlers[keyword] = handler_instance

    async def _handle_help(self, channel: discord.TextChannel):
        help_embed = discord.Embed(
            title="Gothbot Help",
            type="rich",
            description="Use `!gh` with one of the following sub commands (ie `!gh <subcommand>`)",
        )

        module_tuples = []

        for command_module in sorted(
            self._command_modules_list, key=lambda module: module.keywords[0]
        ):
            module_tuples.append(
                (
                    ", ".join(
                        map(lambda keyword: f"`{keyword}`", command_module.keywords)
                    ),
                    command_module.description,
                )
            )

        help_embed.add_field(
            name="Commands",
            value="\n".join(
                map(
                    lambda module_tuple: f"{module_tuple[0]}\t--\t{module_tuple[1]}",
                    module_tuples,
                )
            ),
            inline=False,
        )

        await channel.send(embed=help_embed)
