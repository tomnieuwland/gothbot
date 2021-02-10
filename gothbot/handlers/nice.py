import logging
import datetime

import discord

from gothbot.handlers.base import BaseHandler

logger = logging.getLogger(__name__)


class NiceHandler(BaseHandler):
    """
    If the user types nice, or similar, they get a nice back
    """

    def __init__(self):
        super().__init__()
        self.name = "NiceHandler"
        self.keywords = ["nice", "nice.", "Nice", "Nice.", "NICE"]

        self.cooldown = None

        self.COOLDOWN_MINUTES = 3

    async def handle(self, message: discord.Message):
        # Are we on cooldown?
        if self.cooldown is not None and self.cooldown > datetime.datetime.now():
            logger.debug("Not nicing, on cooldown")
            return
        # We aren't on cooldown
        logger.debug("Nice.")
        await message.channel.send(message.content)

        # Set cooldown for COOLDOWN_MINUTES from now
        self.cooldown = datetime.datetime.now() + datetime.timedelta(
            minutes=self.COOLDOWN_MINUTES
        )
        return
