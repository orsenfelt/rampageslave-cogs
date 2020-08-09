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
        self.channel = "740650365078339667"
        self.db = pymysql.connect("localhost","rampage","6gxby3An5oYA2cP0S5JR80^X&","rampage" )
        self.cursor = self.db.cursor()
        self.bot = bot
        self.restart = True
        self.loop = self.bot.loop.create_task(self._loop_echo())
        

    async def _send_echo(self):
        channel = self.bot.get_channel(int(self.channel))
        now = str(time.time_ns())
        now = int(now[:-9])
        five_ago = str(now - (60 * 5))
        sql = "SELECT uid,line FROM echo WHERE echoed='0' AND epoch>'" + five_ago + "' ORDER BY epoch ASC LIMIT 10"

        print("#################")
        print(sql)

        self.cursor.execute(sql)
        data = self.cursor.fetchall()

        for line in data:

            print("[>] " + line[1])
            
            ## Update this line to echoed
            sql = "UPDATE echo SET echoed='1' WHERE uid='" + line[0] + "'"
            try:
                self.cursor.execute(sql)
                self.db.commit()
                await channel.send(line[1])
                await asyncio.sleep(0.1)
            except:
                print("fail")
                self.db.rollback()

        return True


    async def _loop_echo(self):
        while True:
            await self._send_echo()
            await asyncio.sleep(3)


    @commands.command(name="test", brief="Just Testing")
    async def test(self, ctx):
        await self._send_echo()