import abc

import discord


class BaseHandler(abc.ABC):
    def __init__(self):
        self.name = "BaseHandler"
        self.keywords = []

    async def handle(self, message: discord.Message):
        # Implement something here to handle the message
        pass
