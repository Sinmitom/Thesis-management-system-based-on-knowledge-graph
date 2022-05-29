from py2neo import Graph, Node, Relationship, NodeMatcher, cypher, Path


class Neo4j_Handle():
    graph = None
    flag = -1

    # matcher = None
    def __init__(self):
        self.flag = -1
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
                "match (entity1:Paper) -[rel]-> (entity2) where entity1.Name = \"" + value + "\" return entity1, rel,"
                                                                                             "entity2").data()
            # if len(answer) == 0:   # 查询失败,没有关系连接时
            #     print("调用了吗")
            #     answer = self.graph.run(
            #         "match (entity1:Paper) where entity1.Name = \"" + value + "\" return entity1").data()

        elif select == 'authorName' or select == 2:  # 若实体1类型为作者
            answer = self.graph.run(
                "match (entity1:Author) -[rel]-> (entity2) where entity1.Name = \"" + value + "\" return entity1, "
                                                                                              "rel,entity2").data()
            # if answer is None:
            #     answer = self.graph.run(
            #         "match (entity1:Author) where entity1.Name = \"" + value + "\" return entity1").data()
        else:  # 若为其他情况
            answer = self.graph.run(
                "MATCH (entity1) - [rel] -> (entity2)  WHERE entity2.Name = \"" + value + "\" RETURN entity1,rel,"
                                                                                          "entity2").data()
            # answer = self.graph.run("match (entity1:Paper) -[rel]-> (entity2) where entity1.Name = \"" + value+ "\" return entity1, rel,entity2").data()

        print('*' * 50, answer, value, select)
        return answer

    # 关系查询:实体1
    def findRelationByEntity1(self, entity1):
        #  查找论文及其对应关系
        answer = self.graph.run(
            "MATCH (n1:Paper {Name:\"" + entity1 + "\"})- [rel] -> (n2) RETURN n1,rel,n2").data()
        flag = 0
        # print(answer)
        # 基于论文作者查询，注意此处额外的空格

        if len(answer) == 0:  # 若输入的不是论文标题，则查找作者及其对应关系
            answer = self.graph.run(
                "MATCH (n1:Author {Name:\"" + entity1 + "\"})- [rel] - (n2) RETURN n1,rel,n2").data()
            flag = 1
        return answer, flag

    # 关系查询：实体2
    def findRelationByEntity2(self, entity2):
        # 查询论文
        answer = self.graph.run(
            "MATCH (n1)- [rel] -> (n2:Paper {Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()

        flag = -1
        if len(answer) == 0:  # 若输入的不是，则查找作者单位及其对应关系
            answer = self.graph.run(
                "MATCH (n1) - [rel] -> (n2:Affiliation {Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
            flag = 1

        if len(answer) == 0:  # 若输入的不是，则查找论文出版单位及其对应关系
            answer = self.graph.run(
                "MATCH (n1) - [rel] -> (n2:Venue{Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
            flag = 0
        if len(answer) == 0:  # 若输入的不是论文标题，则查找作者感兴趣领域
            answer = self.graph.run(
                "MATCH (n1) - [rel] -> (n2:Concept {Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
            flag = 1

        return answer, flag

    # 关系查询：实体1+关系
    def findOtherEntities(self, entity, relation):
        if relation == 'refer':
            answer = self.graph.run(
                "MATCH (n1:Paper {Name:\"" + entity + "\"})- [rel:Citation {type:\"" + relation +
                "\"}] -> (n2) RETURN n1,rel,n2").data()
            flag = 0

        elif relation == 'own':
            answer = self.graph.run(
                "MATCH (n1:Author {Name:\"" + entity + "\"})- [rel:AuthorPaper {type:\"" + relation +
                "\"}] -> (n2) RETURN n1,rel,n2").data()
            flag = 1
        elif relation == 'belong':
            answer = self.graph.run(
                "MATCH (n1:Author {Name:\"" + entity + "\"})- [rel:AuthorAffiliation {type:\"" + relation +
                "\"}] -> (n2) RETURN n1,rel,n2").data()
            flag = 1
            if len(answer) == 0:
                answer = self.graph.run(
                    "MATCH (n1:Paper {Name:\"" + entity + "\"})- [rel:PaperVenue {type:\"" + relation +
                    "\"}] -> (n2) RETURN n1,rel,n2").data()
                flag = 0
        elif relation == 'interest':
            answer = self.graph.run(
                "MATCH (n1:Author {Name:\"" + entity + "\"})- [rel:AuthorConcept{type:\"" + relation +
                "\"}] -> (n2) RETURN n1,rel,n2").data()
            flag = 1
        else:
            answer = self.graph.run("MATCH (n1 {Name:\"" + entity + "\"})- [rel {type:\"" + relation +
                                    "\"}] -> (n2) RETURN n1, rel, n2").data()
            flag = -1
        return answer, flag

    # 关系查询：关系+实体2
    def findOtherEntities2(self, entity2, relation):
        print("findOtherEntities2==")
        # print(entity, relation)
        if relation == 'refer':
            answer = self.graph.run(
                "MATCH (n1)- [rel:Citation {type:\"" + relation + "\"}] -> (n2:Paper {Name:\"" + entity2 +
                "\"}) RETURN n1,rel,n2").data()
            flag = 0
        elif relation == 'own':
            answer = self.graph.run(
                "MATCH (n1)- [rel:AuthorPaper {type:\"" + relation + "\"}] -> (n2:Paper {Name:\"" + entity2 +
                "\"}) RETURN n1,rel,n2").data()
            flag = 1
        elif relation == 'belong':
            answer = self.graph.run(
                "MATCH (n1)- [rel:AuthorAffiliation {type:\"" + relation + "\"}] -> (n2:Affiliation {Name:\"" + entity2
                + "\"}) RETURN n1,rel,n2").data()
            flag = 1
            if len(answer) == 0:
                answer = self.graph.run(
                    "MATCH (n1)- [rel:PaperVenue {type:\"" + relation + "\"}] -> (n2:Venue {Name:\"" + entity2 +
                    "\"}) RETURN n1,rel,n2").data()
                flag = 0

        elif relation == 'interest':
            answer = self.graph.run(
                "MATCH (n1)- [rel:AuthorConcept {type:\"" + relation + "\"}] -> (n2:Concept {Name:\"" + entity2
                + "\"}) RETURN n1,rel,n2").data()
            flag = 1
        else:
            answer = self.graph.run("MATCH (n1)- [rel {type:\"" + relation + "\"}] -> (n2 {Name:\"" + entity2
                                    + "\"}) RETURN n1,rel,n2").data()
            flag = -1
        return answer, flag

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
        print('*test'*100, answer)
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
        return relationDict, self.flag

    # 查询数据库中是否有对应的实体-关系匹配
    def findEntityRelation(self, entity1, relation, entity2):
        answer = self.graph.run("MATCH (n1:Paper {Name:\"" + entity1 + "\"})- [rel:Citation {type:\"" + relation +
                                "\"}] -> (n2:Paper{Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()

        if len(answer) == 0:
            answer = self.graph.run("MATCH (n1:Paper {Name:\"" + entity1 + "\"})- [rel:PaperVenue {type:\"" + relation +
                                    "\"}] -> (n2:Venue{Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()

        if len(answer) == 0:
            print('test')
            answer = self.graph.run(
                "MATCH (n1:Author {Name:\"" + entity1 + "\"})- [rel:AuthorPaper {type:\"" + relation +
                "\"}] -> (n2:Paper{Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()

        if len(answer) == 0:
            answer = self.graph.run(
                "MATCH (n1:Author {Name:\"" + entity1 + "\"})- [rel:AuthorAffiliation {type:\"" + relation +
                "\"}] -> (n2:Affiliation{Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()

        if len(answer) == 0:
            answer = self.graph.run(
                "MATCH (n1:Author {Name:\"" + entity1 + "\"})- [rel:AuthorVenue {type:\"" + relation +
                "\"}] -> (n2:Venue{Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()

        return answer, self.flag

        # 添加实体

    def addEntity(self, entityId, entityName, entityInfo, select):
        # 查询实体：考虑实体1类型，查找和实体1类型相关的所有实体以及关系
        print("测试添加实体")
        answer = []
        if select == 'Paper' or select == 1:  # 若添加实体1类型为论文
            # 先查看是否已经添加过此实体
            answer = self.graph.run(
                "match (entity:Paper) where entity.Name = \"" + entityName + "\" and entity.Id = \"" +
                entityId + "\"return entity").data()
            if len(answer) != 0:  # 若已经有此实体
                return answer
            else:
                answer = self.graph.run(
                    "merge(entity:Paper{Name : \"" + entityName + "\", Id : \"" +
                    entityId + "\" , Year : \"" + entityInfo + "\"}) return entity").data()
        elif select == 'Author' or select == 2:  # 若添加实体类型为作者
            answer = self.graph.run(
                "match (entity:Author) where entity.Name = \"" + entityName + "\" and entity.Id = \"" +
                entityId + "\"return entity").data()
            if len(answer) != 0:  # 若已经有此实体
                return answer
            else:  # 添加作者信息
                answer = self.graph.run(
                    "merge(entity:Author{Name : \"" + entityName + "\", Id : \"" +
                    entityId + "\"}) return entity").data()

        elif select == 'Affiliation' or select == 3:  # 若添加实体类型为作者单位
            answer = self.graph.run(
                "match (entity:Affiliation) where entity.Name = \"" + entityName + "\" and entity.Id = \"" +
                entityId + "\"return entity").data()
            if len(answer) != 0:  # 若已经有此实体
                return answer
            else:  # 添加作者信息
                answer = self.graph.run(
                    "merge(entity:Affiliation{Name : \"" + entityName + "\", Id : \"" +
                    entityId + "\"}) return entity").data()

        elif select == 'Venue' or select == 4:  # 若添加实体类型为论文机构
            answer = self.graph.run(
                "match (entity:Venue) where entity.Name = \"" + entityName + "\" and entity.Id = \"" +
                entityId + "\"return entity").data()
            if len(answer) != 0:  # 若已经有此实体
                return answer
            else:  # 添加作者信息
                answer = self.graph.run(
                    "merge(entity:Venue{Name : \"" + entityName + "\", Id : \"" +
                    entityId + "\"}) return entity").data()
        elif select == 'Concept' or select == 5:  # 若添加实体类型为感兴趣领域
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

    def deleteEntity(self, entityId, entityName, entityInfo, select):
        # 删除实体
        print("测试删除实体")
        answer = []
        if select == 'Paper' or select == 1:  # 若删除实体1类型为论文
            # 先查看是否已经添加过此实体
            answer = self.graph.run(
                "match (entity:Paper) where entity.Name = \"" + entityName + "\" and entity.Id = \"" +
                entityId + "\"return entity").data()
            if len(answer) != 0:  # 若已经有此实体，开删,包括其关系！
                answer = self.graph.run(
                    "match (entity:Paper) where entity.Name = \"" + entityName + "\" or entity.Id = \"" +
                    entityId + "\"detach delete entity return entity").data()  # 返回的应该是[Node{'entity':}]

        elif select == 'Author' or select == 2:  # 若删除实体类型为作者
            answer = self.graph.run(
                "match (entity:Author) where entity.Name = \"" + entityName + "\" and entity.Id = \"" +
                entityId + "\"return entity").data()
            if len(answer) != 0:  # 若已经有此实体，开删,包括其关系！
                answer = self.graph.run(
                    "match (entity:Author) where entity.Name = \"" + entityName + "\" or entity.Id = \"" +
                    entityId + "\"detach delete entity return entity").data()  # 返回的应该是[Node{'entity':}]

        elif select == 'Affiliation' or select == 3:  # 若删除实体类型为作者所属机构单位
            answer = self.graph.run(
                "match (entity:Affiliation) where entity.Name = \"" + entityName + "\" and entity.Id = \"" +
                entityId + "\"return entity").data()
            if len(answer) != 0:  # 若有此实体，开删！
                answer = self.graph.run(
                    "match (entity:Affiliation) where entity.Name = \"" + entityName + "\" or entity.Id = \"" +
                    entityId + "\"detach delete entity return entity").data()  # 返回的应该是[Node{'entity':}]

        elif select == 'Venue' or select == 4:  # 若删除实体类型为论文收录期刊
            answer = self.graph.run(
                "match (entity:Venue) where entity.Name = \"" + entityName + "\" and entity.Id = \"" +
                entityId + "\"return entity").data()
            if len(answer) != 0:  # 若已经有此实体
                answer = self.graph.run(
                    "match (entity:Venue) where entity.Name = \"" + entityName + "\" or entity.Id = \"" +
                    entityId + "\"detach delete entity return entity").data()  # 返回的应该是[Node{'entity':}]

        elif select == 'Concept' or select == 5:  # 若添加实体类型为感兴趣领域
            answer = self.graph.run(
                "match (entity:Concept) where entity.Name = \"" + entityName + "\" and entity.Id = \"" +
                entityId + "\"return entity").data()
            if len(answer) != 0:  # 若已经有此实体
                answer = self.graph.run(
                    "match (entity:Concept) where entity.Name = \"" + entityName + "\" or entity.Id = \"" +
                    entityId + "\"detach delete entity return entity").data()  # 返回的应该是[Node{'entity':}]
        return answer

    def updateRelation1(self, entity1, relation, entity2):  # 添加论文引用关系
        answer = self.graph.run("MATCH (n1:Paper {Name:\"" + entity1 + "\"})- [rel:Citation {type:\"" + relation +
                                "\"}] -> (n2:Paper{Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()  # 查看是否已经有此关系
        print("究极测试", len(answer))
        if len(answer) == 0:  # 若关系不存在，则添加关系
            answer = self.graph.run("MATCH (n1:Paper{Name:\"" + entity1 + "\"}), (n2:Paper{Name:\"" + entity2 +
                                    "\"}) MERGE (n1)-[rel: Citation{type:\"" + relation + "\"}]->(n2) RETURN n1,rel,n2").data()  # 创建论文引用关系
        return answer  # 若关系存在，则返回此关系数据

    def deleteRelation1(self, entity1, relation, entity2):  # 删除论文引用关系
        answer = self.graph.run("MATCH (n1:Paper {Name:\"" + entity1 + "\"})- [rel:Citation {type:\"" + relation +
                                "\"}] -> (n2:Paper{Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()  # 查看是否已经有此关系
        print("究极测试", len(answer))
        if len(answer) != 0:  # 若关系存在，则删除关系
            answer = self.graph.run("MATCH (n1:Paper{Name:\"" + entity1 + "\"})-[rel: Citation{type:\"" + relation +
                                    "\"}]->(n2:Paper{Name:\"" + entity2 + "\"}) delete rel RETURN n1,rel,n2").data()  # 删除论文引用关系
        return answer  # 若关系不存在，则返回此关系数据

    def updateRelation2(self, entity1, relation, entity2):  # 添加作者-论文关系
        answer = self.graph.run("MATCH (n1:Author {Name:\"" + entity1 + "\"})- [rel:AuthorPaper {type:\"" + relation +
                                "\"}] -> (n2:Paper{Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()  # 查看是否已经有此关系
        print("究极测试", len(answer))
        if len(answer) == 0:  # 若关系不存在，则添加关系
            answer = self.graph.run("MATCH (n1:Author{Name:\"" + entity1 + "\"}), (n2:Paper{Name:\"" + entity2 +
                                    "\"}) MERGE (n1)-[rel: AuthorPaper{type:\"" + relation + "\"}]->(n2) RETURN n1,rel,n2").data()  # 创建论文引用关系
        return answer  # 若关系存在，则返回此关系数据

    def deleteRelation2(self, entity1, relation, entity2):  # 删除作者-论文关系
        answer = self.graph.run("MATCH (n1:Author {Name:\"" + entity1 + "\"})- [rel:AuthorPaper {type:\"" + relation +
                                "\"}] -> (n2:Paper{Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()  # 查看是否已经有此关系
        print("究极测试", len(answer))
        if len(answer) != 0:  # 若关系存在，则删除关系
            answer = self.graph.run("MATCH (n1:Author{Name:\"" + entity1 + "\"})-[rel: AuthorPaper{type:\"" + relation +
                                    "\"}]->(n2:Paper{Name:\"" + entity2 + "\"}) delete rel RETURN n1,rel,n2").data()  # 删除作者-论文关系
        return answer  # 若关系不存在，则返回此关系数据

    def updateRelation3(self, entity1, relation, entity2):  # 作者-机构关系 or论文-期刊关系
        answer = self.graph.run(
            "MATCH (n1:Author {Name:\"" + entity1 + "\"})- [rel:AuthorAffiliation {type:\"" + relation +
            "\"}] -> (n2:Affiliation{Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()  # 查看是否已经有作者-机构关系
        print("究极测试", len(answer))
        if len(answer) == 0:  # 若关系不存在，则接着查询论文-期刊关系
            answer = self.graph.run(
                "MATCH (n1:Paper {Name:\"" + entity1 + "\"})- [rel:PaperVenue {type:\"" + relation +
                "\"}] -> (n2:Venue{Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()  # 查看是否已经有此关系
            if len(answer) == 0:
                answer = self.graph.run(
                    "MATCH (n1:Author{Name:\"" + entity1 + "\"}), (n2:Affiliation{Name:\"" + entity2 +
                    "\"}) MERGE (n1)-[rel:AuthorAffiliation{type:\"" + relation + "\"}]->(n2) RETURN n1,rel,n2").data()  # 创建作者-机构引用关系
                if len(answer) == 0:
                    answer = self.graph.run(
                        "MATCH (n1:Paper{Name:\"" + entity1 + "\"}), (n2:Venue{Name:\"" + entity2 +
                        "\"}) MERGE (n1)-[rel:PaperVenue{type:\"" + relation + "\"}]->(n2) RETURN n1,rel,n2").data()  # 创建论文-期刊引用关系

        return answer  # 若关系不存在，则返回此关系数据

    def deleteRelation3(self, entity1, relation, entity2):  # 删除作者-机构关系 or论文-期刊关系
        answer = self.graph.run(
            "MATCH (n1:Author {Name:\"" + entity1 + "\"})- [rel:AuthorAffiliation {type:\"" + relation +
            "\"}] -> (n2:Affiliation{Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()  # 查看是否已经有作者-机构关系
        print("究极测试", len(answer))
        if len(answer) != 0:  # 若关系存在，则删除 查询作者-单位关系
            answer = self.graph.run(
                "MATCH (n1:Author {Name:\"" + entity1 + "\"})- [rel:AuthorAffiliation {type:\"" + relation +
                "\"}] -> (n2:Affiliation{Name:\"" + entity2 + "\"}) delete rel RETURN n1,rel,n2").data()  # 删除作者-单位关系
        else:  # 若关系不存在，则接着查询 论文-期刊关系
            answer = self.graph.run(
                "MATCH (n1:Paper {Name:\"" + entity1 + "\"})- [rel:PaperVenue {type:\"" + relation +
                "\"}] -> (n2:Venue {Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()  # 查看是否已经有论文-期刊关系
            if len(answer) != 0:  # 若关系存在，则删除 查询论文-期刊关系
                answer = self.graph.run(
                    "MATCH (n1:Paper {Name:\"" + entity1 + "\"})- [rel:PaperVenue {type:\"" + relation +
                    "\"}] -> (n2:Venue{Name:\"" + entity2 + "\"}) delete rel RETURN n1,rel,n2").data()  # 删除论文-期刊关系

        return answer  # 返回此关系数据

    def updateRelation4(self, entity1, relation, entity2):  # 作者-感兴趣领域关系
        answer = self.graph.run("MATCH (n1:Author {Name:\"" + entity1 + "\"})- [rel:AuthorPaper {type:\"" + relation +
                                "\"}] -> (n2:Concept{Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()  # 查看是否已经有此关系
        print("究极测试", len(answer))
        if len(answer) == 0:  # 若关系不存在，则添加关系
            answer = self.graph.run("MATCH (n1:Author{Name:\"" + entity1 + "\"}), (n2:Concept{Name:\"" + entity2 +
                                    "\"}) MERGE (n1)-[rel: AuthorConcept{type:\"" + relation + "\"}]->(n2) RETURN n1,rel,n2").data()  # 创建论文引用关系
        return answer  # 若关系存在，则返回此关系数据

    def deleteRelation4(self, entity1, relation, entity2):  # 删除作者-感兴趣领域关系
        answer = self.graph.run("MATCH (n1:Author {Name:\"" + entity1 + "\"})- [rel:AuthorConcept {type:\"" + relation +
                                "\"}] -> (n2:Concept{Name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()  # 查看是否已经有此关系
        print("究极测试", len(answer))
        if len(answer) != 0:  # 若关系存在，则删除关系
            answer = self.graph.run(
                "MATCH (n1:Author {Name:\"" + entity1 + "\"})- [rel:AuthorConcept {type:\"" + relation +
                "\"}] -> (n2:Concept{Name:\"" + entity2 + "\"}) delete rel RETURN n1,rel,n2").data()  # 删除作者-研究领域关系
        return answer  # 若关系存在，则返回此关系数据
