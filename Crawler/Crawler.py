'''
Created on Mar 20, 2017

@author: Lana Shafik
'''
#import urllib.request
#from Files import *
#from urllib.request import urlopen
from urllib.parse import urlparse
from LinkFinder import LinkFinder
import threading
import robots
import requests
import Queries
from bs4 import BeautifulSoup as BS
from time import sleep
import datetime
'''import Connection
from sqlalchemy.sql.expression import except_

connection = Connection.Connection()
connection.Start_Connection()'''



threadLock = threading.Lock()
lock = threading.Lock()
threadLock_DB = threading.Lock()
threadLock_Queue = threading.Lock()
threadLock_Crawled = threading.Lock()

webDictionary = {"https://www.stackoverflow.com/": 1, "https://www.quora.com/": 1, "http://www.edition.cnn.com/": 0.5, "http://www.bbc.com/": 0.5, "http://www.ahram.org.eg/": 0.5, "https://www.theguardian.com/international": 0.5, "https://www.youtube.com/": 1.5, "https://vimeo.com/": 1.5}
listWebsites = ["https://www.youtube.com/",  "https://www.stackoverflow.com/", "https://www.quora.com/", "http://www.edition.cnn.com/", "http://www.bbc.com/", "https://www.theguardian.com/international", "https://vimeo.com/", "http://www.ahram.org.eg/"]

queue = set()
crawled = set()
        

class CrawlerThread(threading.Thread):
    k = 0
    def __init__(self, crawler):
        threading.Thread.__init__(self)
        self.crawler = crawler
        
    def run(self):
        try:
            threadLock.acquire()
            while (CrawlerThread.k < len(listWebsites)):
                self.crawler.startingUrl = listWebsites[CrawlerThread.k]
                CrawlerThread.k = CrawlerThread.k + 1
                threadLock.release()
                self.crawler.start_crawling()
                threadLock.acquire()
                
            threadLock.release()
        except KeyboardInterrupt:
            print("saving")
            for url in queue:
                Queries.insert_queue(Crawler.cursor, url, 0, 0)
                Crawler.db.commit()
            print("done saving")    
            
            

class Crawler(object):
    cursor = None
    db = None
    l = 0
    
    def __init__(self, startingUrl, maxDepth):
        self.startingUrl = startingUrl
        self.maxDepth = maxDepth
        #self.webDictionary = webDictionary
        self.depth = 0
        #self.cursor = cursor
        #self.db = db
    
    @staticmethod
    def boot():
        print("booting")
        rows = Queries.get_all_links(Crawler.cursor)
        for row in rows:
            if(row[3] == 1): # visited
                crawled.add(row[1])
            else:
                queue.add(row[1])
        Queries.delete_all_not_visited(Crawler.cursor)  
        Crawler.db.commit()
        print(len(crawled))
        print(len(queue))
        print("finish booting")

    def get_html(self,url):
        try:
            page = requests.get(url).text
            soup = BS(page, "html.parser")
            soup = soup.renderContents().decode()
            return soup
        
        except KeyboardInterrupt:
            raise KeyboardInterrupt
     
    def get_difference(self, previous):
        try:
            now = datetime.datetime.now()
            hours = now.hour - previous.hour
            minutes = now.minute - previous.minute
            days = now.day - previous.day
            difference = hours + (days * 24) + (minutes / 60)
            return difference
        
        except KeyboardInterrupt:
            raise KeyboardInterrupt
    
    def get_base_link(self, link):
        try:
            parsed = urlparse(link)
            base = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed)    
            return base
        
        except KeyboardInterrupt:
            raise KeyboardInterrupt
         
    def start_crawling(self):
        self.crawl(self.startingUrl)         
    
    def fetch_and_set(self, link):
        try:
            if(requests.get(link).status_code == 200):
                robot = robots.robots(link)
                if(robot.Is_Allowable()):
                    threadLock_Queue.acquire()
                    self.add_links_to_queue(self.gather_links(link))
                    threadLock_Queue.release()
                    delay = robot.Get_Delay() 
                    if(delay is not None):
                        sleep(delay)
                        
                    return True
                        
                else:
                    return False
                
            else:
                return False
            
        except KeyboardInterrupt:
            raise KeyboardInterrupt
                                        
        
    def crawl(self, pageUrl):
        print("crawling")
        print(pageUrl)
        try:
            if(pageUrl not in queue): 
                if(pageUrl in crawled):
                    threadLock_DB.acquire()
                    row = Queries.get_link(Crawler.cursor, pageUrl)
                    threadLock_DB.release()
                    frequency = row[6] 
                    lastVisited = row[5]
                    difference = self.get_difference(lastVisited)

                    if(difference >= frequency):
                        content = self.get_html(pageUrl)
                        now = datetime.datetime.now()
                        
                        if(self.fetch_and_set(pageUrl)):
                            threadLock_DB.acquire()
                            Queries.update_link(Crawler.cursor, row[0], content, now)
                            Crawler.db.commit()
                            threadLock_DB.release()   
                    
                    
                else:
                    if(self.fetch_and_set(pageUrl)):
                        content = self.get_html(pageUrl)
                        base = self.get_base_link(pageUrl)
                        frequency = webDictionary.get(base)
                        if(frequency == None):
                            frequency = 3
                        now = datetime.datetime.now()
                        threadLock_DB.acquire()
                        Queries.insert_link(Crawler.cursor, pageUrl, content, 1, 0, now, frequency)
                        Crawler.db.commit()
                        threadLock_DB.release()
                        print(pageUrl)
                        threadLock_Crawled.acquire()
                        crawled.add(pageUrl)
                        threadLock_Crawled.release()
                            
                
            
            while (self.depth < self.maxDepth):
                linksList = list(queue)
                count = len(linksList)
                #for link in linksList:
                lock.acquire()
                while (Crawler.l < len(linksList)):
                    print(count)
                    link = linksList[Crawler.l]
                    Crawler.l = Crawler.l + 1
                    lock.release()
                    
                    if(link in crawled):
                        threadLock_DB.acquire()
                        row = Queries.get_link(Crawler.cursor, link)
                        threadLock_DB.release()
                        frequency = row[6] 
                        lastVisited = row[5]
                        difference = self.get_difference(lastVisited)

                        if(difference >= frequency):
                            content = self.get_html(link)
                            now = datetime.datetime.now()
                    
                            if(self.fetch_and_set(link)):
                                threadLock_DB.acquire()
                                Queries.update_link(Crawler.cursor, row[0], content, now)
                                Crawler.db.commit()
                                threadLock_DB.release()        

                    else:
                        if(self.fetch_and_set(link)):
                            content = self.get_html(link)
                            base = self.get_base_link(link)
                            frequency = webDictionary.get(base)
                            if(frequency == None):
                                frequency = 3
                            now = datetime.datetime.now()
                            threadLock_DB.acquire()
                            Queries.insert_link(Crawler.cursor, link, content, 1, 0, now, frequency)
                            Crawler.db.commit()
                            print(link)
                            threadLock_DB.acquire()
                            threadLock_Queue.acquire()
                            queue.remove(link)
                            threadLock_Queue.release()
                            threadLock_Crawled.acquire()
                            crawled.add(link)
                            threadLock_Crawled.release()
                    
                    count = count - 1        
                lock.release()
                self.depth  = self.depth + 1
                  
        except KeyboardInterrupt:
            raise KeyboardInterrupt    
        except Exception:
            print(Exception)
        
    def gather_links(self, pageUrl):
        try:
            finder = LinkFinder(pageUrl)
            finder.get_links_from_page()
            return finder.page_links()
        
        except KeyboardInterrupt:
            raise KeyboardInterrupt                
        except:
            return set()  
         
    
    
    def add_links_to_queue(self, links):
        try:
            for link in links:
                if(link not in queue):
                    queue.add(link)                    
                    
        except KeyboardInterrupt:
            raise KeyboardInterrupt
                        