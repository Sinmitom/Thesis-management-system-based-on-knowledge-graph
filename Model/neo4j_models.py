from py2neo import Graph, Node, Relationship, NodeMatcher, cypher, Path


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
        elif select == 'authorName' or select == 2:  # 若实体1类型为作者
            answer = self.graph.run(
                "match (entity1:Author) -[rel]-> (entity2) where entity1.Name = \"" + value + "\" return entity1, rel,entity2").data()
        else:  # 若为其他情况
            answer = self.graph.run(
                "MATCH (entity1) - [rel] -> (entity2)  WHERE entity1.Name = \"" + value + "\" RETURN entity1,rel,entity2").data()
            # answer = self.graph.run("match (entity1:Paper) -[rel]-> (entity2) where entity1.Name = \"" + value+ "\" return entity1, rel,entity2").data()

        return answer

    # 关系查询:实体1
    def findRelationByEntity1(self, entity1):
        #  查找论文及其对应关系
        answer = self.graph.run(
            "MATCH (n1:Paper {Name:\"" + entity1 + "\"})- [rel] -> (n2) RETURN n1,rel,n2").data()
        # print(answer)
        # 基于论文作者查询，注意此处额外的空格

        if len(answer) == 0:  # 若输入的不是论文标题，则查找作者及其对应关系
            answer = self.graph.run(
                "MATCH (n1:Author {Name:\"" + entity1 + "\"})- [rel] - (n2) RETURN n1,rel,n2").data()
        return answer

    # 关系查询：实体2
    def findRelationByEntity2(self, entity2):
        # 查询论文
        answer = self.graph.run(
            "MATCH (n1)- [rel] -> (n2:Paper {Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        if len(answer) == 0:  # 若输入的不是，则查找作者单位及其对应关系
            answer = self.graph.run(
                "MATCH (n1) - [rel] -> (n2:Affiliation {Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        if len(answer) == 0:  # 若输入的不是，则查找论文出版单位及其对应关系
            answer = self.graph.run(
                "MATCH (n1) - [rel] -> (n2:Venue{Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        if len(answer) == 0:  # 若输入的不是论文标题，则查找作者感兴趣领域
            answer = self.graph.run(
                "MATCH (n1) - [rel] -> (n2:Concept {Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        return answer

    # 关系查询：实体1+关系
    def findOtherEntities(self, entity, relation):
        if relation == 'refer':
            answer = self.graph.run(
                "MATCH (n1:Paper {Name:\"" + entity + "\"})- [rel:Citation {type:\"" + relation +
                "\"}] -> (n2) RETURN n1,rel,n2").data()
        elif relation == 'own':
            answer = self.graph.run(
                "MATCH (n1:Author {Name:\"" + entity + "\"})- [rel:AuthorPaper {type:\"" + relation +
                "\"}] -> (n2) RETURN n1,rel,n2").data()
        elif relation == 'belong':
            answer = self.graph.run(
                "MATCH (n1:Author {Name:\"" + entity + "\"})- [rel:AuthorAffiliation {type:\"" + relation +
                "\"}] -> (n2) RETURN n1,rel,n2").data()
            if len(answer) == 0:
                answer = self.graph.run(
                    "MATCH (n1:Paper {Name:\"" + entity + "\"})- [rel:PaperVenue {type:\"" + relation +
                    "\"}] -> (n2) RETURN n1,rel,n2").data()
        elif relation == 'interest':
            answer = self.graph.run(
                "MATCH (n1:Author {Name:\"" + entity + "\"})- [rel:AuthorConcept{type:\"" + relation +
                "\"}] -> (n2) RETURN n1,rel,n2").data()
        else:
            answer = self.graph.run("MATCH (n1 {Name:\"" + entity + "\"})- [rel {type:\"" + relation +
                                    "\"}] -> (n2) RETURN n1, rel, n2").data()
        return answer

    # 关系查询：关系+实体2
    def findOtherEntities2(self, entity2, relation):
        print("findOtherEntities2==")
        # print(entity, relation)
        if relation == 'refer':
            answer = self.graph.run(
                "MATCH (n1)- [rel:Citation {type:\"" + relation + "\"}] -> (n2:Paper {Name:\"" + entity2 +
                "\"}) RETURN n1,rel,n2").data()
        elif relation == 'own':
            answer = self.graph.run(
                "MATCH (n1)- [rel:AuthorPaper {type:\"" + relation + "\"}] -> (n2:Paper {Name:\"" + entity2 +
                "\"}) RETURN n1,rel,n2").data()
        elif relation == 'belong':
            answer = self.graph.run(
                "MATCH (n1)- [rel:AuthorAffiliation {type:\"" + relation + "\"}] -> (n2:Affiliation {Name:\"" + entity2
                + "\"}) RETURN n1,rel,n2").data()
            if len(answer) == 0:
                answer = self.graph.run(
                    "MATCH (n1)- [rel:PaperVenue {type:\"" + relation + "\"}] -> (n2:Venue {Name:\"" + entity2 +
                    "\"}) RETURN n1,rel,n2").data()

        elif relation == 'interest':
            answer = self.graph.run(
                "MATCH (n1)- [rel:AuthorConcept {type:\"" + relation + "\"}] -> (n2:Concept {Name:\"" + entity2
                + "\"}) RETURN n1,rel,n2").data()
        else:
            answer = self.graph.run("MATCH (n1)- [rel {type:\"" + relation + "\"}] -> (n2 {Name:\"" + entity2
                                    + "\"}) RETURN n1,rel,n2").data()
        return answer

    # 关系查询：查询实体1和实体2它们之间的最短路径
    def findRelationByEntities(self, entity1, entity2):
        # 论文-论文
        answer = self.graph.run("MATCH (n1:Paper {Name:\"" + entity1 + "\"}),(n2:Paper{Name:\"" +
                                entity2 + "\"}), p=shortestpath((n1)-[rel*..10]-(n2)) RETURN p").evaluate()
        # 论文-作者
        if answer is None:
            answer = self.graph.run("MATCH (n1:Paper {Name:\"" + entity1 + "\"}),(n2:Author{Name:\"" +
                                    entity2 + "\"}),p=shortestpath((n1)-[rel*..10]-(n2)) RETURN p").evaluate()
        # 论文-作者单位
        if answer is None:
            answer = self.graph.run("MATCH (n1:Paper {Name:\"" + entity1 + "\"}),(n2:Affiliation{Name:\"" +
                                    entity2 + "\"}),p=shortestpath((n1)-[rel*..10]-(n2)) RETURN p").evaluate()
        # 论文-论文单位
        if answer is None:
            answer = self.graph.run("MATCH (n1:Paper {Name:\"" + entity1 + "\"}),(n2:Venue{Name:\"" +
                                    entity2 + "\"}),p=shortestpath((n1)-[rel*..10]-(n2)) RETURN p").evaluate()
        # 论文-研究领域
        if answer is None:
            answer = self.graph.run("MATCH (n1:Paper {Name:\"" + entity1 + "\"}),(n2:Concept{Name:\"" +
                                    entity2 + "\"}),p=shortestpath((n1)-[rel*..10]-(n2)) RETURN p").evaluate()

        # 作者-论文
        if answer is None:
            answer = self.graph.run("MATCH (n1:Author {Name:\"" + entity1 + "\"}),(n2:Paper{Name:\"" +
                                    entity2 + "\"}), p=shortestpath((n1)-[rel*..10]-(n2)) RETURN p").evaluate()
        # 作者-作者
        if answer is None:
            answer = self.graph.run("MATCH (n1:Author {Name:\"" + entity1 + "\"}),(n2:Author{Name:\"" +
                                    entity2 + "\"}),p=shortestpath((n1)-[rel*..10]-(n2)) RETURN rel").evaluate()
        # 作者-作者单位
        if answer is None:
            answer = self.graph.run("MATCH (n1:Author {Name:\"" + entity1 + "\"}),(n2:Affiliation{Name:\"" +
                                    entity2 + "\"}),p=shortestpath((n1)-[rel*..10]-(n2)) RETURN p").evaluate()
        # 作者-论文单位
        if answer is None:
            answer = self.graph.run("MATCH (n1:Author {Name:\"" + entity1 + "\"}),(n2:Venue{Name:\"" +
                                    entity2 + "\"}),p=shortestpath((n1)-[rel*..10]-(n2)) RETURN p").evaluate()
        # 作者-研究领域
        if answer is None:
            answer = self.graph.run("MATCH (n1:Author {Name:\"" + entity1 + "\"}),(n2:Concept{Name:\"" +
                                    entity2 + "\"}),p=shortestpath((n1)-[rel*..10]-(n2)) RETURN p").evaluate()

        relationDict = []
        if answer is not None:
            print(answer)
            for x in answer:
                print(x)
                tmp = {}
                start_node = x.start_node
                end_node = x.end_node
                tmp['n1'] = start_node
                tmp['n2'] = end_node
                tmp['rel'] = x
                relationDict.append(tmp)
        print(relationDict)
        return relationDict

    # 查询数据库中是否有对应的实体-关系匹配
    def findEntityRelation(self, entity1, relation, entity2):
        answer = self.graph.run("MATCH (n1:Paper {Name:\"" + entity1 + "\"})- [rel:Citation {type:\"" + relation +
                                "\"}] -> (n2:Paper{Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        if answer is None:
            answer = self.graph.run("MATCH (n1:Paper {Name:\"" + entity1 + "\"})- [rel:PaperVenue {type:\"" + relation +
                                    "\"}] -> (n2:Venue{Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()

        if answer is None:
            answer = self.graph.run(
                "MATCH (n1:Author {Name:\"" + entity1 + "\"})- [rel:AuthorPaper {type:\"" + relation +
                "\"}] -> (n2:Paper{Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()

        if answer is None:
            answer = self.graph.run(
                "MATCH (n1:Author {Name:\"" + entity1 + "\"})- [rel:AuthorAffiliation {type:\"" + relation +
                "\"}] -> (n2:Affiliation{Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()

        if answer is None:
            answer = self.graph.run(
                "MATCH (n1:Author {Name:\"" + entity1 + "\"})- [rel:AuthorVenue {type:\"" + relation +
                "\"}] -> (n2:Venue{Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()

        return answer

        # 添加实体

    def addEntity(self, entityId, entityName, entityInfo, select):
        # 查询实体：考虑实体1类型，查找和实体1类型相关的所有实体以及关系
        print("测试添加实体")
        answer = []
        if select == 'Paper' or select == '1':  # 若添加实体1类型为论文
            # 先查看是否已经添加过此实体
            answer = self.graph.run(
                "match (entity:Paper) where entity.Name = \"" + entityName + "\" and entity.Id = \"" +
                entityId + "\"return entity").data()
            if len(answer) != 0:  # 若已经有此实体
                return answer
            else:
                answer = self.graph.run(
                    "merge(entity:Paper{Name : \"" + entityName + "\", Id : \"" +
                    entityId + "\" , Abstract : \"" + entityInfo + "\"}) return entity").data()
        elif select == 'Author' or select == '2':  # 若添加实体类型为作者
            answer = self.graph.run(
                "match (entity:Author) where entity.Name = \"" + entityName + "\" and entity.Id = \"" +
                entityId + "\"return entity").data()
            if len(answer) != 0:  # 若已经有此实体
                return answer
            else:  # 添加作者信息
                answer = self.graph.run(
                    "merge(entity:Author{Name : \"" + entityName + "\", Id : \"" +
                    entityId + "\"}) return entity").data()

        elif select == 'Affiliation' or select == '3':  # 若添加实体类型为作者单位
            answer = self.graph.run(
                "match (entity:Affiliation) where entity.Name = \"" + entityName + "\" and entity.Id = \"" +
                entityId + "\"return entity").data()
            if len(answer) != 0:  # 若已经有此实体
                return answer
            else:  # 添加作者信息
                answer = self.graph.run(
                    "merge(entity:Affiliation{Name : \"" + entityName + "\", Id : \"" +
                    entityId + "\"}) return entity").data()

        elif select == 'Venue' or select == '4':  # 若添加实体类型为论文机构
            answer = self.graph.run(
                "match (entity:Venue) where entity.Name = \"" + entityName + "\" and entity.Id = \"" +
                entityId + "\"return entity").data()
            if len(answer) != 0:  # 若已经有此实体
                return answer
            else:  # 添加作者信息
                answer = self.graph.run(
                    "merge(entity:Venue{Name : \"" + entityName + "\", Id : \"" +
                    entityId + "\"}) return entity").data()
        elif select == 'Concept' or select == '5':  # 若添加实体类型为感兴趣领域
            answer = self.graph.run(
                "match (entity:Concept) where entity.Name = \"" + entityName + "\" and entity.Id = \"" +
                entityId + "\"return entity").data()
            if len(answer) != 0:  # 若已经有此实体
                return answer
            else:  # 添加作者信息
                answer = self.graph.run(
                    "merge(entity:Concept{Name : \"" + entityName + "\", Id : \"" +
                    entityId + "\"}) return entity").data()

        return answer
