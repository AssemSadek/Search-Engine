'''
Created on Mar 17, 2017

@author: Lana Shafik
'''
from html.parser import HTMLParser
from urllib import parse
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests   
from url_normalize import url_normalize
from urllib.parse import urlparse    
        
class LinkFinder (HTMLParser):
    #def __init__(self, baseUrl, pageUrl):
    def __init__(self, url):
        HTMLParser.__init__(self)
        #self.baseUrl = baseUrl
        #self.pageUrl = pageUrl
        self.url = url
        self.links = set()
    
    
    def Is_Absolute(self, url):
        return (bool((urlparse(url).netloc) and (urlparse(url).scheme)))
    

    def get_links_from_page(self):
        try:
            response = requests.get(self.url)
            contentType = response.headers.get('content-type')
        
            if((contentType == 'text/html') or (contentType == 'text/html; charset=utf-8')):
                page = urlopen(self.url)
                page = page.read()
                soup = BeautifulSoup(page, 'lxml')
                for link in soup.findAll('a', href = True):
                    if(not(self.Is_Absolute(link['href']))):
                        url = parse.urljoin(self.url, link['href'])
                    else:
                        url = link['href']
            
                    url = url_normalize(url)
                    self.links.add(url)
        except:
            self.links = set()                        
                        
    
    def page_links(self):
        return self.links