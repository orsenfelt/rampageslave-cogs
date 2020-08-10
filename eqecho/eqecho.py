## Python imports
import pymysql
import discord
import json
import aiohttp
import time
import asyncio

## Redbot imports
from redbot.core import Config, commands
from redbot.core.utils.chat_formatting import box

class EQEcho(commands.Cog):

    def __init__(self, bot):
        defaults = {"channel": "",
                    "dbhost": "localhost",
                    "dbuser": "",
                    "dbpass": "",
                    "dbname": "",
                    "guild": "",
                    "loopdelay": 5,
                    "echo": "0"
                    }
        self.config = Config.get_conf(self, identifier=1355242993)
        self.config.register_global(**defaults)

        self.guild = "740650364575023127"
        self.channel = "740650365078339667"
        self.db = pymysql.connect("localhost","rampage","6gxby3An5oYA2cP0S5JR80^X&","rampage")
        self.cursor = self.db.cursor()
        self.bot = bot
        self.restart = True
        self.loop = self.bot.loop.create_task(self._loop_echo())


    async def _send_echo(self):
        conf_channel = self.bot.get_channel(int(self.config.channel))
        now = str(time.time_ns())
        now = int(now[:-9])
        five_ago = str(now - (60 * 10))
        sql = "SELECT id,line FROM echo WHERE echoed='0' AND epoch>'" + five_ago + "' ORDER BY id ASC LIMIT 10"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()

        for line in data:
            
            ## Update this line to echoed
            sql = "UPDATE echo SET echoed='1' WHERE id='" + line[0] + "'"
            try:
                self.cursor.execute(sql)
                self.db.commit()
            except:
                self.db.rollback()
                #!!# loop breaking fail condition

            ## Send out the line to discord
            try: 
                await conf_channel.send(line[1])
                await asyncio.sleep(0.2)
            except:
                self.db.rollback()
                #!!# loop breaking fail condition

        return True


    async def _loop_echo(self):
        while True:
            conf_echo = await self.config.echo()
            conf_echo = str(conf_echo)

            conf_loopdelay = await self.config.loopdelay()
            conf_loopdelay = int(conf_loopdelay)
            
            if (conf_echo == "1"):
                await self._send_echo()
                await asyncio.sleep(conf_loopdelay)

            else:
                await asyncio.sleep(30)


    @commands.command(name="setecho", brief="Enable (1) or Disable (2) the echo loop")
    async def setecho(self, ctx, setting):
        await self.config.echo.set(setting)
        await ctx.send("[#] Updated __echo__ setting to :: {}".format(setting))


    @commands.command(name="getguild", brief="Get the guild ID")
    async def getguild(self, ctx):
        setting = await self.config.guild()
        await ctx.send("[>] Current __guild__ setting is :: {}".format(setting))


    @commands.command(name="setguild", brief="Set the guild ID")
    async def setguild(self, ctx, setting):
        await self.config.guild.set(setting)
        await ctx.send("[#] Updated __guild__ setting to :: {}".format(setting))


    @commands.command(name="getchannel", brief="Get the channel ID")
    async def getchannel(self, ctx):
        setting = await self.config.guild()
        await ctx.send("[>] Current __channel__ setting is :: {}".format(setting))


    @commands.command(name="setchannel", brief="Set the channel ID to echo into")
    async def setchannel(self, ctx, setting):
        await self.config.channel.set(setting)
        await ctx.send("[#] Updated __channel__ setting to :: {}".format(setting))


    @commands.command(name="test", brief="Just Testing")
    async def test(self, ctx):
        await self._send_echo()