import random
import discord

from discord.ext import commands
from discord_slash import cog_ext, SlashContext, SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
from functions.dailyRequests import dailyCommandFunction
from functions.constants import GUILDS
from json import *

class sBasic(commands.Cog):

    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="random")
    async def random(self, ctx: SlashContext):
        await ctx.send("This should never ever send.")

    @cog_ext.cog_subcommand(base="random", name="coinflip", description="Flips for heads or tails", guild_ids=GUILDS)
    async def random_flip(self, ctx: SlashContext):
        results = ["`Heads`", "`Tails`"]
        return await ctx.send(random.choice(results))

    @cog_ext.cog_subcommand(base="random", name="diceroll", description="Rolls a 6 sided die", guild_ids=GUILDS)
    async def random_roll(self, ctx: SlashContext):
        result = random.choice(range(1,7))
        return await ctx.send(f"`{result}`")

    @cog_ext.cog_slash(name="consume", description="Sends a random Food and Animal Emoji", guild_ids=GUILDS)
    async def consume(self, ctx: SlashContext):
        foods = 'ð ð ð ð ð ð ð ð ð ð ð ð ðĨ­ ð ðĨĨ ðĨ ð ð ðĨ ðĨĶ ðĨŽ ðĨ ðķ ð― ðĨ ð§ ð§ ðĨ ð  ðĨ ðĨŊ ð ðĨ ðĨĻ ð§ ðĨ ðģ ð§ ðĨ ð§ ðĨ ðĨĐ ð ð ðĶī ð­ ð ð ð ðĨŠ ðĨ ð§ ðŪ ðŊ ðĨ ðĨ ðĨŦ ð ð ðē ð ðĢ ðą ðĨ ðĶŠ ðĪ ð ð ð ðĨ ðĨ  ðĨŪ ðĒ ðĄ ð§ ðĻ ðĶ ðĨ§ ð§ ð° ð ðŪ ð­ ðŽ ðŦ ðŋ ðĐ ðŠ ð° ðĨ ðŊ ðĨ ðž ðĩ ð§ ðĨĪ ðķ ðš ðŧ ðĨ ð· ðĨ ðļ ðđ ð§ ðū ð§ :poop:'
        food_list = foods.split()
        animals = 'ðķ ðą ð­ ðđ ð° ðĶ ðŧ ðž ðĻ ðŊ ðĶ ðŪ ð· ðļ ðĩ ð ð§ ðĶ ðĪ ðĶ ðĶ ðĶ ðĶ ðš ð ðī ðĶ ð ð ðĶ ð ð ð ðĶ ðĶ ð· ðĶ ðĒ ð ðĶ ðĶ ðĶ ð ðĶ ðĶ ðĶ ðĶ ðĄ ð  ð ðŽ ðģ ð ðĶ ð ð ð ðĶ ðĶ ðĶ§ ð ðĶ ðĶ ðŠ ðŦ ðĶ ðĶ ð ð ð ð ð ð ð ðĶ ð ðĶ ð ðĐ ðĶŪ ðâðĶš ð ð ðĶ ðĶ ðĶ ðĶĒ ðĶĐ ð ð ðĶ ðĶĻ ðĶĄ ðĶĶ ðĶĨ ð ð ðŋ ðĶ ð'
        animals_list = animals.split()
        return await ctx.send(f'{random.choice(food_list)}{random.choice(animals_list)}')
    
    @cog_ext.cog_slash(name="daily", 
        description="sets up a daily message for bot to send", 
        guild_ids=GUILDS, 
        options=[
            create_option(
                name="daily_type",
                description="Decide what kind of message for bot to send each day",
                option_type=str,
                required=True,
                choices=[
                    create_choice(
                        name="song",
                        value="song"
                    ),
                    create_choice(
                        name="stat",
                        value="stat"
                    ),
                    create_choice(
                        name="hmmm",
                        value="hmmm"
                    ),
                    create_choice(
                        name="pokemon",
                        value="pokemon"
                    ),
                    create_choice(
                        name="botw",
                        value="botw"
                    ),
                    create_choice(
                        name="anime",
                        value="anime"
                    ),
                    create_choice(
                        name="info",
                        value="info"
                    )
                ]
            )
        ])
    async def daily(self, ctx: SlashContext, daily_type:str):
        await ctx.defer()
        return await dailyCommandFunction(self.client, ctx, daily_type)

def setup(client):
    client.add_cog(sBasic(client))
