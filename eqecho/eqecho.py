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

defaults = {"Channel": 740650365078339667,
            "Dbhost": "localhost",
            "Dbuser": "rampage",
            "Dbpass": "6gxby3An5oYA2cP0S5JR80^X&",
            "Dbname": "rampage",
            "Loopdelay": 5,
            "Echo": 0
            }

class EQEcho(commands.Cog):

    def __init__(self, bot):

        self.sets = Config.get_conf(self, identifier=1355242993, force_registration=True)
        self.sets.register_guild(**defaults)

        self.channel = "740650365078339667"
        self.db = pymysql.connect("localhost","rampage","6gxby3An5oYA2cP0S5JR80^X&","rampage" )
        self.cursor = self.db.cursor()
        self.bot = bot
        self.restart = True
        self.loop = self.bot.loop.create_task(self._loop_echo())
        

    async def _send_echo(self):
        channel = self.bot.get_channel(int(self.channel))
        
        print("loop would run...")
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
            await self._send_echo()
            await asyncio.sleep(5)


    @commands.command(name="echo", brief="Enable (1) or Disable (2) the echo loop")
    async def echo(self, ctx, setting: int):
        await self.sets.guild(ctx.guild).Echo.set(setting)
        await ctx.send("Updated Echo to {setting}.")


    @commands.command(name="test", brief="Just Testing")
    async def test(self, ctx):
        await self._send_echo()