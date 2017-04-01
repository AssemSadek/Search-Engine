'''
Created on Mar 19, 2017

@author: Lana Shafik
'''
#from urllib.parse import urljoin
import robotexclusionrulesparser
from urllib.parse import urlparse

class robots():
    def __init__(self, url):
        #self.baseUrl = baseUrl
        self.url = url
        self.agent = "*"
        
        
    def Is_Allowable(self):
        try:
            parsedUrl = urlparse(self.url)
            base = parsedUrl[1]
            robotsUrl = "http://" + base + "/robots.txt"
            parser  = robotexclusionrulesparser.RobotExclusionRulesParser()
            parser.user_agent = self.agent
            parser.fetch(robotsUrl)
            return (parser.is_allowed(self.agent, self.url))
        except:
            return False
    

    def Get_Delay(self):
        parser  = robotexclusionrulesparser.RobotExclusionRulesParser()
        parser.user_agent = self.agent
        return (parser.get_crawl_delay(parser.user_agent))
        
    
    
    
'''from urllib import robotparser
from urllib.parse import urljoin

class robots():
    def __init__(self, baseUrl, url):
        self.baseUrl = baseUrl
        self.url = url
        
    def Is_Allowable(self):
        agent = "*"    
        parser = robotparser.RobotFileParser()
        parser.set_url(urljoin(self.baseUrl, '/robots.txt'))
        parser.read()
        return (parser.can_fetch(agent, self.url))'''
        
        