import mysql.connector

class Connection:
    def __init__(self):
        self.db = None
        self.cursor = None
    
    
    def Start_Connection(self):
        self.db = mysql.connector.connect(user='SEARCH_ENGINE',password='mafeshbanatfehandasa',host = '192.168.8.101', database='search_engine', charset='utf8', use_unicode=True)
        #self.db = mysql.connector.connect(user='Assem',password='tt66tt66',host = 'localhost', database='SEARCH_ENGINE', charset='utf8', use_unicode=True)
        self.cursor = self.db.cursor()
        self.cursor.execute("SET SQL_SAFE_UPDATES = 0;")
        self.cursor.execute("set names utf8;")
    
        
    def Close_Connection(self):
        print("DISCONNECTED")
        self.db.commit()
        self.cursor.close()
        self.db.close()