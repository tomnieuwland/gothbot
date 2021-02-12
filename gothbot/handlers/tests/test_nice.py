import datetime
from unittest import IsolatedAsyncioTestCase

from gothbot.handlers.nice import NiceHandler
from gothbot.utilities.testing import create_mock_discord_message


class TestNiceHandler(IsolatedAsyncioTestCase):
    async def test_handle(self):
        # Setup
        handler = NiceHandler()
        message = create_mock_discord_message()

        # Tests that the nice handler just spits back whatever it is told to handle (which should be a keyword)
        message.content = "test"

        await handler.handle(message)

        # Using the send method on discord.message.Message, the handled message should be "sent"
        message.channel.send.assert_awaited_once_with("test")

    async def test_cooldown(self):
        # Setup
        handler = NiceHandler()
        message = create_mock_discord_message()

        message.content = "test"

        self.assertIsNone(handler.cooldown)
        await handler.handle(message)
        # Using the send method on discord.message.Message, the handled message should be "sent"
        message.channel.send.assert_awaited_once()

        # If we try and handle on cooldown, no message should be sent
        await handler.handle(message)
        # Total awaits should still be one
        message.channel.send.assert_awaited_once()

        # Simulate cooldown passing
        handler.cooldown = datetime.datetime.now() - datetime.timedelta(
            minutes=handler.COOLDOWN_MINUTES + 1
        )
        await handler.handle(message)
        # Total awaits should now be two because handler is off cooldown
        self.assertEqual(message.channel.send.await_count, 2)
