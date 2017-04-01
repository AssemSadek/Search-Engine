'''
Created on Mar 22, 2017

@author: Lana Shafik
'''
import mysql.connector

class Connection:
    def __init__(self):
        self.db = None
        self.cursor = None
    
    
    def Start_Connection(self):
        self.db = mysql.connector.connect(user='SEARCH_ENGINE',password='mafeshbanatfehandasa',host = '197.133.73.82', database='SEARCH_ENGINE')
        #self.db = mysql.connector.connect(user='root',password='7890',host = 'localhost', database='SEARCH_ENGINE')
        self.cursor = self.db.cursor()
        print("connected")
    
        
    def Close_Connection(self):
        self.db.commit()
        self.cursor.close()
        self.db.close()
        print("disconnected")