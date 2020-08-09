## Python imports
import pymysql
import discord
import json
import aiohttp

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
        

    async def _send_echo(self, channel):
        self.cursor.execute("SELECT uid,line FROM echo WHERE echoed='0' ORDER BY epoch ASC LIMIT 2")
        data = self.cursor.fetchall()

        for line in data:
            ## Update this line to echoed
            sql = "UPDATE echo SET echoed='1' WHERE uid='" + line[0] + "'"
            try:
                self.cursor.execute(sql)
                self.db.commit()
                await channel.send(line[1])
            except:
                self.db.rollback()

    def _loop_echo(self, ctx):
        self._send_echo(ctx, self.channel)


    @commands.command(name="test", brief="Just Testing")
    async def test(self, ctx):
        channel = ctx.bot.get_channel(int(self.channel))
        await self._send_echo(channel)


