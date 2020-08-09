## Python imports
import pymysql
import discord
import json
import aiohttp

## Redbot imports
from redbot.core import Config, commands
from redbot.core.utils.chat_formatting import box

class EQEcho(commands.Cog):

    def __init__(self):
        self.server = "740650364575023127"
        self.channel = "740650365078339667"
        self.db = pymysql.connect("localhost","rampage","6gxby3An5oYA2cP0S5JR80^X&","rampage" )
        self.cursor = self.db.cursor()
  


    async def send_echo(self):
        
        self.cursor.execute("SELECT uid,line FROM echo WHERE echoed='0' ORDER BY epoch ASC LIMIT 2")
        data = self.cursor.fetchall()

        channel = self.channel
        for line in data:
            await channel.send(line[1])


    async def loop_echo(self):
        while True:
            await self.send_echo()
            await asyncio.sleep(3)