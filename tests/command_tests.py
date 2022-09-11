import os

from discord.ext import commands
from functions.botwFuncs import botwFunction

class DiscordBotTestRunner:
    
    def __init__(self, client: commands.Bot, ):
        self.client = client
        self.test_channel_id = os.getenv("TEST_CHANNEL")

    async def run_test(self):
        await self._check_test_channel()
        await self._botw_message()
        raise KeyboardInterrupt
        
    async def _check_test_channel(self):
        if self.test_channel_id == None:
            raise TypeError("Test Channel ID is None")
        self.test_channel_id = int(self.test_channel_id)

    async def _botw_message(self):
        botwEmbed = botwFunction(None)
        
        test_channel = self.client.get_channel(self.test_channel_id)
        await test_channel.send(embed=botwEmbed)
