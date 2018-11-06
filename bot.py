import discord
import time
import config#storing out token in here
import json
from pathlib import Path

jsonFileName = "boss-timer.json"
jsonFilePath = Path(jsonFileName)


class MS2Bot(discord.Client):
    """Maplestory2 discord bot"""    
    targetChannel = ""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = config.TOKEN
        self.targetChannelID = 509102127105441833

        self.bossSpawnerTask = self.loop.create_task(self._announceBossSpawn())
    
    
    async def on_ready(self):
        print("Wazzzzzaaaaaaaaaaaaaap")
        print(f'we logged in as {self.user}')
    
    async def on_message(self,message):        

        print(f'{message.channel} | {message.author} | {message.author.id} | {message.author.name} | {message.content} | {message.channel.id} | {message.channel}')
        if message.content.startswith('!omak'):
            await message.channel.send('Omak 7elwa ya saif.')
        if message.content.startswith('!whostheleader'):
            await message.channel.send('Omak')
        if(self._parseString(message.content,"soofa")):
            await message.channel.send("Why do you mention my name?")
        if message.content.startswith('!guides'):
            await message.channel.send("Check out the guide channel.")
                
    def _parseString(self,message,target):
        """Parses the discord message and checks if soofa was mentioned"""
        for word in message.split(" "):
            if word.lower() == target:
                return True

    async def _announceBossSpawn(self):
        """Background task that is always on and writes in the channel when a boss is about to spawn """
        await self.wait_until_ready()        

        targetChannel = self.get_channel(self.targetChannelID)        
        fileContent=""        
        # with open(jsonFilePath) as file:
        #     fileContent = json.load(file)
        while not self.is_closed():
            # for boss in fileContent:
            await targetChannel.send("Hi")
            #     print(boss)
            await asyncio.sleep(10)#task runs every 60 seconds