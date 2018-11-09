import discord
from time import gmtime, strftime
import config#storing out token in here
import json
import asyncio
from pathlib import Path

jsonFilePath = Path(Path.cwd()/"Maplestory2Bot"/"boss-timer.json")


class MS2Bot(discord.Client):
    """Maplestory2 discord bot"""    
    targetChannel = ""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = config.TOKEN
        self.targetChannelID = 509102127105441833

        self.bossSpawnerTask = self.loop.create_task(self._announceBossSpawn())
    
    
    async def on_ready(self):
        print("Bot has been initialized.")        
        # print(Path.cwd()/"Maplestory2Bot"/"boss-timer.json")
    
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
        try:
            with open(jsonFilePath) as file:
                fileContent = json.load(file)
        except Exception as e:
            print(e)

        while not self.is_closed():
            currentMinute = int(strftime("%M",gmtime()))
            bossNames=[]
            bossesSpawnInfo=[]
            content=""
            try:
                for boss,bossInfo in fileContent.items():     
                    bossSpawningInFive = (currentMinute + 5) == bossInfo['Spawn Time']
                    bossSpawningInThree = (currentMinute + 3) == bossInfo['Spawn Time']
                    """Checks if boss is spawning in 5 minutes"""
                    if(bossSpawningInFive):
                        bossNames.append(boss)
                        bossesSpawnInfo.append(bossInfo)                        
                    # elif(bossSpawningInThree):
                content = self.formatJSON(bossNames,bossesSpawnInfo)               
            except Exception as e:
                print(e)
            if (content != None):
                await targetChannel.send(content)            
            else:
                print("nothing to send")
            await asyncio.sleep(60)#task runs every 60 seconds

    def formatJSON(self,bossNames,bossInfo):
        if(len(bossNames) < 1):
            print("fuck this im out!")
            return
        content = "Bosses about to spawn soon: \n"
        for boss,info in enumerate(bossInfo):
            content += f'**{bossNames[boss]}** '+"\n"
            content += "LVL: " + str(info['LVL'])+"\n"
            content += "Map: "+ info['Map']+"\n"
            content += "Spawn time: " + str(info['Spawn Time'])+"\n"
            content += "\n"                        
        print(content)  
        return content  

ms2bot = MS2Bot()
ms2bot.run(ms2bot.token)