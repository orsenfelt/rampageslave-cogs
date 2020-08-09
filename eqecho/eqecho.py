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

    @commands.command(name="test", brief="Just Testing")
    async def test(self, ctx):
        await author.send("Hello World")
