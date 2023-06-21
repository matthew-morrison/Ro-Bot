import os
import json
from discord.ext import commands
import discord
import asyncio

# epoch must be in the format like "1 January 2020 PST", ie, following the "%d %B %Y %Z" date format.

configFile = "config.json"
if os.path.isfile(configFile):
    file = open(configFile)
    conf = json.load(file)
    discord_token = conf["discord_bot_token"]
    description = conf['description']
    rocode_minute = conf['rocode_minute']
    rocode_hour = conf['rocode_hour']
    epoch = conf['epoch']
    timezone = conf['timezone']
else:
    print("Uh... no config file. Gonna explode now.")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', description=description, intents=intents)
bot.rocode_minute = rocode_minute
bot.rocode_hour = rocode_hour
bot.epoch_str = epoch
bot.timezone_str = timezone
#bot.load_extension("cogs.rocode")

@bot.event
async def on_ready():
    print('Logged in as', bot.user.name, bot.user.id, '\n-----')


async def main():
    async with bot:
        await bot.load_extension('cogs.rocode')
        await bot.start(discord_token)

asyncio.run(main())
