import mysql.connector

class Connection:
    def __init__(self):
        self.db = None
        self.cursor = None
    
    
    def Start_Connection(self):
        #self.db = mysql.connector.connect(user='SEARCH_ENGINE',password='7890',host = '41.69.147.185', database='SEARCH_ENGINE')
        self.db = mysql.connector.connect(user='root',password='7890',host = 'localhost', database='SEARCH_ENGINE')
        self.cursor = self.db.cursor()
    
        
    def Close_Connection(self):
        self.db.commit()
        self.cursor.close()
        self.db.close()