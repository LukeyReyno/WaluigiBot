import argparse
import discord
import random
import asyncio
import time
import datetime
import os

from dotenv import load_dotenv
from discord.ext import commands, tasks
from json import *
from discord.ext.commands.errors import *
from discord_slash import SlashCommand 
from functions.dailyRequests import fullDailyRoutine
from functions.constants import GAME_STATS_FILE, COMMAND_STATS_FILE
from tests.command_tests import DiscordBotTestRunner

parser = argparse.ArgumentParser()
parser.add_argument('--test', action='store_true', help='sets up discord bot test runner')
args = parser.parse_args()

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = "wah ", case_insensitive=True, intents=intents)
bot.remove_command('help')
slash = SlashCommand(bot, sync_commands=True)

async def background_loop():
    await bot.wait_until_ready()
    while not bot.is_closed():
        lt = time.localtime(time.time())
        if lt.tm_hour == 20: #1pm in UTC
            await fullDailyRoutine(bot)
            MP_num = random.choice(range(2,11))
            await bot.change_presence(activity=discord.Game(name=f"Mario Party {MP_num} | wah help"))
        await asyncio.sleep(3600)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)

    upDate = datetime.datetime.now().date()
    print(upDate)

    await bot.change_presence(activity=discord.Game(name="Mario Kart 8 Deluxe | wah help"))
    
    if args.test:
        print('----Tester----')
        testRunner = DiscordBotTestRunner(bot)
        await testRunner.run_test()
    else:
        print('-------')
        bot.loop.create_task(background_loop())
        with open(COMMAND_STATS_FILE, "r") as INFile:
            WahDict = load(INFile)
        WahDict["upDate"] = str(upDate)
        with open(COMMAND_STATS_FILE, "w") as OUTFile:
            dump(WahDict, OUTFile, indent="  ")

cogs = [
    "commands.basic", 
    "commands.hangman", 
    "commands.wordsearch", 
    "commands.reddit", 
    "commands.botw",
    "commands.pokemon",
    "commands.admin",
    "commands.anime",
    "commands.exec",
    "commands.stats",
    "commands.twitter",
    "commands.component",
    "slashcommands.sDBD",
    "slashcommands.sBotw",
    "slashcommands.sPokemon",
    "slashcommands.sBasic",
    "slashcommands.sStats",
    "slashcommands.sReddit",
    "slashcommands.sTwitter",
    "slashcommands.sAnime"
    ]
for cog in cogs:
    try:
        bot.load_extension(cog)
    except Exception as e:
        print(e)

@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        with open(COMMAND_STATS_FILE, "r") as INFile:
            WahDict = load(INFile)
        try:
            WahDict["mentions"] += 1
        except:
            WahDict["mentions"] = 1
        with open(COMMAND_STATS_FILE, "w") as OUTFile:
            dump(WahDict, OUTFile, indent="  ")
    await bot.process_commands(message)

def updateCommandData(ctx: commands.context.Context):
    with open(GAME_STATS_FILE, "r") as INFile:
        WahDict = load(INFile)
    #For User's command count
    try:
        WahDict["games"]["commands"][str(ctx.author.id)] += 1
    except:
        WahDict["games"]["commands"][str(ctx.author.id)] = 1
    with open(GAME_STATS_FILE, "w") as OUTFile:
        dump(WahDict, OUTFile, indent="  ")

    with open(COMMAND_STATS_FILE, "r") as INFile:
        WahDict = load(INFile)
    #For Waluigi Bot's command count
    WahDict["command_count"] += 1
    try:
        WahDict["commands"][f"{ctx.command}"] += 1
    except:
        WahDict["commands"][f"{ctx.command}"] = 1
    with open(COMMAND_STATS_FILE, "w") as OUTFile:
        dump(WahDict, OUTFile, indent="  ")

@bot.event
async def on_slash_command(ctx):
    updateCommandData(ctx)

@bot.event
async def on_command_completion(ctx):
    updateCommandData(ctx)

@bot.event
async def on_command_error(ctx, error):
    print(error)
    if isinstance(error, CommandNotFound):
        return await ctx.send("`That is not a valid command\nType 'wah help' for a list`")
    elif isinstance(error, MissingRequiredArgument):
        return await ctx.send("`You need to include correct arguments for this command\nType 'wah help' for an example`")
    elif isinstance(error, MissingPermissions):
        return await ctx.send("`User is missing the valid permissions to use that command`")
    elif isinstance(error, BotMissingPermissions):
        return await ctx.author.send("`I'm missing valid permissions to use that command`")
    elif isinstance(error, AttributeError):
        return await ctx.send("`Make sure you're using correct arguments\nType 'wah help' for an example`")
    elif isinstance(error, CommandInvokeError):
        try:
            if not ctx.channel.permissions_for(await ctx.guild.fetch_member(bot.user.id)).send_messages:
                return await ctx.author.send("`Unable to satisfy the command. Make sure I have permission to type in that channel\nYou can also type 'wah help' here for some more information.`")
            elif not ctx.channel.permissions_for(await ctx.guild.fetch_member(bot.user.id)).embed_links:
                return await ctx.send("`Make sure I can embed links\nUse 'wah help' somewhere else for more info`")
            return await ctx.send("`Make sure you're using valid arguments\n/are in a valid channel with enough user permissions`")
        except:
            print("Sending Message error")
    else:
        return await ctx.send("`ERROR: Looks like something bad happened.`")

bot.run(TOKEN)
