import discord
from discord.ext import commands
import config
import os
import dotenv

dotenv.load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix=config.discord_prefix)

@bot.event
async def on_ready():
    print(f'{bot.user.name} is ready!')

@commands.slash_command(description='Pong!')
async def ping(ctx):
    await ctx.reply('Pong!')

@bot.command()
async def reload(ctx):
    if ctx.author.id not in config.discord_admins:
        return
    reload_commands()
    await ctx.reply('ok')

def reload_commands():
    for file in os.listdir('./commands'):
        if file.endswith('.py'):
            try:
                bot.reload_extension(f'commands.{file[:-3]}')
            except discord.ext.commands.errors.ExtensionNotLoaded:
                bot.load_extension(f'commands.{file[:-3]}')

reload_commands()
    
bot.run(os.getenv('discord_token'))



