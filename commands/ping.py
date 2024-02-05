import discord
from discord.ext import commands

class ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.slash_command(description='Pong!')
    async def ping(self, ctx:discord.ApplicationContext):
        await ctx.respond(f'Pong! Ping: `{round(ctx.bot.latency * 1000)}ms`')

def setup(bot:commands.Bot):
    bot.add_cog(ping(bot))
