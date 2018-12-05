from bs4 import BeautifulSoup
import urllib.request

class Scrapper:
        soup = None
        url = ""
        httpResponse = None
        websiteContent = ""

        def __init__(self):
                pass
        
        #This sends a get request to the website and opens it
        def GetWebsite(self, targetURL):
                self.url = targetURL
                self.httpResponse = urllib.request.Request(self.url,data=None,headers={"User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"})
                self.websiteContent=urllib.request.urlopen(self.httpResponse)           
        #Creates the HTML Document Tree, so we can parse it
        def CreateSoup(self):
                self.soup = BeautifulSoup(self.websiteContent.read(), "html.parser")
        
        #Formats the DOM
        def PrettifyDOMTree(self):
                print(self.soup.prettify())
                
        #Don't know where I can use that yet...
        def FindAttribute(self, tags):
                targetAttribute=""
                for tag in tags:
                        targetAttribute += tag + " "
                targetAttribute = targetAttribute.rstrip()
                print("Searching for Tag...")
                for tag in self.soup.select(targetAttribute):
                        print(tag)
                                            
        def CheckCurrentNewsArticle(self,newsURL):
            """Calls the URL and the creates a soup object"""
            self.GetWebsite(newsURL)
            self.CreateSoup()
            return self.GetLatestNewsArticle()

        def GetLatestNewsArticleURL(self):
            """Gets the newest post article """
            article = self.soup.find("a",class_="news-item-link")
            return article.get('href')



scrap = Scrapper()

scrap.CheckCurrentNewsArticle("http://maplestory2.nexon.net/en/news")