# -*- coding: utf-8 -*-
"""
Created on Wed May 17 15:33:56 2017

@author: ykou
"""
import nltk
import re
import pandas as pd
#import csv
#import unicodecsv as csv
import codecs
import GraphDB
import TripletGenerator

def get_keyword_set():
    keywords = "system, systems, equipment, function, functions, device, devices, channel, channels, component, components, instrument, instruments," + \
           "subsystem, subsystems, logic, unit, units, trip, trips, multiplex, switchgear, sensor, detector, controller, algorithm, indicator, " + \
           "indicators, indication, set, sets, algorithm, algorithms, network"

    TermSet = set(re.split(', ',keywords))
    return TermSet

def get_unwanted_entity_set():
#    keywords = ["system", "systems", "information", "section", "chapter", "equipment", "design", 
#                "standard", "figure", "reference", "sections", "they", "it", "which", "that", "those", 
#                "examples", "details"]
    text_file = open("unwanted_entities.txt", "r")
    lines = text_file.read().split('\n')
    text_file.close()
    return set(lines)

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
   #print(tree)
   #tree.draw()
   for subtree in tree.subtrees():
      if subtree.label() in filters: 
          #print(subtree)
          list_subtrees.append(subtree)
   return list_subtrees

## convert tags to original text
def conert_tags_to_original_string(tag_str):
    tag_list = tag_str.split(" ")
    if len(tag_list) <= 1:
        return ""
        
    tag_list = tag_list[1:]
    str_list = [x.split('/')[0] for x in tag_list]
    s = " ".join(str_list)
    s = s[:-1]
    return " ".join(str_list)

def parse_to_sentences(text):
    paragraphs = re.split('\r\r|\n\n|\r\n\r\n', text)    
    #paragraphs = text.split(["\r\n\r\n", "\n\n"])
    sentences = []
    for p in paragraphs:
        sentences = sentences + nltk.sent_tokenize(p)
     
    sentences = [s.strip().replace('\n', '').replace('\r', '') for s in sentences]
    print("before filtering short sentences: {}".format(len(sentences))) 
    sentences = [s for s in sentences if len(s) > 2]    
    print("after filtering short sentences: {}".format(len(sentences))) 
    return sentences

##  find all noun phrases
def find_noun_phrases(input_file):
    text = ""
    myfile = codecs.open(input_file, "r", "utf-8")
    text = myfile.read()
    # The commented code is only for python 3
    #with open(input_file, 'r', encoding="utf8") as myfile:
    #    text=myfile.read().replace('\n', '')    
    #print(text)
    #text = "The main control room is implemented as a set of compact operator consoles featuring color graphic displays and soft control input devices."
    sentences = parse_document(text)
    print("{} sentences are obtained".format(len(sentences)))
#    grammar = r"""
#        NP: {<DT>?((<JJ.*>|<NN.*>)+<IN>?<NN.*>+)}
#        VP: {<VB.*>+(<TO>|<IN>)?}
#        CLAUSE: {<NP><VP><NP>}"""
    grammar = r"""
        NP: {(<JJ.*>?<NN.*>+) (<IN>?(<JJ.*>?<NN.*>+))*}
              """
    np_list = []
    for s in sentences:
        print(s)
        np_list = np_list + chunk_noun_phrase(s, grammar, ['NP', 'VP'])
    
    org_list = [conert_tags_to_original_string(str(x)) for x in np_list]    
    org_list = [modify_string(x) for x in org_list]
    df = pd.DataFrame({"Noun_Phrase": np_list, "Orignal_String": org_list})
    return df


def modify_string(x):
    chars_to_remove = ['.', '!', '?', '"', '“', '•']
    #x = x.translate(''.join(chars_to_remove))  # python 3 method
    for c in chars_to_remove:    
        x = x.replace(c, '')  
    return x

def filter_condition(x):
    length = len(x)
    if length < 3 or x.isdigit():
        return False
    if len(x.split(" ")) == 1 and x.lower() in get_unwanted_entity_set():
        return False
    if  len(x.split(" ")) == 1 and x.islower():
        return False
    
    pattern = re.compile('^.*(document|documents|chapter|section|criteria|sections|chapters|revision|reference|example)$')
    if  pattern.match(x.lower()):
        return False
    
    return True
# this is to do some cleaning work, including: 
# (1) remove some characters like ' or "
# (2) remove the whole entity, like "the system" or "the information"
def post_filter(np_list, org_list):
    new_o_list = [modify_string(x) for x in org_list]
    return np_list, new_o_list        

def populate_graph_db(entity_dict, triplets):
    entities = list(entity_dict)
    relList = []    
    for t in triplets:
        if (t[0] in entity_dict) and (t[2] in entity_dict):
            print("subject: {},   rel: {},  object: {}".format(t[0], t[1], t[2]) )
            relList.append(t)
            
    db = GraphDB.GraphDB("http://localhost:7474", username="neo4j", password="Neo4j3342")
#    try:
#        db.remove_all_nodes_with_a_label("Entity")
#    except Exception:
#        print("cannot find the label: {}".format("Entity"))
#        pass  # or you could 
    db.create_entities("Entity", entities)    
    db.create_relations("Entity", relList)

def dedup_triplets(triplets):
    dict_triplets = {}
    for t in triplets:
        key = t[0] + ":" + t[1] + ":" + t[2]
        dict_triplets[key] = t
    print("before dedup, len={}, after dedup len={}".format(len(triplets), len(dict_triplets)))
    return dict_triplets.values()
        
 
def get_relations_from_document(txt_file):
    myfile = codecs.open(input_file, "r", "utf-8")
    text = myfile.read()
    # The commented code is only for python 3
    #with open(input_file, 'r', encoding="utf8") as myfile:
    #    text=myfile.read().replace('\n', '')    
    #text = "The main control room is implemented as a set of compact operator consoles featuring color graphic displays and soft control input devices."
    tg = TripletGenerator.TripletGenerator()
    #text = text.replace("\r", "").replace("\n", "")
    #text = ' '.join(text.split(" "))
    sentences = parse_to_sentences(text)
#    text = "7.  Instrumentation and Controls CHAPTER 7 INSTRUMENTATION AND CONTROLS 7.1 Introduction AP1000 Design Control Document The instrumentation and control systems presented in this chapter provide protection against unsafe reactor operation during steady-state and transient power operations. They initiate selected protective functions to mitigate the consequences of design basis events. This chapter relates the functional performance requirements, design bases, system descriptions, and safety evaluations for those systems."
    #text = text.encode('ascii', errors='backslashreplace')

    triplets = []
    for s in sentences:
        #print(s)
        t = s.encode('ascii', errors='backslashreplace')
        triplets = triplets + tg.parse_sentence(t)
       
    return dedup_triplets(triplets)       


def entity_relation_extraction(input_file, output_file):
    df = find_noun_phrases(input_file)
    print("len before: {}".format(len(df)))
    df = df[df["Orignal_String"].apply(filter_condition)]
    df.to_csv(output_file, index=False)
    print("len after: {}".format(len(df)))
    
    comp_dict = set()
    for i in range(len(df)):
        comp_dict.add(df.iloc[i]["Orignal_String"])
    
    df = pd.DataFrame({"components": list(comp_dict)})
    print("len of df: {}".format(len(df)))
    df.to_csv('chapter_7_entities.csv', encoding='utf-8', index=False)
    
    triplets = get_relations_from_document(input_file)
    print(triplets)
    populate_graph_db(comp_dict, triplets)

    
#############################################################
## 
#############################################################
def test_sentence_split():
    text = '''Introduction 

AP1000 Design Control Document 

The instrumentation and control systems presented in this chapter provide protection against 
unsafe reactor operation during steady-state and transient power operations. They initiate selected 
protective functions to mitigate the consequences of design basis events. This chapter relates the 
functional performance requirements, design bases, system descriptions, and safety evaluations for 
those systems. The safety evaluations show that the systems can be designed and built to conform 
to the applicable criteria, codes, and standards concerned with the safe generation of nuclear 
power. '''
    print(text)
    sentences = parse_to_sentences(text)
    print(sentences)
    #output_file = input_file + "_noun_phrase.csv"
    #test(input_file, output_file)


if __name__ == '__main__': 
#    get_unwanted_entity_set()
    #    test_sentence_split()
    input_file = '../../documents/chapter_7.txt'    
    output_file = input_file + "_noun_phrase.csv"
    entity_relation_extraction(input_file, output_file)
       
    
