'''
@author Ahmed Hassan Koshek
'''

import Connection as connect
import Indexer as Index
import sys
import os

connection = connect.Connection()
clear = lambda: os.system('cls')

if __name__ == '__main__':   
    connection.Start_Connection()
    clear()
    print("Successfully connected to Database")
    print("Indexing...")
    
    try:
        while (True):
            Indexer = Index.CreateIndex(connection.cursor)
            connection.db.commit()
    except KeyboardInterrupt:
        clear()
        print("The Indexer is Exiting")
        connection.Close_Connection()
        sys.exit(0)