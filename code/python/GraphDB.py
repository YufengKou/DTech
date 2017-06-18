# -*- coding: utf-8 -*-
"""
Created on Tue May 30 07:51:48 2017

@author: ykou

# some sample queries:
# (1) 'MATCH (s:EntityTest)-[r]->(o:EntityTest) RETURN s, type(r), o'
# (2) 'MATCH (s:Entity)-[r]->(o:Entity) RETURN s, type(r), o'
# (3) MATCH (n:Entity) DETACH DELETE n
"""

from neo4jrestclient.client import GraphDatabase
#from neo4jrestclient import client

class GraphDB:
    def __init__(self, url=None, username=None, password=None):
        if (url is None) or (username is None) or (password is None): 
            print("Wrong url/username/password to create neo4j database.")
            exit(1)
        #db = GraphDatabase("http://localhost:7474", username="neo4j", password="Neo4j3342")
        self.db = GraphDatabase(url, username, password)

    def create_entities(self, eType, eList): 
        print("before create entities:")
        print(self.db.labels)
        label = self.db.labels.create(eType)
        for e in eList:
            entity = self.db.nodes.create(name=e)
            label.add(entity)
        print("after create entities:")
        print(self.db.labels)
 
    def create_relations(self, eType, rList):
        print("labels:{}".format(self.db.labels) )
        entity = self.db.labels.get(eType)
        for r in rList:
            subEntity = entity.get(name=r[0])
            if (subEntity is None) or len(subEntity) == 0:
                print("There is no such subject entity: {}".format(r[0]))
                continue
            #print("r[2]:{}".format(r[2]))
            objEntity = entity.get(name=r[2])
            #print("objEntity:")
            #for e in objEntity:
            #    print(e.get("name"))
            
            if (objEntity is None) or len(objEntity) == 0:
                print("There is no such object entity: {}".format(r[2]))
                continue
            rel = r[1]
            subEntity[0].relationships.create(rel, objEntity[0])
            
    def remove_all_nodes_with_a_label(self, label):
        q = 'MATCH (n:' + label +') DETACH DELETE n'
        #results = self.db.query(q, returns=(client.Node, str, client.Node))
        results = self.db.query(q)
        return results
        
def test():
    db = GraphDB("http://localhost:7474", username="neo4j", password="Neo4j3342")
    entities = ['Beijing', 'Shanghai', 'DC']
    relList = [('Beijing', 'likes', 'Shanghai'), ('DC', 'loves', 'Beijing'), ('Luoyang', 'hates', 'Nothing') ]
    db.create_entities("EntityTest", entities)
    db.create_relations("EntityTest", relList)
    db.remove_all_nodes_with_a_label("EntityTest")

        
    
    
if __name__ == "__main__":
    test()
   