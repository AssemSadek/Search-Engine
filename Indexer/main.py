'''
@author Ahmed Hassan Koshek
'''

import Connection as connect
import Indexer as Index

connection = connect.Connection()

if __name__ == '__main__':
    connection.Start_Connection()
    print("CONNECTED")
    Indexer = Index.CreateIndex(connection.cursor)
    
    print("commit?")
    input()
    connection.Close_Connection()
    