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
        self.config = Config.get_conf(self, identifier="123321123000")
        default_guild = {
            "server": 740650364575023127
            "channel": 740650365078339667
        }
        self.config.register_guild(**default_guild)


        self.db = pymysql.connect("localhost","rampage","6gxby3An5oYA2cP0S5JR80^X&","rampage" )
        self.cursor = self.db.cursor()


    @commands.command()
    async def setserver(self, ctx, new_value):
        await self.config.guild(ctx.guild).server.set(new_value)
        await ctx.send("Value of baz has been changed!")    


    async def echo(self):
        while True:
            self.cursor.execute("SELECT uid,line FROM echo WHERE echoed='0' ORDER BY epoch ASC")
            data = self.cursor.fetchall()
            author = 

    @commands.command(name="test", brief="Just Testing")
    async def test(self, ctx):
        
        self.cursor.execute("SELECT uid,line FROM echo WHERE echoed='0' ORDER BY epoch ASC LIMIT 5")
        data = self.cursor.fetchall()
        author = ctx.author

        for line in data:

            ## Update this line to echoed
            sql = "UPDATE echo SET echoed='1' WHERE uid='" + line[0] + "'"
            try:
                self.cursor.execute(sql)
                self.db.commit()
                await ctx.send(line[1])
            except:
                self.db.rollback()
            