from curses.ascii import isdigit
from webbrowser import get
import discord

from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from functions.constants import GUILDS
from functions.dbd_funcs import getPerkEmbed, buildPlayerStat

class sReddit(commands.Cog):

    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="deadbydaylight")
    async def deadbydaylight(self, ctx: SlashContext):
        await ctx.send("This should never ever send.")

    @cog_ext.cog_subcommand(base="deadbydaylight", name="perk",
        description="returns desired deady by daylight perk (or random)", 
        guild_ids=GUILDS, 
        options=[
            create_option(
                name="perk_name",
                description="Name of a Dead By Daylight Perk",
                option_type=str,
                required=False,
            )
        ])
    async def reddit_search(self, ctx: SlashContext, perk_name: str=None):
        perk_embed = getPerkEmbed(perk_name)
        if perk_embed == None:
            return await ctx.send("`Dead By Daylight Perk doesn't exist or is formatted improperly`")
        await ctx.send(embed=perk_embed)
        
    @cog_ext.cog_subcommand(base="deadbydaylight", name="playerstats",
        description="given public steam id, dead by daylight stats will be generated", 
        guild_ids=GUILDS, 
        options=[
            create_option(
                name="steam_id",
                description="Steam ID of User",
                option_type=str,
                required=True,
            )
        ])
    async def reddit_search(self, ctx: SlashContext, steam_id: str=None):
        if len(steam_id) < 10 or not steam_id.isdigit():
            return await ctx.send("`Not a valid Steam ID`")
        steam_id = int(steam_id)
        perk_embed = buildPlayerStat(steam_id)
        if perk_embed == None:
            return await ctx.send("`There was an error with retrieving info\nIt could be that Dead By Daylight player doesn't exist or has a private profile`")
        await ctx.send(embed=perk_embed)

def setup(client):
    client.add_cog(sReddit(client))