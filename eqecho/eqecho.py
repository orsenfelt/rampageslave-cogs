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
        five_ago = str(now - (60 * 10))
        sql = "SELECT id,line FROM echo WHERE echoed='0' AND epoch>'" + five_ago + "' ORDER BY id ASC"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()

        for line in data:
            print("[~] ("{}") " + line[1]).format(line[0])
            ## Update this line to echoed
            sql = "UPDATE echo SET echoed='1' WHERE id='{}'".format(line[0])
            try:
                self.cursor.execute(sql)
                self.db.commit()
                print("[m] DB update!")
            except:
                self.db.rollback()
                print("[x] DB rollback!")
                #!!# loop breaking fail condition

            ## Send out the line to discord
            try: 
                await self.echo_chan.send(line[1])
                print("[m] Discord sent!")
                await asyncio.sleep(0.2)
            except:
                self.db.rollback()
                print("[m] Problem with sending to discord =/")
                #!!# loop breaking fail condition

        return True


    async def _loop_echo(self):

        while True:
            conf_echo = await self.config.echo()
            conf_echo = str(conf_echo)

            conf_loopdelay = await self.config.loopdelay()
            conf_loopdelay = int(conf_loopdelay)

            self.echochan = await self.config.echochan()
            self.echo_chan = self.bot.get_channel(int(self.echochan))

            if (len(self.echochan) > 5):
                print("[#] Channel is set")
                if (conf_echo == "1"):
                    print("[m] Echo enabled")
                    await self._send_echo()
                    await asyncio.sleep(conf_loopdelay)
                else:
                    print("[x] Echo disabled")
                    await asyncio.sleep(30)
            else:
                print("[x] Channel not set")
                await asyncio.sleep(60)
                continue


    @commands.command(name="setecho", brief="Enable (1) or Disable (2) the echo loop")
    async def setecho(self, ctx, setting):
        await self.config.echo.set(setting)
        await ctx.send("[#] Updated __echo__ setting to :: {}".format(setting))


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