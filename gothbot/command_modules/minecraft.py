import logging
import os

import discord
from mcstatus import MinecraftServer

from command_modules.base import BaseCommandModule

logger = logging.getLogger(__name__)


class MinecraftCommandModule(BaseCommandModule):
    def __init__(self, *, minecraft_host: str, minecraft_port: int):
        super().__init__()
        self.name = "MinecraftCommandModule"
        self.keywords = ["minecraft", "mc"]
        self.description = "Minecraft related commands for Gothbot"
        self.help_embed = self.generate_help_embed(
            title="Gothbot Minecraft Module",
            description=self.description,
            aliases=self.keywords,
            commands=[
                ("help", "Prints this help box"),
                ("ping", "Checks if minecraft server is up"),
                ("players", "Checks who is online"),
                ("ip", "Prints the current IP for the server"),
            ],
        )

        self.command_prefix = os.environ["COMMAND_PREFIX"]
        self.host = minecraft_host
        self.port = minecraft_port
        self.ip_string = self.host if self.port == 25565 else f"{self.host}:{self.port}"
        self.server = MinecraftServer(self.host, self.port)

    async def handle(self, message: discord.Message):
        segments = message.content.split(" ", 3)

        if len(segments) == 2:
            await self._handle_help(message.channel)
            return

        command = segments.pop()

        if command == "help":
            await self._handle_help(message.channel)
        elif command == "ping":
            await self._handle_ping(message.channel)
        elif command == "ip":
            await self._handle_ip(message.channel)
        elif command == "players":
            await self._handle_players(message.channel)
        else:
            await message.channel.send(
                f"Unknown command. Type `{self.command_prefix} {self.keywords[0]} help` to see available commands"
            )

    async def _handle_help(self, channel: discord.TextChannel):
        logger.debug("Handling minecraft help request")
        await channel.send(embed=self.help_embed)

    async def _handle_ping(self, channel: discord.TextChannel):
        logger.debug("Handling minecraft ping request")
        message = f"`{self.ip_string}` appears to be down"
        try:
            latency = self.server.ping()
            message = f"`{self.ip_string}` is up and replied in {latency} ms"
        except Exception:
            pass

        await channel.send(message)

    async def _handle_ip(self, channel: discord.TextChannel):
        logger.debug("Handling minecraft ip request")
        await channel.send(f"The current minecraft ip is `{self.ip_string}`")

    async def _handle_players(self, channel: discord.TextChannel):
        logger.debug("Handling minecraft player request")
        message = f"Could not fetch players for `{self.ip_string}`"
        try:
            query = self.server.query()
            if query.players.names:
                message = f"`{self.ip_string}` has the following players online: {', '.join(query.players.names)}"
            else:
                message = f"`{self.ip_string}` has no players online"
        except Exception:
            pass

        await channel.send(message)
