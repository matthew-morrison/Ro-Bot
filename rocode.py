import datetime
import pytz
import random
import discord

from random import shuffle
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands


class Rocode(commands.Cog):

    def __init__(self, bot):
        self.tz = pytz.timezone(bot.timezone_str)  # https://www.youtube.com/watch?v=-5wpm-gesOY
        self.epoch = datetime.datetime.strptime(bot.epoch_str, "%M %H %d %B %Y")
        self.epoch = self.tz.localize(self.epoch)
        print("Rocode set to send messages at every ", bot.rocode_hour, ":", bot.rocode_minute, self.tz)

        codefile = open("codes.txt")
        self.codes = codefile.readlines()
        random.seed(1)  # seed random so we shuffle to the same state on each startup
        shuffle(self.codes)

        self.rocodeChannel = {
            "test": 590716993146191873,  # testing server / channel
            "prod": 837825838359511060  # production server / channel
        }

        self.bot = bot

        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.perform_job, trigger='cron', minute=bot.rocode_minute, hour=bot.rocode_hour, day='*', week='*', month='*',
                          year='*', misfire_grace_time=100, coalesce=False, timezone=self.tz)
        scheduler.start()

    async def perform_job(self):
        print("Performing Rocode Job at " + datetime.datetime.now(tz=self.tz).strftime("%d-%m-%Y--%H-%M"))
        curr_code = self.codes[(datetime.datetime.now(tz=self.tz) - self.epoch).days % len(self.codes)]
        for server, channel in self.rocodeChannel.items():
            try:
                ch = self.bot.get_channel(channel)
                if ch is None:
                    print("Skipping server with no perms or non-existent channel ID")
                else:
                    await self.bot.get_channel(channel).send(curr_code)
            except discord.HTTPException:
                print("Could not send ro'code, HTTP error")
            except discord.Forbidden:
                print("Could not send ro'code, Forbidden error")

    # Users can manually retrieve the current rocode using this command in discord
    @commands.command(pass_context=True)
    async def rocode(self, ctx):
        curr_code = self.codes[(datetime.datetime.now(tz=self.tz) - self.epoch).days % len(self.codes)]
        print((datetime.datetime.now(tz=self.tz) - self.epoch).days)
        await ctx.channel.send("Today's Rover Code is:\n\n" + curr_code)


def setup(bot):
    bot.add_cog(Rocode(bot))
