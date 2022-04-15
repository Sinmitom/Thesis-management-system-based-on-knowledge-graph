from py2neo import Graph, Node, Relationship, NodeMatcher


class Neo4j_Handle():
    graph = None

    # matcher = None
    def __init__(self):
        print("Neo4j Init ...")


    def connectDB(self):
        self.graph = Graph('bolt://localhost:7687', user='neo4j', password='password')

    # self.matcher = NodeMatcher(self.graph)

    # 实体查询，用于命名实体识别：品牌+车系+车型
    def matchEntityItem(self, value):
        answer = self.graph.run("MATCH (entity1) WHERE entity1.name = \"" + value + "\" RETURN entity1").data()
        print(answer)
        return answer

    # 实体查询
    def getEntityRelationbyEntity(self, value):
        # 查询实体：不考虑实体类型，只考虑关系方向
        print("测试调用实体查询")
        answer = self.graph.run("MATCH (entity1) - [rel] -> (entity2) WHERE entity1.paperTitle Contains \"" + value + "\" RETURN entity1, rel, entity2").data()
        #answer = self.graph.run("MATCH (entity1) - [rel] -> (entity2)  WHERE entity1.paperTitle = \"" + value + "\" RETURN entity1, rel,entity2").data()
        #answer = self.graph.run("MATCH (entity1) - [rel] -> (entity2)  WHERE entity1.paperTitle = ~"+ "\".*" + value + ".*\" RETURN entity1,rel,entity2").data()
        # 基于模糊查询  ~ ".*content.*"
        # 模糊查询2 where n.attribute Contains "content"
        # if (len(answer) == 0):
        #     # 查询实体：不考虑关系方向
        #     answer = self.graph.run("MATCH (entity1) - [rel] - (entity2)  WHERE entity2.paperTitle = \"" + value + "\" RETURN entity1, rel, entity2").data()
        return answer

    # 关系查询:实体1
    def findRelationByEntity1(self, entity1):
        # 基于论文标题查询
        answer = self.graph.run("MATCH (n1:Paper {paperTitle:\"" + entity1 + "\"})- [rel] -> (n2) RETURN n1,rel,n2").data()
        #print(answer)
        # 基于论文作者查询，注意此处额外的空格
        if (len(answer) == 0):
            answer = self.graph.run("MATCH (n1:Author {authorName:\"" + entity1 + "\"})- [rel] - (n2) RETURN n1,rel,n2").data()
        return answer

    # 关系查询：实体2
    def findRelationByEntity2(self, entity2):
        # 基于论文标题查询
        answer = self.graph.run("MATCH (n1)<- [rel] - (n2:Paper {paperTitle:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
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
