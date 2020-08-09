from .eqecho import EQEcho

def setup(bot):
    bot.add_cog(EQEcho(bot, ctx))