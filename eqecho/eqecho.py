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
  


    async def send_echo(self, ctx):
        # Grab 2 lines from database, send to discord and mark as sent
        self.cursor.execute("SELECT uid,line FROM echo WHERE echoed='0' ORDER BY epoch ASC LIMIT 2")
        data = self.cursor.fetchall()
        channel = ctx.get_user(111584658029826048)
        
        for line in data:
            ## Update this line to echoed
            sql = "UPDATE echo SET echoed='1' WHERE uid='" + line[0] + "'"
            try:
                self.cursor.execute(sql)
                self.db.commit()
                await channel.send(line[1])
            except:
                self.db.rollback()


    async def loop_echo(self, ctx):
        ## echo new lines every 3 seconds
        while True:
            await self.send_echo(self, ctx)
            await asyncio.sleep(3)


    @commands.command(name="test", brief="Just Testing")
    async def test(self, ctx):
        
        channel = discord.utils.get(client.get_channel(self.channel))
        await ctx.send(channel)

        channel = ctx.bot.channels.get(self.channel)
        await channel.send("Booya")