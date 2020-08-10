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
                    "loopdelay": 5,
                    "echo": "0"
                    }
        self.config = Config.get_conf(self, identifier=1355242993, force_registration=True)
        self.config.register_guild(**defaults)

        self.channel = "740650365078339667"
        self.db = pymysql.connect("localhost","rampage","6gxby3An5oYA2cP0S5JR80^X&","rampage" )
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
            ## Get the current config echo value
            conf_echo = await self.config.guild(self.bot.guild).echo()
            print(conf_echo)
            conf_echo = str(conf_echo)
            
            if (conf_echo == "1"):
                print("Loop >")
                await self._send_echo()
                await asyncio.sleep(5)

            else:
                print("No loops")
                await asyncio.sleep(60)


    @commands.command(name="echo", brief="Enable (1) or Disable (2) the echo loop")
    async def echo(self, ctx, setting):
        await self.config.guild(ctx.guild).echo.set(setting)
        await ctx.send("Updated")


    @commands.command(name="getdbhost", brief="Get DB Host")
    async def getconf(self, ctx, key: str):
        baz_val = await self.config.guild(ctx.guild).dbhost()
        await ctx.send("The value of baz is {}".format(str(baz_val)))


    @commands.command(name="test", brief="Just Testing")
    async def test(self, ctx):
        await self._send_echo()