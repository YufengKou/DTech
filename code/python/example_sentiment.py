# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 16:35:51 2017

@author: ykou
"""

from pycorenlp import StanfordCoreNLP 

 
if __name__ == '__main__': 
    nlp = StanfordCoreNLP('http://localhost:9000') 
    text = ( 
        'The plant control system contains nonsafety-related control and instrumentation equipment to change reactor power, control pressurizer pressure and level, control feedwater flow, and perform other plant functions associated with power generation. The plant control system is described in subsections 7.1.3 and 7.7.1. ') 
    output = nlp.annotate(text, properties={ 
        'annotators': 'tokenize,ssplit,pos,depparse,parse', 
         'outputFormat': 'json' 
     }) 
     
    #print(output['sentences'])
    #print(output['sentences'][0]['parse']) 
    output = nlp.tokensregex(text, pattern='/You like/', filter=False) 
    print(output) 
    output = nlp.semgrex(text, pattern='{tag: VBD}', filter=False) 
    print(output) 


##############################################333
nlp = StanfordCoreNLP('http://localhost:9000')
res = nlp.annotate("I love you. I hate him. You are nice. He is dumb",
                   properties={
                       'annotators': 'sentiment',
                       'outputFormat': 'json'
                   })
for s in res["sentences"]:
    print "%d: '%s': %s %s" % (
        s["index"],
        " ".join([t["word"] for t in s["tokens"]]),
        s["sentimentValue"], s["sentiment"])

