'''
@author Ahmed Hassan Koshek
'''

import Connection as connect
import Indexer as Index
import sys
connection = connect.Connection()
if __name__ == '__main__':
    connection.Start_Connection()
    print("Successfully connected to Database")
    
    try:
        while (True):
            Indexer = Index.CreateIndex(connection.cursor)
            connection.db.commit()
    except KeyboardInterrupt:
        print("The Indexer is Exiting")
        connection.Close_Connection()
        sys.exit(0)  