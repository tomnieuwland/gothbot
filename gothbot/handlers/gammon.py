import logging
import datetime

import discord

from gothbot.handlers.base import BaseHandler

logger = logging.getLogger(__name__)


class gammonHandler(BaseHandler):
    """
    IWhenever gammon types a message he gets handled, max once every hour
    """

    def __init__(self):
        super().__init__()
        self.name = "gammonHandler"
        self.cooldown = None
        self.COOLDOWN_MINUTES = 60

    async def handle(self, message: discord.Message):
        # Are we on cooldown?
        if self.cooldown is not None and self.cooldown > datetime.datetime.now():
            logger.debug("On cooldown for gammon handler")
            return
        
        elif (message.author.id == 193272940739952640):         # We aren't on cooldown and gammon sent message
            logger.debug("gammon is handled")
            await message.channel.send("Get handled Gammon:soy: Gammon is a :soy: confirmed by artificial intelligence")

        
        

        # Set cooldown for COOLDOWN_MINUTES from now
        self.cooldown = datetime.datetime.now() + datetime.timedelta(
            minutes=self.COOLDOWN_MINUTES
        )