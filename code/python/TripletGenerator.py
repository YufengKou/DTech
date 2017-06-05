# -*- coding: utf-8 -*-
"""
Created on Mon May 29 19:54:58 2017

@author: Yufeng
"""
from pycorenlp import StanfordCoreNLP
 

class TripletGenerator:
    def __init__(self):
        self.nlp = StanfordCoreNLP('http://localhost:9000') 

    def parse_sentence(self, text):
        #text = ('The operation and control centers system includes the main control room, the technical support center, the remote shutdown room, emergency operations facility, local control stations and associated workstations for these centers.') 
        output = self.nlp.annotate(text, properties={ 
            'annotators': 'tokenize,ssplit,pos,depparse,parse,openie', 
            'outputFormat': 'json' 
         }) 
         
        tList = []
        #print(output)
        for s in output['sentences']:
            #print(s)
            for ie in s['openie']:
                t = (ie['subject'], ie['relation'], ie['object'])
                #print(t)
                tList.append(t)

        return tList

    def parse_sentences(self, sentences):
        triplets = []
        for s in sentences:
            tList = self.parse_sentence(s)
            triplets = triplets + tList

        return triplets
    
if __name__ == '__main__': 
    csv_file = "test_triplet.csv"
    text = "I love the dog and the cat. fingers are a part of a hand."
    tg = TripletGenerator()
    triplets = tg.parse_sentence(text)
    print(triplets)         
        