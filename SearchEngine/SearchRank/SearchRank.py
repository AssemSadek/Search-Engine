from .QuerySearcher import QuerySearcher
from .Ranker import Ranker
from .Connection import Connection as connect


def takePortion(links):
    portion=[]
    i=0
    size = len(links)*0.05
    for x in links:
        if i<size:
            portion.append(x)
            i=i+1
        else:
            break
    
    print(len(links))
    print(len(portion))
    return portion

def SearchRank(text):
    connection = connect()
    connection.Start_Connection()

    try:
        querySearcher = QuerySearcher(connection.cursor, connection.db)
        ranker = Ranker(connection.cursor, connection.db)
        if text[0] == "\"" and text[len(text)-1]=="\"" :
            phrase = text[1:-1]
            links = querySearcher.phraseSearch(phrase)
        else:
            links, words = querySearcher.search(text)
        
        portion = links
        
        if len(links) == 0:
            print ("No links found")
            return [],[],[]
            
        if len(links) >= 100:    
            portion = takePortion(links)

        if text[0] == "\"" and text[len(text)-1]=="\"" :
            rankedLinks = ranker.rankPhrase(portion,phrase)
            linksContent = querySearcher.linkPhraseMatching(portion, phrase)
        else:

            rankedLinks = ranker.rank(portion,words)
            linksContent = querySearcher.linkWordMatching(portion, words)
            #rint(type(linksContent))
            #   print(key)
            #input()
            
        linksDetails = querySearcher.linkDetails(portion)
        
        #for link in rankedLinks:
        '''
        print(linksDetails[link[0]][0])
        print(link[1])
        print(linksDetails[link[0]][1])
        #print(linksContent[link[0]])
        #input()
        print("\n")
        '''
        
    finally:     
        connection.Close_Connection()
        
    return rankedLinks,linksDetails,linksContent
       

#s = raw_input("Search Bar")
#SearchRank(s)

