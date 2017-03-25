class queries:
    def __init__(self,cursor):
        self.cursor = cursor

    def Get_html(self):
        Query_Get_Links = "select* from web_pages where Indexed = 0"
        self.cursor.execute(Query_Get_Links)
        rows = self.cursor.fetchall()
        return rows
     
    def call_insert_word(self,L_ID,All_Words,TF,No_Titles,No_Headers,No_Others):
        All_Words = ",".join(All_Words)
        TF = ",".join(str(x) for x in TF)
        No_Titles = ",".join(str(x) for x in No_Titles)
        No_Headers = ",".join(str(x) for x in No_Headers)
        No_Others = ",".join(str(x) for x in No_Others)
        args = (All_Words,L_ID,TF,No_Titles,No_Headers,No_Others)
        self.cursor.callproc('insert_words', args)
    
    def call_insert_phrase(self,L_ID,All_Titles,All_Headers,All_Others):
        All_Titles = ",".join(All_Titles)
        All_Headers = ",".join(All_Headers)
        All_Others = ",".join(All_Others)
        args = (L_ID,All_Titles,All_Headers,All_Others)
        self.cursor.callproc('insert_phrase', args)
    
            
    def Indexed(self,L_ID):
        Query_Indexed = "Update web_pages set Indexed = %s where ID = %s"
        args = (1,L_ID)
        self.cursor.execute(Query_Indexed, args)
        