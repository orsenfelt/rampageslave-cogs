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
        defaults = {"echochan": "",
                    "loopdelay": 5,
                    "echo": "0"
                    }
        self.config = Config.get_conf(self, identifier=1355242993)
        self.config.register_global(**defaults)
        self.bot = bot
        self.db = pymysql.connect("localhost","rampage","6gxby3An5oYA2cP0S5JR80^X&","rampage")
        self.cursor = self.db.cursor()
        self.restart = True
        self.loop = self.bot.loop.create_task(self._loop_echo())


    async def _send_echo(self):
        now = str(time.time_ns())
        now = int(now[:-9])
        minago = str(now - (60 * 15))
        sql = "SELECT id,line FROM echo WHERE echoed='0' AND epoch>'" + minago + "' ORDER BY id ASC LIMIT 2"
        print("[~] " + sql)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()

        for line in data:
            print("[>] (" + str(line[0]) + ") " + line[1])
            sql = "UPDATE echo SET echoed='1' WHERE id='" + str(line[0]) + "'"
            try:
                self.cursor.execute(sql)
                self.db.commit()
                await self.echo_chan.send(line[1])
                print("[^] Done")
                sleep(0.6)
            except:
                self.db.rollback()


    async def _loop_echo(self):
        conf_echo = await self.config.echo()
        conf_echo = str(conf_echo)

        while (conf_echo == "1"):

            conf_echo = await self.config.echo()
            conf_echo = str(conf_echo)

            conf_loopdelay = await self.config.loopdelay()
            conf_loopdelay = int(conf_loopdelay)

            self.echochan = await self.config.echochan()
            self.echo_chan = self.bot.get_channel(int(self.echochan))

            if (len(self.echochan) > 5):
                await self._send_echo()
                await asyncio.sleep(5)
            else:
                print("[x] Channel not set")
                await asyncio.sleep(30)
                continue


    @commands.command(name="setecho", brief="Enable (1) or Disable (2) the echo loop")
    async def setecho(self, ctx, setting):
        await self.config.echo.set(setting)
        await ctx.send("[#] Updated __echo__ setting to :: {}".format(setting))


    @commands.command(name="setloopdelay", brief="Seconds between DB searches")
    async def setloopdelay(self, ctx, setting):
        await self.config.loopdelay.set(setting)
        await ctx.send("[#] Updated __loopdelay__ setting to :: {}".format(setting))


    @commands.command(name="getchannel", brief="Get the channel ID")
    async def getchannel(self, ctx):
        setting = await self.config.echochan()
        await ctx.send("[>] Current __channel__ setting is :: {}".format(setting))


    @commands.command(name="setchannel", brief="Set the channel ID to echo into")
    async def setchannel(self, ctx, setting):
        await self.config.echochan.set(setting)
        await ctx.send("[#] Updated __channel__ setting to :: {}".format(setting))


    @commands.command(name="test", brief="Just Testing")
    async def test(self, ctx):        
        self.echochan = await self.config.echochan()
        self.echo_chan = self.bot.get_channel(int(self.echochan))
        await self.echo_chan.send("Starting test echo to :: {}".format(self.echochan))
        await self._send_echo()