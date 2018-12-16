import discord
import random
from time import gmtime, strftime
import config#storing out token in here
import json
import asyncio
import Scrapper
from pathlib import Path



bossSpawnerJson = Path(Path.cwd()/"boss-timer.json")
ms2NewsJSON = Path(Path.cwd()/"maplestory2-news.json")



class MS2Bot(discord.Client):
    """Maplestory2 discord bot"""    
    targetChannel = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = config.TOKEN
        self.bossSpawnerChannel = 509102127105441833
        self.updatesChannel = 519503847291355146
        self.newsURL = "http://maplestory2.nexon.net/en/news"


        self.bossSpawnerTask = self.loop.create_task(self._announceBossSpawn())
        self.newsCheckerTask = self.loop.create_task(self._postNewNewsArticle())
    
    
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
            await message.channel.send(self.randomReply())
        if message.content.startswith('!guides'):
            await message.channel.send("Check out the guide channel.")
        if message.content.startswith('!google'):
            await message.channel.send(self.googleSearch(message.content))
        if message.content.startswith('!cl'):
            await message.channel.send(self.commandList())
        if message.content.startswith('!test'):
            await self._postNewNewsArticle()
                
    def _parseString(self,message,target):
        """Parses the discord message and checks if soofa was mentioned"""
        for word in message.split(" "):
            if word.lower() == target:
                return True

    async def _postNewNewsArticle(self):
        """Writes into the updates channel once a new news article is posted."""        
        scrapper = Scrapper.Scrapper()
        await self.wait_until_ready()        

        #Setting the channel that will get posted into 
        updateChannel = self.get_channel(self.updatesChannel)

        while not self.is_closed():
            try:
                with open(ms2NewsJSON) as file:
                    fileContent = json.load(file)
                    latestArticle = scrapper.CheckCurrentNewsArticle("http://maplestory2.nexon.net/en/news")
                    fileContent['URL'] = latestArticle
                    latestArticleDate = scrapper.GetNewsArticleDate()
                    fileContent['publishedOn'] = latestArticleDate
                if fileContent['URL'] == "":
                    #Add a news article if nothing was given
                    with open(ms2NewsJSON, "w") as write_file:
                        json.dump(fileContent, write_file, indent=4)
                elif fileContent['URL'] != latestArticle:
                    #if the latest news article is not already in json
                    fileContent['URL'] = latestArticle
                    fileContent['publishedOn'] = latestArticleDate
                    with open(ms2NewsJSON, "w") as write_file:
                        json.dump(fileContent, write_file, indent=4)
                        await updateChannel.send("http://maplestory2.nexon.net" + latestArticle)
            except Exception as e:
                print(e)
        await asyncio.sleep(360)  # task runs every 60 seconds

    async def _announceBossSpawn(self):
        """Background task that is always on and writes in the channel when a boss is about to spawn """
        await self.wait_until_ready()        

        targetChannel = self.get_channel(self.bossSpawnerChannel)        
        fileContent=""        
        try:
            with open(bossSpawnerJson) as file:
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
                content = self.formatJSON(bossNames,bossesSpawnInfo)               
            except Exception as e:
                print(e)
            if (content != None):
                await targetChannel.send(content)                        
            await asyncio.sleep(60)#task runs every 60 seconds

    def formatJSON(self,bossNames,bossInfo):
        """Formats the JSON file so that it can be posted in the guild channel"""
        if(len(bossNames) < 1):
            # print("fuck this im out!")
            return
        content = "Bosses spawning in 5 minutes: \n"
        for boss,info in enumerate(bossInfo):
            content += f'**{bossNames[boss]}** '+"\n"
            content += "LVL: " + str(info['LVL'])+"\n"
            content += "Map: "+ info['Map']+"\n"
            content += "Spawn time: " + str(info['Spawn Time'])+"\n"
            content += "\n"                        
        print(content)  
        return content

    def googleSearch(self,searchWord):
        query = searchWord.split(" ")
        query.pop(0)
        filteredWords = ('porn','anal')
        for word in query:
            for bannedWord in filteredWords:
                if word == bannedWord:
                    return "You naughty boy. You can't google that!"
        finalQuery = ""
        if(len(query)>1):
            for wordCount,word in enumerate(query):
                if wordCount == 0:                
                    finalQuery += f'{word}'
                else:
                    finalQuery += f'+{word}'
        else:
            finalQuery = query[0]
        googleQuery = f"Here you go. https://www.google.com/search?q={finalQuery}"
        return googleQuery

    def randomReply(self):
        replies = ["Who dares summon me?!","Yes boss?","Soofa... Soofa!!","A wild soofa appeared!"]           
        reply=random.randint(0,len(replies)-1)     
        # print(reply)
        # print(replies[reply])soofa
        return replies[reply]

    def commandList(self):
        return "Command list:\n!google <search word>\n!guide\n!whostheleader\n!omak"
    




ms2bot = MS2Bot()
ms2bot.run(ms2bot.token)