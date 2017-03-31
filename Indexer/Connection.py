import mysql.connector

class Connection:
    def __init__(self):
        self.db = None
        self.cursor = None
    
    
    def Start_Connection(self):
        #self.db = mysql.connector.connect(user='SEARCH_ENGINE',password='7890',host = '41.69.147.185', database='SEARCH_ENGINE')
        self.db = mysql.connector.connect(user='root',password='7890',host = 'localhost', database='SEARCH_ENGINE', charset='utf8', use_unicode=True)
        self.cursor = self.db.cursor()
        self.cursor.execute("SET SQL_SAFE_UPDATES = 0;")
        self.cursor.execute("set names utf8;")
    
        
    def Close_Connection(self):
        print("DISCONNECTED")
        self.db.commit()
        self.cursor.close()
        self.db.close()