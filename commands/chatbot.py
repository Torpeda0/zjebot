import discord
from discord.ext import commands
import config
import asyncio
import random
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

chatbot = ChatBot('zjebot')
trainer = ListTrainer(chatbot)

class Chatbot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.training = False

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.author == self.bot.user:
            return
        if message.channel.id not in config.chatbot_allowed_channels:
            return
        if self.bot.user.mention in message.content or (message.reference and message.reference.resolved.author == self.bot.user) or random.randint(0,100)*0.01 <= config.chatbot_random_response_chance:
            async with message.channel.typing(): 
                await message.reply(await self.get_response(message.content), allowed_mentions=discord.AllowedMentions.none())

    async def get_response(self, message: str): 
        message = message.replace(self.bot.user.mention, '')
        if message == '':
            return
        response = await asyncio.to_thread(chatbot.get_response, message)
        await self.bot.change_presence(activity=discord.Game(name=response.text[:128]))   
        return response.text
    
    @commands.slash_command(description='Trenuje zjebota')
    async def train(self, ctx: discord.ApplicationContext):
        if self.training:
            return await ctx.respond('Już się trenuje xd')
        self.training = True
        await ctx.respond('Rozpoczęto trenowanie zjebota')
        try:
            with open('last_message') as file:
                last_message = file.read()
        except FileNotFoundError:
            last_message = 0
        channel = self.bot.get_channel(config.discord_chat_id)
        messages = await channel.history(after=last_message, limit=None).flatten()
        open('last_message', 'w').write(str(messages[-1].created_at.timestamp()))
        data = []
        temp = ''
        author = messages[0].author
        for message in messages:
            if message.content == '':
                continue
            if message.author.bot == True: 
                continue
            if author != message.author:
                data.append(temp)
                author = message.author
                temp = ''
            temp += message.content + ' '
        await asyncio.to_thread(trainer.train, data)
        await ctx.edit(content = 'Zakończono trenowanie zjebota')
        self.training = False


def setup(bot: commands.Bot):
    bot.add_cog(Chatbot(bot))