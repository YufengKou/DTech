# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 16:35:51 2017

@author: ykou
"""

from pycorenlp import StanfordCoreNLP 
import pandas as pd
 
if __name__ == '__main__': 
    nlp = StanfordCoreNLP('http://localhost:9000') 
#    text = ('The plant control system contains nonsafety-related control and instrumentation equipment to change reactor power, control pressurizer pressure and level, control feedwater flow, and perform other plant functions associated with power generation.') 
#    text = ('The operation and control centers system includes the main control room, the technical support center, the remote shutdown room, emergency operations facility, local control stations and associated workstations for these centers.') 
#    text = ('I love Shanghai and New York.') 
    text = ('I study in Stanford. I study in Princeton.') 
    output = nlp.annotate(text, properties={ 
        'annotators': 'tokenize,ssplit,pos,depparse,parse,ner,openie', 
         'outputFormat': 'json' 
     }) 
     
    subList = []
    objList = [] 
    relList = []
    for s in output['sentences']:
        for ie in s['openie']:
            openie = s['openie']
            subList.append(ie['subject'])
            objList.append(ie['object'])
            relList.append(ie['relation'])
    
    df = pd.DataFrame({"subject":subList, "relation":relList, "object":objList})
    df.to_csv("openie_relation.csv", encoding='utf-8') 
#    print(output)
    print(output['sentences'][0]['openie']) 
#    print(output['sentences'][0]['parse']) 
#    output = nlp.tokensregex(text, pattern='/You like/', filter=False) 
#    print(output) 
#    output = nlp.semgrex(text, pattern='{tag: VBD}', filter=False) 
#    print(output) 


