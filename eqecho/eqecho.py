## Python imports
import pymysql
import discord
import json
import aiohttp

## Redbot imports
from redbot.core import commands
from redbot.core.utils.chat_formatting import box

class EQEcho(commands.Cog):

    def __init__(self):
        self.serverid = "740650364575023127"
        self.channelid = "740650365078339667"
        db = pymysql.connect("localhost","rampage","6gxby3An5oYA2cP0S5JR80^X&","rampage" )
        self.cursor = db.cursor()

    @commands.command(name="test", brief="Just Testing")
    async def test(self, ctx):
        
        self.cursor.execute("SELECT uid,line FROM echo WHERE echoed='0' ORDER BY epoch LIMIT 5")
        data = self.cursor.fetchone()
        author = ctx.author

        for line in data:
            await author.send(line)