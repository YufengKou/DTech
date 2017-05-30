# -*- coding: utf-8 -*-
"""
Created on Mon May 29 19:54:58 2017

@author: Yufeng
"""
from pycorenlp import StanfordCoreNLP
 

class TripletGenerator:
    def __init__(self):
        self.nlp = StanfordCoreNLP('http://localhost:9000') 

    def parse_sentences(self, sentence, csv_file):
        #text = ('The operation and control centers system includes the main control room, the technical support center, the remote shutdown room, emergency operations facility, local control stations and associated workstations for these centers.') 
        output = self.nlp.annotate(sentence, properties={ 
            'annotators': 'tokenize,ssplit,pos,depparse,parse,ner,openie', 
             'outputFormat': 'json' 
         }) 
         
        tList = []
        for s in output['sentences']:
            for ie in s['openie']:
                t = (ie['subject'], ie['relation'], ie['object'])
                tList.append(t)

        return tList
    
if __name__ == '__main__': 
    tg = TripletGenerator()
    csv_file = "test_triplet.csv"
    sentences = ["I love the dog and the cat.", "fingers are a part of a hand."]
    triplets = []
    for s in sentences:
        tList = tg.parse_sentences(s, csv_file)
        triplets = triplets + tList
    print(triplets)         
        