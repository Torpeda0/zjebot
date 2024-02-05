import discord
from discord.ext import commands
import config
import os
import dotenv

dotenv.load_dotenv(override=True)

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix=config.discord_prefix)

@bot.event
async def on_ready():
    print(f'{bot.user.name} is ready!')
    await bot.change_presence(activity=discord.Game(name='Autyzm'))

@commands.slash_command(description='Pong!')
async def ping(ctx):
    await ctx.reply('Pong!')

@bot.command()
async def update(ctx: discord.ApplicationContext):
    if ctx.author.guild_permissions.administrator:
        message = await ctx.send('Czekaj...')
        os.system('git pull')
        reload_commands()
        await message.edit(content='Zrobione')

@bot.command()
async def reload(ctx: discord.ApplicationContext):
    if ctx.author.guild_permissions.administrator:
        message = await ctx.send('Czekaj...')
        reload_commands()
        await message.edit(content='Zrobione')

def reload_commands():
    for file in os.listdir('./commands'):
        if file.endswith('.py'):
            print(f'Loading {file[:-3]}...', end=' ')
            try:
                bot.reload_extension(f'commands.{file[:-3]}')
            except discord.errors.ExtensionNotLoaded:
                bot.load_extension(f'commands.{file[:-3]}')
            print('ok')
            

reload_commands()
    
bot.run(os.getenv('token'))



