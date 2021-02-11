import logging

import discord

from gothbot.handlers.base import BaseHandler

logger = logging.getLogger(__name__)


class BurtoHandler(BaseHandler):
    """
    if someone mentions burto it tells them that he is cool
    """

    def __init__(self):
        super().__init__()
        self.name = "BurtoHandler"
        self.keywords = ["burto", "Burto", "burto.", "Burto."]

    async def handle(self, message: discord.Message):
        await message.channel.send("@burto is cool")
        
