#Initial commit
import discord
from discord.ext import commands
import time
import config#storing out token in here

class MS2Bot(discord.Client):
    """Maplestory2 discord bot"""    
    #Contrustctor

    def __init__(self):
        super().__init__()
        self.token = config.TOKEN
        # self.bot = commands.Bot(command_prefix='!',description=self.botDescription)
    
    
    async def on_ready(self):
        print("Wazzzzzaaaaaaaaaaaaaap")
        print(f'we logged in as {self.user}')
    
    
    async def on_message(self,message):
        print(f'{message.channel}  | {message.author} | {message.author.name} | {message.content}')
        if message.content.startswith('!omak'):
            await message.channel.send('Omak 7elwa ya saif.')

    async def _started_bot(self,message):
        await channel.send("hi")

    


