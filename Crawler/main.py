'''
Created on Mar 19, 2017

@author: Lana Shafik
'''
import threading
#from queue import Queue
from Crawler import Crawler, CrawlerThread
import Connection
from sqlalchemy.sql.expression import except_
import sys
#from Files import *




'''if __name__ == '__main__':
    numThreads = input("Number of threads: ")
    maxDepth = input("Maximum depth: ")
    
    listWebsites = ["https://www.quora.com/", "https://www.google.com.eg/", "https://www.stackoverflow.com/", "https://www.youtube.com/"]
    
    threads = []
    for i in range(int(numThreads)):
        try:
            crawler = Crawler(CRAWLER_FOLDER, listWebsites[i], int(maxDepth))
            thread = CrawlerThread(crawler)
            thread.start()
            threads.append(thread)
        except Exception:
            print("Interrupted")'''
            

 
if __name__ == '__main__': 
    numThreads = input("Number of threads: ")
    maxDepth = input("Maximum depth: ")
    
    try:
        connection = Connection.Connection()
        connection.Start_Connection()
        Crawler.cursor = connection.cursor
        Crawler.db = connection.db
        Crawler.boot()
        
        threads = []
    
        for i in range(int(numThreads)):
            crawler = Crawler("", int(maxDepth))
            thread = CrawlerThread(crawler)
            thread.start()
            threads.append(thread)
         
         
        for t in threads:
            t.join()  
        connection.Close_Connection()    
            
    except:
        print("main")
        sys.exit()
        connection.Close_Connection()

        
        '''
        
        crawler = Crawler("https://www.stackoverflow.com/", int(maxDepth), connection.cursor, connection.db)
        crawler.start_crawling()
        connection.Close_Connection()'''
            

            

         


 
 
    