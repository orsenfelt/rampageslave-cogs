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
        self.config = Config.get_conf(self, identifier=1355242993, force_registration=True)
        self.config.register_guild(**defaults)

        self.guild = "740650364575023127"
        self.channel = "740650365078339667"
        self.db = pymysql.connect("localhost","rampage","6gxby3An5oYA2cP0S5JR80^X&","rampage")
        self.cursor = self.db.cursor()
        self.bot = bot
        self.restart = True
        self.loop = self.bot.loop.create_task(self._loop_echo())


    async def _send_echo(self):
        channel = self.bot.get_channel(int(self.channel))
        return "done"

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
                ## loop breaking fail condition

            ## Send out the line to discord
            try: 
                await channel.send(line[1])
                await asyncio.sleep(0.2)
            except:
                self.db.rollback()
                ## loop breaking fail condition

        return True


    async def _loop_echo(self):
        while True:
            conf_echo = await self.config.guild(self.bot.get_guild(self.guild)).echo()
            print("################")
            print(conf_echo)
            print("################")
            conf_echo = str(conf_echo)
            
            if (conf_echo == "1"):
                await self._send_echo()
                await asyncio.sleep(5)

            else:
                print("No loops")
                await asyncio.sleep(60)


    @commands.command(name="setecho", brief="Enable (1) or Disable (2) the echo loop")
    async def setecho(self, ctx, setting):
        await self.config.guild(ctx.guild).echo.set(setting)
        await ctx.send("[#] Updated __echo__ setting to :: {}".format(setting))


    @commands.command(name="setguild", brief="Set the guild ID")
    async def setguild(self, ctx, setting):
        await self.config.guild(ctx.guild).guild.set(setting)
        await ctx.send("[#] Updated __guild__ setting to :: {}".format(setting))


    @commands.command(name="setchannel", brief="Set the channel ID to echo into")
    async def setchannel(self, ctx, setting):
        await self.config.guild(ctx.guild).channel.set(setting)
        await ctx.send("[#] Updated __channel__ setting to :: {}".format(setting))


    @commands.command(name="test", brief="Just Testing")
    async def test(self, ctx):
        await self._send_echo()