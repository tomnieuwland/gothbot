from unittest import IsolatedAsyncioTestCase, mock
from unittest.mock import patch

from mcstatus import MinecraftServer

from gothbot.command_modules.minecraft import MinecraftCommandModule
from gothbot.utilities.testing import create_mock_discord_message, prefix_command

mock_error = mock.Mock()
mock_error.side_effect = Exception


class TestMinecraftCommandModule(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.module = MinecraftCommandModule(
            minecraft_host="fakehost", minecraft_port=25565
        )
        self.message = create_mock_discord_message()

    @patch.object(MinecraftCommandModule, "_handle_help")
    async def test_handle_no_command(self, mock_handle_help):
        # Test that when handle is called with no command, the help handler is called
        self.message.content = prefix_command("minecraft")

        await self.module.handle(self.message)

        mock_handle_help.assert_awaited_once()

    @patch.object(MinecraftCommandModule, "_handle_help")
    async def test_handle_help(self, mock_handle_help):
        # Test that when handle is called with help command, the help handler is called
        self.message.content = prefix_command("minecraft help")

        await self.module.handle(self.message)

        mock_handle_help.assert_awaited_once()

    @patch.object(MinecraftServer, "ping")
    async def test_handle_ping(self, mock_ping):
        # Test that when handle is called with ping command, the ping handler is called, and the right message is sent
        self.message.content = prefix_command("minecraft ping")
        mock_ping.return_value = 1

        await self.module.handle(self.message)

        # We attempt to call mcstatus.MinecraftServer.ping
        mock_ping.assert_called_once()

        # We return the correct message with the latency given
        self.message.channel.send.assert_awaited_once_with(
            "`fakehost` is up and replied in 1 ms"
        )

    @patch.object(MinecraftServer, "ping", mock_error)
    async def test_handle_bad_ping(self):
        # Test that when ping fails, the exception is caught and the right message is sent
        self.message.content = prefix_command("minecraft ping")

        await self.module.handle(self.message)

        # We return the correct message with the latency given
        self.message.channel.send.assert_awaited_once_with(
            "`fakehost` appears to be down"
        )

    async def test_handle_ip(self):
        # Test that when the ip command is used, the right string is returned
        # Default minecraft port
        self.message.content = prefix_command("minecraft ip")
        await self.module.handle(self.message)
        self.message.channel.send.assert_awaited_with(
            "The current minecraft ip is `fakehost`"
        )

        # Non standard minecraft port
        non_standard_module = MinecraftCommandModule(
            minecraft_host="fakehost", minecraft_port=1111
        )
        await non_standard_module.handle(self.message)
        self.message.channel.send.assert_awaited_with(
            "The current minecraft ip is `fakehost:1111`"
        )

    @patch.object(MinecraftServer, "query")
    async def test_handle_players(self, mock_query):
        # Test that when the players command is used, the right string is returned
        # Has Players
        self.message.content = prefix_command("minecraft players")
        mock_query.return_value.players.names = ["foo", "bar"]

        await self.module.handle(self.message)

        self.message.channel.send.assert_awaited_with(
            "`fakehost` has the following players online: foo, bar"
        )

        # No players
        mock_query.return_value.players.names = []

        await self.module.handle(self.message)

        self.message.channel.send.assert_awaited_with(
            "`fakehost` has no players online"
        )

    @patch.object(MinecraftServer, "query", mock_error)
    async def test_handle_bad_players(self):
        # Test that when the players command is used, and the query fails, the exception is handled
        self.message.content = prefix_command("minecraft players")
        await self.module.handle(self.message)
        self.message.channel.send.assert_awaited_with(
            "Could not fetch players for `fakehost`"
        )
