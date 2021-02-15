import logging
import datetime

import discord

from gothbot.handlers.base import BaseHandler

logger = logging.getLogger(__name__)


class RepeatHandler(BaseHandler):
    """
    If user string matches regex, repeat message back to user
    """

    def __init__(
        self, pattern, name="RepeatHandler", cooldown_enabled=True, cooldown_minutes=3
    ):
        super().__init__()
        self.name = name
        self.pattern = pattern

        self.cooldown_enabled = cooldown_enabled
        self.cooldown_ends_at = None
        self.cooldown_minutes = cooldown_minutes

    async def handle(self, message: discord.Message):
        # Are we on cooldown?

        if self.cooldown_enabled:
            if (
                self.cooldown_ends_at is not None
                and self.cooldown_ends_at > datetime.datetime.now()
            ):
                logger.debug(
                    f"{self.name} not handling matched message '{message.content}' due to cooldown"
                )
                return

        # We aren't on cooldown or its not enabled
        await message.channel.send(message.content)
        logger.debug(f"{self.name} handled matched message '{message.content}'")

        if self.cooldown_enabled:
            # Set cooldown for COOLDOWN_MINUTES from now
            self.cooldown_ends_at = datetime.datetime.now() + datetime.timedelta(
                minutes=self.cooldown_minutes
            )
