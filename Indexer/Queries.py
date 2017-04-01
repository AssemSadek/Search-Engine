class queries:
    def __init__(self,cursor):
        self.cursor = cursor

    def Get_html(self):
        Query_Get_Links = "select* from web_pages where Indexed = 0 and Visited =  1"
        self.cursor.execute(Query_Get_Links)
        rows = self.cursor.fetchall()
        return rows
     
    def insert_word_DB(self,L_ID,All_Words,TF,No_Titles,No_Headers,No_Others):
        Query_Delete = "Delete From words where L_ID = %s"
        Query_Insert = "insert into words(word,L_ID,TF,No_Titles,No_Headers,No_others) values(%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(Query_Delete, (L_ID,))
        i = 0
        input()
        for x in All_Words:
            args =(x.encode("utf-8"),L_ID,TF[i],No_Titles[i],No_Headers[i],No_Others[i])
            self.cursor.execute(Query_Insert, args)
            i = i + 1
    
    def insert_phrase_DB(self,L_ID,All_Titles,All_Headers,All_Others):
        Query_Delete = "Delete From phrase where L_ID = %s"
        Query_Insert = "insert into phrase(word,L_ID,Pos,Type) values(%s,%s,%s,%s)"
        self.cursor.execute(Query_Delete, (L_ID,))
        
        i = 0
        for x in All_Titles:
            args = (x.encode("utf-8"),L_ID,i,"Title")
            self.cursor.execute(Query_Insert, args)
            i = i + 1
        i = 0
        for x in All_Headers:
            args = (x.encode("utf-8"),L_ID,i,"Header")
            self.cursor.execute(Query_Insert, args)
            i = i + 1
        i = 0
        for x in All_Others:
            args = (x.encode("utf-8"),L_ID,i,"Other")
            self.cursor.execute(Query_Insert, args)
            i = i + 1
            
    def Indexed(self,L_ID):
        Query_Indexed = "Update web_pages set Indexed = %s where ID = %s"
        args = (1,L_ID)
        self.cursor.execute(Query_Indexed, args)        