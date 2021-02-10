import abc
from typing import List, Tuple, Union

import discord


class BaseCommandModule(abc.ABC):
    def __init__(self):
        self.name = "BaseHandler"
        self.keywords = ""
        self.description = ""

    async def handle(self, message: discord.Message):
        # Implement something here to handle the message
        pass

    def generate_help_embed(
        self,
        *,
        title: str,
        description: str,
        aliases: Union[List[str], None],
        commands: Union[List[Tuple[str, str]], None],
    ) -> discord.Embed:
        help_embed = discord.Embed(title=title, type="rich", description=description)
        if aliases:
            help_embed.add_field(
                name="Aliases",
                value=", ".join(map(lambda alias: f"`{alias}`", sorted(aliases))),
                inline=False,
            )

        if commands:
            help_embed.add_field(
                name="Commands",
                value="\n".join(
                    map(
                        lambda command_tuple: f"`{command_tuple[0]}`\t--\t{command_tuple[1]}",
                        sorted(commands, key=lambda command: command[0]),
                    )
                ),
                inline=False,
            )
        return help_embed
