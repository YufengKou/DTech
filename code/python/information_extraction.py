# -*- coding: utf-8 -*-
"""
Created on Wed May 17 15:33:56 2017

@author: ykou
"""
import nltk
import re
import pandas as pd
#import csv
import unicodecsv as csv

def get_keyword_set():
    keywords = "system, systems, equipment, function, functions, device, devices, channel, channels, component, components, instrument, instruments," + \
           "subsystem, subsystems, logic, unit, units, trip, trips, multiplex, switchgear, sensor, detector, controller, algorithm, indicator, " + \
           "indicators, indication, set, sets, algorithm, algorithms, network"

    TermSet = set(re.split(', ',keywords))
    return TermSet

def get_unwanted_entity_set():
    keywords = ["system", "systems", "information", "section", "chapter", "equipment", "design", "standard", "figure", "reference", "sections"]
    return set(keywords)

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

##  find all noun phrases
def find_noun_phrases(input_file):
    text = ""
    with open(input_file, 'r', encoding="utf8") as myfile:
        text=myfile.read().replace('\n', '')    
    print(text)
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
        #print(s)
        np_list = np_list + chunk_noun_phrase(s, grammar, ['NP', 'VP'])
    
    org_list = [conert_tags_to_original_string(str(x)) for x in np_list]    
    org_list = [modify_string(x) for x in org_list]
    df = pd.DataFrame({"Noun_Phrase": np_list, "Orignal_String": org_list})
    return df


def modify_string(x):
    chars_to_remove = ['.', '!', '?', '"', '“', '•']
    x = x.translate(''.join(chars_to_remove))
    return x

def filter_condition(x):
    length = len(x)
    if length < 3 or x.isdigit():
        return False
    if len(x.split(" ")) == 1 and x.lower() in get_unwanted_entity_set():
        return False
    if  len(x.split(" ")) == 1 and x.islower():
        return False
    
    pattern = re.compile('^.*(document|documents|chapter|section|criteria|sections|chapters|revision|reference)$')
    if  pattern.match(x.lower()):
        return False
    
    return True
# this is to do some cleaning work, including: 
# (1) remove some characters like ' or "
# (2) remove the whole entity, like "the system" or "the information"
def post_filter(np_list, org_list):
    new_o_list = [modify_string(x) for x in org_list]
    return np_list, new_o_list        

def test(input_file, output_file):
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
   
    
    
#############################################################
## 
#############################################################

    
if __name__ == "__main__":
    input_file = "../../documents/chapter_7.txt"
    output_file = input_file + "_noun_phrase.csv"
    test(input_file, output_file)
