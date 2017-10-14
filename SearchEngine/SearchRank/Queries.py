class Queries:
    def __init__(self,cursor):
        self.cursor = cursor

    def insert_autocomplete(self,word):
        Qury_check_ifexist='select* from autocomplete where query=%s'
        Query_insert_autocomplete = "insert into autocomplete (query) values(%s)"
        self.cursor.execute(Qury_check_ifexist, (word,))
        rows = self.cursor.fetchall()
        if(len(rows)==0):
            self.cursor.execute(Query_insert_autocomplete, (word,))

    def get_tot_num_words(self, L_ID): 
        Query_get_tot_num_words = "select sum(TF) from words where L_ID= %s"
        self.cursor.execute(Query_get_tot_num_words, (L_ID,))
        rows = self.cursor.fetchall()
        return rows[0][0]
    
    def get_all_links(self,word):
        Query_get_all_links= "select L_ID from words where word=%s"
        self.cursor.execute(Query_get_all_links, (word,))
        rows = self.cursor.fetchall()
        return rows
    
    def get_occurencies(self, word, L_ID):
        Query_get_occurencies = "select TF from words where word= %s and L_ID= %s"
        args =(word.encode("utf-8"),L_ID)
        self.cursor.execute(Query_get_occurencies, args)
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            return 0;
        return rows[0][0]


    def get_word_data(self, word, L_ID):
        Query_get_occurencies = "select* from words where word= %s and L_ID= %s"
        args =(word.encode("utf-8"),L_ID)
        self.cursor.execute(Query_get_occurencies, args)
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            return 0;
        return rows[0]


    
    def get_tot_num_links(self):
        Query_get_tot_num_links = "select count(ID) from web_pages"
        self.cursor.execute(Query_get_tot_num_links)
        rows = self.cursor.fetchall()
        return rows[0][0]
    
    def get_num_links_per_word(self, word):
        Query_get_num_links_per_word = "select count(word) from words where word=%s"
        self.cursor.execute(Query_get_num_links_per_word, (word,))
        rows = self.cursor.fetchall()
        return rows[0][0]
    
    def get_popularity(self, L_ID):
        Query_get_popularity = "select Popularity from web_pages where ID=%s"
        self.cursor.execute(Query_get_popularity, (L_ID,))
        rows = self.cursor.fetchall()
        return rows[0][0]
    
    def get_links_word(self, word):
        Query_get_links_word = "select L_ID from words where word=%s"
        self.cursor.execute(Query_get_links_word, (word,))
        rows = self.cursor.fetchall()
        return rows
    
    def get_url(self, L_ID):

        Query_get_link = "select Link from web_pages where ID=%s"
        self.cursor.execute(Query_get_link, (L_ID,))
        rows = self.cursor.fetchall()
        return rows[0][0].decode("utf-8")
    
    def Get_html(self,L_ID):
        Query_Get_Links = "select content from web_pages where ID = %s"
        self.cursor.execute(Query_Get_Links, (L_ID,))
        rows = self.cursor.fetchall()
        return rows    

    def Get_unstemed(self,word,L_ID):
        Query_Get_unstemed = "select unstemed from words where L_ID=%s and word=%s"
        args=(L_ID,word)
        self.cursor.execute(Query_Get_unstemed, args)
        rows = self.cursor.fetchall()
        if(len(rows)==0):
            return ""
        return rows[0][0].decode("utf-8")
    
    def phrase_search(self, phrase):
        links=[]
        phrase = phrase.lower()
        word = phrase.split()

        if(len(word)==1):
            Query_phrase_search = "select L_ID from words where unstemed=%s"
            self.cursor.execute(Query_phrase_search, (word[0],))
        else:
            Query_phrase_search = "select p0.L_ID from "
            i=0
            for x in word:
                Query_phrase_search += "phrase p" + str(i)
                if(i< len(word)-1):
                    Query_phrase_search += ", "
                i=i+1

            Query_phrase_search += " where "
            i=0
            for x in word:
                Query_phrase_search += "p" + str(i) +".word = %s and "
                i=i+1

            i=0
            for x in word:
                Query_phrase_search += "p0.L_ID = p" + str(i) +".L_ID and "
                i=i+1

            i=0
            for x in word:
                Query_phrase_search += "p0.Type = p" + str(i) +".Type and "
                i=i+1

            i=0
            for x in word:
                if(i< len(word)-1):
                    Query_phrase_search += "p" + str(i + 1) + ".Pos - p" + str(i) + ".Pos = 1 and ";
                i=i+1

            Query_phrase_search += "p0.L_ID in (select L_ID from phrase group by L_ID having count(*) > 1) order by L_ID"

            args=(word)
            self.cursor.execute(Query_phrase_search, args)
        rows = self.cursor.fetchall()
        for x in rows:
            links.append(x[0])
        return links
        
    
            
             
    