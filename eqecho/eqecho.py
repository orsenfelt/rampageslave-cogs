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
        author = ctx.author
        await author.send("Hello World")

    @commands.command()
    async def dadjoke(self, ctx: commands.Context):
        headers = {
            "User-Agent": "FoxV3 (https://github.com/bobloy/Fox-V3)",
            "Accept": "application/json",
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            joke = await fetch_url(session, "https://icanhazdadjoke.com/")

        await ctx.send(joke["joke"])