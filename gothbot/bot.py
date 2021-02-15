import logging
import re

import discord

from command_modules.base import BaseCommandModule
from handlers.base import BaseHandler

logger = logging.getLogger(__name__)


class GothBot(discord.Client):
    def __init__(self, *args, command_prefix, **kwargs):
        self.command_modules = {}
        self._command_modules_list = []

        self.regex_handlers = []

        self.COMMAND_PREFIX = command_prefix

        super().__init__(*args, **kwargs)

    async def on_ready(self):
        logger.info(f"Logged in as {self.user.name} (id={self.user.id})")
        logger.info("Ready!")

    async def on_message(self, message: discord.Message):
        # Always ignore messages sent by the bot
        if message.author == self.user:
            return

        elif (
            message.content == self.COMMAND_PREFIX
            or message.content == f"{self.COMMAND_PREFIX} help"
        ):
            await self._handle_help(message.channel)

        elif message.content.startswith(self.COMMAND_PREFIX):
            # If a message starts with the command prefix, try to pass it off to a command module
            logger.info(
                f"Received command {message.content} from {message.author.name}"
            )
            pattern = f"{self.COMMAND_PREFIX} ([A-z]*).*"
            re_search = re.search(pattern, message.content)

            if re_search is not None:
                command_module_keyword = re_search.group(1)
                command_module = self.command_modules.get(command_module_keyword)

                if command_module is not None:
                    await command_module.handle(message)
                    return
            await message.channel.send("Unknown command.")

        else:
            for re_handler in self.regex_handlers:
                match = re.search(re_handler.pattern, message.content)
                if match:
                    await re_handler.handle(message)
                    # We don't need to keep searching
                    break

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

    def register_regex_handler(self, handler_instance: BaseHandler):
        logger.info(f'Registering regex handler "{handler_instance.name}"')
        self.regex_handlers.append(handler_instance)

    async def _handle_help(self, channel: discord.TextChannel):
        help_embed = discord.Embed(
            title="Gothbot Help",
            type="rich",
            description=f"Use `{self.COMMAND_PREFIX}` with one of the following sub commands (ie `{self.COMMAND_PREFIX} <subcommand>`)",
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
