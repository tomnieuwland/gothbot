import datetime
from unittest import IsolatedAsyncioTestCase

from gothbot.handlers.repeat import RepeatHandler
from gothbot.utilities.testing import create_mock_discord_message


class TestRepeatorHandler(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.handler = RepeatHandler("testpattern")

    async def test_handle(self):
        # Setup
        message = create_mock_discord_message()

        # Tests that the nice handler just spits back whatever it is told to handle (which should be a keyword)
        message.content = "test"

        await self.handler.handle(message)

        # Using the send method on discord.message.Message, the handled message should be "sent"
        message.channel.send.assert_awaited_once_with("test")

    async def test_cooldown(self):
        # Setup
        message = create_mock_discord_message()

        message.content = "test"

        self.assertIsNone(self.handler.cooldown_ends_at)
        await self.handler.handle(message)
        # Using the send method on discord.message.Message, the handled message should be "sent"
        message.channel.send.assert_awaited_once()

        # If we try and handle on cooldown, no message should be sent
        await self.handler.handle(message)
        # Total awaits should still be one
        message.channel.send.assert_awaited_once()

        # Simulate cooldown passing
        self.handler.cooldown_ends_at = datetime.datetime.now() - datetime.timedelta(
            minutes=self.handler.cooldown_minutes + 1
        )
        await self.handler.handle(message)
        # Total awaits should now be two because handler is off cooldown
        self.assertEqual(message.channel.send.await_count, 2)
