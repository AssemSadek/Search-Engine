import os
import re
from collections import Counter
import math
import operator
from .Queries import Queries
from decimal import *
        
def calculate_tf(occurencies,totNumWords):
    tf =  occurencies / totNumWords
    return tf

def calculate_idf(totNumLinks,NumLinksPerWord):
    idf = math.log(totNumLinks / NumLinksPerWord)
    return idf



class Ranker:
    
    def __init__(self,cursor,db):
        self.queries = Queries(cursor)
        self.db = db
        
    
    def rank(self,links,words):
        print("Start Ranking")
        totNumLinks = self.queries.get_tot_num_links();
        list_to_rank = {}
        for link in links:
            sum=0;
            Popularity = self.queries.get_popularity(link)
            totNumWords = self.queries.get_tot_num_words(link)
            for word in words:
            
                occurencies = self.queries.get_occurencies(word,link)
                tf = calculate_tf(occurencies,totNumWords)
                NumLinksPerWord = self.queries.get_num_links_per_word(word)
                idf = calculate_idf(totNumLinks,NumLinksPerWord)
                score = tf * Decimal(idf)
                sum = sum + score
            
            list_to_rank[link] = sum*Decimal(Popularity)*1000000
            
        

        sorted_list = sorted(list_to_rank.items(), key=operator.itemgetter(1), reverse=True)

        print("End ranking")
        return sorted_list


    def rankPhrase(self,links,phrase):
        print("Start Ranking")
        totNumLinks = self.queries.get_tot_num_links();
        list_to_rank = {}
        
        for link in links:
            list_to_rank[link] = self.queries.get_popularity(link) 
            
        sorted_list = sorted(list_to_rank.items(), key=operator.itemgetter(1), reverse=True)

        print("End ranking")
        return sorted_list     
     