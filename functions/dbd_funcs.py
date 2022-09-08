from typing import Dict, List

import datetime
import discord
import json
import requests
import random
import re

class SteamAuth():
    def __init__(self, steamAuthJson):
        self.__dict__ = steamAuthJson

try:
    with open("data/steamAuth.json", "r") as steamJson:
        credDict = json.load(steamJson)

    steamAuthentication = SteamAuth(credDict)
except:
    steamAuthentication = None
    print("Issue setting up steam token")

class DBD_API_List():

    def __init__(self):
        self.perks: Dict = self._getList("perks")
        
        # possibly just want to write to a file if it takes too much memory
        self.playercache: Dict = {}
        self.steamnamecache: Dict = {}
        #self.killers: List = self._getList("killers")
        #self.survivors: List = self._getList("survivors")
        #self.currencies: List = self._getList("currencies")
        
    def _getList(self, request):
        response = requests.get(f"https://dbd.tricky.lol/api/{request}")
        if (response.ok):
            jsonResult = response.json()
            
            return jsonResult
    
        print(f"ERROR {response.status_code} on GET DBD {request}")
        return None

dbdAPI = DBD_API_List()

def getBaseEmbed():
    embed = discord.Embed()
    embed.color = 0x7027C3
    embed.set_footer(text="Wah", icon_url="https://ih1.redbubble.net/image.15430162.9094/sticker,375x360.u2.png")
    embed.set_thumbnail(url="https://ctd-thechristianpost.netdna-ssl.com/en/full/66473/dead-by-daylight-logo.jpg")
    
    return embed

def getSteamName(steamid):
    if steamAuthentication == None:
        return None
    
    response = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={steamAuthentication.token}&steamids={steamid}")
    if response.ok:
        json_result = response.json()
        return json_result['response']['players'][0]['personaname']
    
    print(f"{response.status_code}: sUnable to get Steam Name from id: {steamid}")
    return None

# returns playerstat json dict
def getPlayerstat(steamid:int):
    if steamid in dbdAPI.playercache:
        now = datetime.datetime.utcnow()
        last_updated_timestamp = datetime.datetime.utcfromtimestamp(dbdAPI.playercache[steamid]['updated_at'])
        seconds_diff = now - last_updated_timestamp
        
        # stats update every ~6 hours
        if seconds_diff.seconds < 6 * 3600:
            return dbdAPI.playercache[steamid]
    
    response = requests.get(f"https://dbd.tricky.lol/api/playerstats?steamid={steamid}")
    if (response.ok):
        jsonResult = response.json()
        dbdAPI.playercache[steamid] = jsonResult 
        return jsonResult

    print(f"ERROR {response.status_code} on GET DBD PlayerStat")
    print(response)
    return None

def buildPlayerStat(steamid:int):
    playerDict = getPlayerstat(steamid)
    if playerDict == None:
        return None
    
    if steamid not in dbdAPI.steamnamecache:
        steam_name = getSteamName(steamid)
        if steam_name != None:
            dbdAPI.steamnamecache[steamid] = steam_name
        else:
            steam_name = None
    else:
        steam_name = dbdAPI.steamnamecache[steamid]
    
    stats_embed: discord.embeds.Embed = getBaseEmbed()
    
    stats_embed.url = f"https://steamcommunity.com/profiles/{steamid}/"
    
    if steam_name != None:
        stats_embed.title = f"Dead by Daylight Player Stats:\n{steam_name}"
    else:
        stats_embed.title = "Dead by Daylight Player Stats"
    
    """ Steam Profile Picture later
    imageName:str = playerDict['name']
    imageName = re.sub(r'[^a-zA-Z]', '', imageName)
    imageUrl = f"https://raw.githubusercontent.com/dearvoodoo/dbd/master/Perks/{imageName}.png"
    stats_embed.set_image(url=imageUrl)
    """
    
    last_updated_timestamp = datetime.datetime.utcfromtimestamp(playerDict['updated_at'])
    description:str = "```" \
        f"Last Updated: {last_updated_timestamp.date()}\n" \
        f"              {last_updated_timestamp.time()} UTC\n" \
        f"Total Playtime:    {((playerDict['playtime']) // 60):,d} hours\n" \
        f"Total Bloodpoints: {playerDict['bloodpoints']:,d}```\n"
    
    stats_embed.description = description
    
    survivor_str = "```" \
        f"Rank:                {playerDict['survivor_rank']:d}\n" \
        f"Generators Repaired: {playerDict['gensrepaired']:,d}\n" \
        f"Survivors Healed:    {playerDict['survivorshealed']:,d}\n" \
        f"Skillchecks:         {playerDict['skillchecks']:,d}\n" \
        f"Unhooks:             {playerDict['saved']:,d}\n" \
        f"Attacks Dodged:      {playerDict['dodgedattack']:,d}\n" \
        f"Items Depleted:      {playerDict['itemsdepleted']:,d}\n" \
        f"Chests Searched:     {playerDict['chestssearched']:,d}\n" \
        f"Hex Totems Cleansed: {playerDict['hextotemscleansed']:,d}\n" \
        f"Exit Gates Opened:   {playerDict['exitgatesopened']:,d}\n" \
        f"Perfect Games:       {playerDict['survivor_perfectgames']:,d}\n" \
        f"Escapes:             {playerDict['escaped']:,d}```\n"
    stats_embed.add_field(name="Survivor", value=survivor_str, inline=False)
    
    killer_str =  f"```" \
        f"Rank:                {playerDict['killer_rank']:,d}\n" \
        f"Sacrifices:          {playerDict['sacrificed']:,d}\n" \
        f"Kills:               {playerDict['killed']:,d}\n" \
        f"Grabs from Gen:      {playerDict['survivorsgrabbedrepairinggen']:,d}\n" \
        f"Grabs from Locker:   {playerDict['survivorsgrabbedfrominsidealocker']:,d}\n" \
        f"Downed Exposed:      {playerDict['survivorsdowned_exposed']:,d}\n" \
        f"Closed Hatch:        {playerDict['hatchesclosed']:,d}```"
    stats_embed.add_field(name="Killer", value=killer_str, inline=False)
    
    return stats_embed

def getPerkEmbed(name=None):
    if name == None:
        perk = dbdAPI.perks[random.choice(list(dbdAPI.perks.keys()))]
    else:
        name = name.lower()
        perk = None
        for p in dbdAPI.perks.keys():
            apiPerkName:str = dbdAPI.perks[p]["name"].lower()
            if apiPerkName == name:
                perk = dbdAPI.perks[p]
                break
        if perk == None:
            return None
        
    perk_embed: discord.embeds.Embed = getBaseEmbed()
    
    perk_embed.title = perk["name"]
    imageName:str = perk['name']
    imageName = re.sub(r'[^a-zA-Z]', '', imageName)
    imageUrl = f"https://raw.githubusercontent.com/dearvoodoo/dbd/master/Perks/{imageName}.png"
    perk_embed.set_image(url=imageUrl)
    
    description:str = ""
    description += f"{perk['description']}"
    description = re.sub(r'<[\/[A-Za-z]*>', '', description)
    for i in range(len(perk['tunables'])):
        tunableStr = ", ".join(perk['tunables'][i])
        description = description.replace("{" + str(i) + "}", tunableStr)
    
    perk_embed.description = description
    
    return perk_embed