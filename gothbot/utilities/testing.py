import os

from unittest.mock import create_autospec, AsyncMock

from discord import Message


def create_mock_discord_message():
    message = create_autospec(Message)
    message.channel.send = AsyncMock()
    return message


def prefix_command(command):
    return f'{os.environ["COMMAND_PREFIX"]} {command}'
