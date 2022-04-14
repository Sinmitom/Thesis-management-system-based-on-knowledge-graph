




from py2neo import Graph, Node, Relationship, NodeMatcher

g = Graph('bolt://localhost:7687', user='neo4j', password='password')

print(len(g.nodes))