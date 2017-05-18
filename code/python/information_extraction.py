# -*- coding: utf-8 -*-
"""
Created on Wed May 17 15:33:56 2017

@author: ykou
"""
import nltk


# parse document string and return parsed pos tags
def parse_document(document):
   sentences = nltk.sent_tokenize(document)
   sentences = [nltk.word_tokenize(sent) for sent in sentences]
   sentences = [nltk.pos_tag(sent) for sent in sentences]
   
   return sentences

# find noun phrases by chunking the pos tags
def chunk_noun_phrase(sentence, grammar, filters):
   list_subtrees = []   
   cp = nltk.RegexpParser(grammar)
   tree = cp.parse(sentence)
   print(tree)
   tree.draw()
   for subtree in tree.subtrees():
      if subtree.label() in filters: 
          print(subtree)
          list_subtrees.append(subtree)
   return list_subtrees


def test():
    sentences = parse_document('''
AP1000 Design Control Document 

The instrumentation and control systems presented in this chapter provide protection against 
unsafe reactor operation during steady-state and transient power operations. They initiate selected 
protective functions to mitigate the consequences of design basis events. This chapter relates the 
functional performance requirements, design bases, system descriptions, and safety evaluations for 
those systems. The safety evaluations show that the systems can be designed and built to conform 
to the applicable criteria, codes, and standards concerned with the safe generation of nuclear 
power. 
''')

    print("{} sentences are obtained".format(len(sentences)))
    grammar = "NP: {<DT>?<JJ>*<NN>+}"
    for s in sentences:
        print(s)
        list_subtrees = chunk_noun_phrase(s, grammar, 'NP')
        

   
if __name__ == "__main__":
    test()
       