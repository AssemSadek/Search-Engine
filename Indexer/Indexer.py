from bs4 import BeautifulSoup as BS
import re
from nltk.stem import PorterStemmer
import Queries as Queries

porter=PorterStemmer()

class CreateIndex:
    cursor = None
    soup = None
    L_ID = None
    Removal_words = ['the', 'for', 'a', 'is', 'an', '', 'by', 'on', 'in', 'to', '_', ' ', '-', '|','\\','.',',','?']
    Title, H1, H2, H3, H4, H5, H6, P, LI, Table = [],[],[],[],[],[],[],[],[],[]
    All_Words, All_Headers, All_Others, All_Titles = [],[],[],[]
    No_Titles, No_Headers, No_Others, TF, Pos , W_Type= [],[],[],[],[],[]
    
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
    
    def __init__(self, cursor):
        Query = Queries.queries(cursor)
        rows = Query.Get_html()
        for row in rows:
            print(row[0])
            self.L_ID = row[0]
            self.soup = row[2]
            self.soup = self.soup.replace('class="srow bigbox container mi-df-local locked-single"', 'class="row bigbox container mi-df-local single-local"')
            self.soup = BS(self.soup,"html.parser")
            self.Get_Text_In_Tags() 
            self.Get_List_Words()
            self.Calculations()

            Query.insert_word_DB(self.L_ID,self.All_Words,self.TF,self.No_Titles,self.No_Headers,self.No_Others)
            Query.insert_phrase_DB(self.L_ID,self.All_Titles,self.All_Headers,self.All_Others)
            Query.Indexed(self.L_ID)
            
            self.All_Words, self.All_Headers, self.All_Others, self.All_Titles = [],[],[],[]
            self.No_Titles, self.No_Headers, self.No_Others, self.TF, self.Pos , self.W_Type= [],[],[],[],[],[]
            