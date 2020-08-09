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
        
        self.cursor.execute("SELECT * FROM echo WHERE echoed='0' ORDER BY epoch DESC LIMIT 2")
        data = cursor.fetchone()
        
        author = ctx.author
        await author.send(data)