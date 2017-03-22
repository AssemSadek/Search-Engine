import requests
from bs4 import BeautifulSoup as BS
import re
from nltk.stem import PorterStemmer
import mysql.connector

porter=PorterStemmer()

class CreateIndex:
    db = None
    cursor = None
    soup = None
    L_ID = None
    Removal_words = ['the', 'for', 'a', 'is', 'an', '', 'by', 'on', 'in', 'to']
    Title, H1, H2, H3, H4, H5, H6, P, LI, Table = [],[],[],[],[],[],[],[],[],[]
    All_Words, All_Headers, All_Others, All_Titles = [],[],[],[]
    No_Titles, No_Headers, No_Others, TF, Pos , W_Type= [],[],[],[],[],[]
    
    def Start_Connection(self):
        self.db = mysql.connector.connect(user='SEARCH_ENGINE',password='7890',host = '192.168.0.51', database='SEARCH_ENGINE')
        #self.db = mysql.connector.connect(user='root',password='7890',host = 'localhost', database='SEARCH_ENGINE')
        self.cursor = self.db.cursor()
        
    def Close_Connection(self):
        self.db.commit()
        self.cursor.close()
        self.db.close()
        
    def Get_html(self,url):
        test_url = url
        page = requests.get(test_url).text
        soup = BS(page, "html.parser")
        return soup
    
    def Get_Text_In_Tags(self):
        self.Title = self.soup.find_all('title')
        self.H1 = self.soup.find_all('h1')
        self.H2 = self.soup.find_all('h2')
        self.H3 = self.soup.find_all('h3')
        self.H4 = self.soup.find_all('h4')
        self.H5 = self.soup.find_all('h5')
        self.H6 = self.soup.find_all('h6')
        self.P = self.soup.find_all('p')
        self.LI = self.soup.find_all('li')
        self.Table = self.soup.find_all('table')
    
    def Tokenize(self,text):
        text = text.lower()
        pattern = re.compile("\w+")
        text = re.findall(pattern,text)
        for item in self.Removal_words:
            text = [x for x in text if x != item]
        text=[ porter.stem(word) for word in text]
        return text
        
    def Get_List_Words(self):
        for x in self.Title:
            self.All_Titles.extend(self.Tokenize(x.text))
        for x in self.H1:
            self.All_Headers.extend(self.Tokenize(x.text))
        for x in self.H2:
            self.All_Headers.extend(self.Tokenize(x.text))
        for x in self.H3:
            self.All_Headers.extend(self.Tokenize(x.text))
        for x in self.H4:
            self.All_Headers.extend(self.Tokenize(x.text))
        for x in self.H5:
            self.All_Headers.extend(self.Tokenize(x.text))
        for x in self.H6:
            self.All_Headers.extend(self.Tokenize(x.text))
        for x in self.P:
            self.All_Others.extend(self.Tokenize(x.text))
        for x in self.LI:
            self.All_Others.extend(self.Tokenize(x.text))
        for x in self.Table:
            self.All_Others.extend(self.Tokenize(x.text))
        self.All_Words.extend(self.All_Headers)
        self.All_Words.extend(self.All_Titles)
        self.All_Words.extend(self.All_Others)
        self.All_Words = set(self.All_Words)
    
    def Calculations(self):
        for x in self.All_Words:
            count1 = self.All_Headers.count(x)
            count2 = self.All_Others.count(x)
            count3 = self.All_Titles.count(x)
            self.No_Headers.append(count1)
            self.No_Others.append(count2)
            self.No_Titles.append(count3)
            self.TF.append(count1+count2+count3)
        
    def insert_word_DB(self):
        Query_Delete = "Delete From words where L_ID = %s"
        Query_Insert = "insert into words(word,L_ID,TF,No_Titles,No_Headers,No_others) values(%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(Query_Delete, (self.L_ID,))
        i = 0
        for x in self.All_Words:
            args =(x,self.L_ID,self.TF[i],self.No_Titles[i],self.No_Headers[i],self.No_Others[i])
            self.cursor.execute(Query_Insert, args)
            i = i + 1
    
    def insert_phrase_DB(self):
        Query_Delete = "Delete From phrase where L_ID = %s"
        Query_Insert = "insert into phrase(word,L_ID,Pos,W_Type) values(%s,%s,%s,%s)"
        self.cursor.execute(Query_Delete, (self.L_ID,))
        
        i = 0
        for x in self.All_Titles:
            args = (x,self.L_ID,i,"Title")
            self.cursor.execute(Query_Insert, args)
            i = i + 1
        i = 0
        for x in self.All_Headers:
            args = (x,self.L_ID,i,"Header")
            self.cursor.execute(Query_Insert, args)
            i = i + 1
        i = 0
        for x in self.All_Others:
            args = (x,self.L_ID,i,"Other")
            self.cursor.execute(Query_Insert, args)
            i = i + 1
        
    def main(self,url,ID):
        self.L_ID = ID
        self.soup = self.Get_html(url) 
        self.Get_Text_In_Tags() 
        self.Get_List_Words()
        self.Calculations()       
        
        self.Start_Connection()
        print("CONNECTED")
        self.insert_word_DB()
        self.insert_phrase_DB()
        self.Close_Connection()
        

url = "http://c4m.cdf.toronto.edu/"
L_ID = None
C=CreateIndex()
C.main(url,1001)