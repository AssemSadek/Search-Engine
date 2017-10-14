from .Queries import Queries
import requests
import re
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer

porter=PorterStemmer()
removalWords = ['the', 'for', 'a', 'is', 'an', '', 'by', 'on', 'in', 'to', '_', ' ', '-', '|','\\','.',',','?']

def Tokenize(text):
    text = text.lower()
    pattern = re.compile("\w+")
    text = re.findall(pattern,text)
    for item in removalWords:
        text = [x for x in text if x != item]
        text=[ porter.stem(word) for word in text]
    return text


class QuerySearcher:


    def __init__(self,cursor,db):
        self.queries = Queries(cursor)
        self.db = db

        
    def search(self,text):
        print("Start Searching")
        links = set()
        words = Tokenize(text)
        for word in words: 
            
            currentLinks = self.queries.get_all_links(word)
            print (currentLinks)
            for l in currentLinks:
                links.add(l[0]);
        
        print("End Searching")
        return links,words
    
    def phraseSearch(self,phrase):
        print("Start Phrase Searching")
        x =  self.queries.phrase_search(phrase)
        print("End Phrase Searching")
        return x
    
    def linkWordMatching(self,links,words):
        print("Start Links Contents")

        linkContent = {}
        for link in links:
            rows = self.queries.Get_html(link)
            soup=rows[0][0]
            soup = soup.replace('class="srow bigbox container mi-df-local locked-single"', 'class="row bigbox container mi-df-local single-local"')
            soup = BeautifulSoup(soup, "html.parser")
            [s.extract() for s in soup('script')]
            [s.extract() for s in soup('style')]
            soup = soup.text
            soup = soup.lower()
            soup=" ".join(soup.split('\n'))
            soup=" ".join(soup.split('\r'))
            for word in words:
                word_unstemed= self.queries.Get_unstemed(word,link)
                if(word_unstemed in soup):
                    index=soup.index(word_unstemed)
                    if(index-500 >=0):
                        start=index-500
                    else:
                        start=0
                    if(index+500 <=len(soup)):
                        end=index+500
                    else:
                        end=len(soup)-1
                    while(start !=0 and soup[start]!=" " and soup[start]!="\n"):
                        start=start-1
                    if(start!=0):
                        start=start+1
                    while(end !=0 and soup[end]!=" " and soup[end]!="\n"):
                        end=end+1
                    if(end!=0):
                        end=end-1
                    text=''.join(soup[start:end])
                    linkContent[link]=text
                    break
        print("End Links Contents")
        return linkContent            
            

    def linkPhraseMatching(self,links,phrase):
        print("Start Links Contents")

        linkContent = {}
        for link in links:
            rows = self.queries.Get_html(link)
            soup=rows[0][0]
            soup = soup.replace('class="srow bigbox container mi-df-local locked-single"', 'class="row bigbox container mi-df-local single-local"')
            soup = BeautifulSoup(soup, "html.parser")
            [s.extract() for s in soup('script')]
            [s.extract() for s in soup('style')]
            soup = soup.text
            soup = soup.lower()
            soup=" ".join(soup.split('\n'))
            soup=" ".join(soup.split('\r'))
            phrase.lower()
            if(phrase in soup):
                index=soup.index(phrase)
                if(index-500 >=0):
                    start=index-500
                else:
                    start=0
                if(index+500 <=len(soup)):
                    end=index+500
                else:
                    end=len(soup)-1
                while(start !=0 and soup[start]!=" " and soup[start]!="\n"):
                    start=start-1
                if(start!=0):
                    start=start+1
                while(end !=0 and soup[end]!=" " and soup[end]!="\n"):
                    end=end+1
                if(end!=0):
                    end=end-1
                text=''.join(soup[start:end])
                linkContent[link]=text
            
        print("End Links Contents")
        return linkContent            
        
    
    
    
    def linkDetails(self,links):
        print("Start Links Details")
        
        dic = {}
        
        for link in links:
            
            l = []
            url = self.queries.get_url(link)

            rows = self.queries.Get_html(link)
            soup=rows[0][0]
            soup = soup.replace('class="srow bigbox container mi-df-local locked-single"', 'class="row bigbox container mi-df-local single-local"')
            soup = BeautifulSoup(soup, "html.parser")
            title = soup.find_all('title')
            l.append(title[0].text)
            l.append(url)
            dic[link] = l

        print("End Links Details")
        return dic

                