import os
import json
from discord.ext import commands


configFile = "config.json"
if os.path.isfile(configFile):
    file = open(configFile)
    conf = json.load(file)
    discord_token = conf["discord_bot_token"]
    description = conf['description']
    rocode_minute = conf['rocode_minute']
    rocode_hour = conf['rocode_hour']
else:
    print("Uh... no config file. Gonna explode now.")

bot = commands.Bot(command_prefix='!', description=description)
bot.rocode_minute = rocode_minute
bot.rocode_hour = rocode_hour
bot.load_extension("rocode")


@bot.event
async def on_ready():
    print('Logged in as', bot.user.name, bot.user.id, '\n-----')


if __name__ == '__main__':
    bot.run(discord_token)