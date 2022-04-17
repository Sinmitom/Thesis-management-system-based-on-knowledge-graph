from py2neo import Graph, Node, Relationship, NodeMatcher


class Neo4j_Handle():
    graph = None

    # matcher = None
    def __init__(self):
        print("Neo4j Init ...")

    def connectDB(self):
        self.graph = Graph('bolt://localhost:7687', user='neo4j', password='password')

    # self.matcher = NodeMatcher(self.graph)

    # 实体查询，用于命名实体识别
    def matchEntityItem(self, value):
        answer = self.graph.run("MATCH (entity1) WHERE entity1.name = \"" + value + "\" RETURN entity1").data()
        print(answer)
        return answer

    # 实体查询
    def getEntityRelationbyEntity(self, value, select):
        # 查询实体：考虑实体1类型，查找和实体1类型相关的所有实体以及关系
        print("测试调用实体查询")
        if select == 'paperName' or select == 1:  # 若实体1类型为论文
            answer = self.graph.run(
                "match (entity1:Paper) -[rel]-> (entity2) where entity1.Name = \"" + value + "\" return entity1, rel,entity2").data()
        elif select == 'authorName' or select == 2:
            answer = self.graph.run(
                "match (entity1:Author) -[rel]-> (entity2) where entity1.Name = \"" + value + "\" return entity1, rel,entity2").data()
        else:
            answer = self.graph.run(
                "MATCH (entity1) - [rel] -> (entity2)  WHERE entity1.Name = \"" + value + "\" RETURN entity1,rel,entity2").data()
            # answer = self.graph.run("match (entity1:Paper) -[rel]-> (entity2) where entity1.Name = \"" + value+ "\" return entity1, rel,entity2").data()

        return answer

    # 关系查询:实体1
    def findRelationByEntity1(self, entity1):
        # 基于论文标题查询
        answer = self.graph.run(
            "MATCH (n1:Paper {paperTitle:\"" + entity1 + "\"})- [rel] -> (n2) RETURN n1,rel,n2").data()
        # print(answer)
        # 基于论文作者查询，注意此处额外的空格
        if (len(answer) == 0):
            answer = self.graph.run(
                "MATCH (n1:Author {authorName:\"" + entity1 + "\"})- [rel] - (n2) RETURN n1,rel,n2").data()
        return answer

    # 关系查询：实体2
    def findRelationByEntity2(self, entity2):
        # 基于论文标题查询
        answer = self.graph.run(
            "MATCH (n1)<- [rel] - (n2:Paper {paperTitle:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        if (len(answer) == 0):
            # 基于论文作者查询
            answer = self.graph.run(
                "MATCH (n1) - [rel] - (n2:Author {authorName:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        return answer

    # 关系查询：实体1+关系
    def findOtherEntities(self, entity, relation):
        answer = self.graph.run(
            "MATCH (n1:Paper {paperTitle:\"" + entity + "\"})- [rel:Citation {type:\"" + relation + "\"}] -> (n2) RETURN n1,rel,n2").data()
        return answer

    # 关系查询：关系+实体2
    def findOtherEntities2(self, entity, relation):
        print("findOtherEntities2==")
        print(entity, relation)
        answer = self.graph.run(
            "MATCH (n1)- [rel:Citation {type:\"" + relation + "\"}] -> (n2:Paper {paperTitle:\"" + entity + "\"}) RETURN n1,rel,n2").data()
        # if (len(answer) == 0):
        #     answer = self.graph.run(
        #         "MATCH (n1)- [rel:Author_Paper {type:\"" + relation + "\"}] -> (n2:Author {authorName:\"" + entity + "\"}) RETURN n1,rel,n2").data()
        return answer

    # 关系查询：实体1+实体2(注意Entity2的空格）
    def findRelationByEntities(self, entity1, entity2):
        # 标题 + 标题
        answer = self.graph.run(
            "MATCH (n1:Paper {paperTitle:\"" + entity1 + "\"})- [rel] -> (n2:Paper{paperTitle:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        if (len(answer) == 0):
            # 作者 + 标题
            print(
                "MATCH (n1:Author {authorName:\"" + entity1 + "\"})- [rel] -> (n2:Paper{paperTitle:\"" + entity2 + "\"}) RETURN n1,rel,n2")
            answer = self.graph.run(
                "MATCH (n1:Author {authorName:\"" + entity1 + "\"})- [rel] -> (n2:Paper{paperTitle:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        # if (len(answer) == 0):
        #     # 系列 + 品牌
        #     answer = self.graph.run(
        #         "MATCH (n1:Series {name:\"" + entity1 + "\"})- [rel] -> (n2:Bank{name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        # if (len(answer) == 0):
        #     # 系列 + 系列
        #     answer = self.graph.run(
        #         "MATCH (n1:Series {name:\"" + entity1 + "\"})- [rel] -> (n2:Series{name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        #
        return answer

    # 查询数据库中是否有对应的实体-关系匹配
    def findEntityRelation(self, entity1, relation, entity2):
        answer = self.graph.run(
            "MATCH (n1:Paper {paperTitle:\"" + entity1 + "\"})- [rel:Citation {type:\"" + relation + "\"}] -> (n2:Paper{paperTitle:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        if (len(answer) == 0):
            answer = self.graph.run(
                "MATCH (n1:Author {authorName:\"" + entity1 + "\"})- [rel:Author_Paper {type:\"" + relation + "\"}] -> (n2:Paper{paperTitle:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        # if (len(answer) == 0):
        #     answer = self.graph.run(
        #         "MATCH (n1:Series {name:\"" + entity1 + "\"})- [rel:subbank {type:\"" + relation + "\"}] -> (n2:Bank{name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        # if (len(answer) == 0):
        #     answer = self.graph.run(
        #         "MATCH (n1:Series {name:\"" + entity1 + "\"})- [rel:subbank {type:\"" + relation + "\"}] -> (n2:Series{name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        return answer
