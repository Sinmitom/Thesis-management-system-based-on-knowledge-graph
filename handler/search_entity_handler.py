from toolkit.pre_load import neo4jconn
import os
import json

relationCountDict = {}
filePath = os.path.abspath(os.path.join(os.getcwd(), "."))

with open(filePath + "/toolkit/relationStaticResult.txt", "r") as fr:
    for line in fr:
        relationNameCount = line.split(",")
        relationName = relationNameCount[0][2:-1]
        relationCount = relationNameCount[1][1:-2]
        relationCountDict[relationName] = int(relationCount)


# 实体查询
def search_entity(entity, select):
    # 根据传入的实体名称搜索出关系
    # 连接数据库
    db = neo4jconn
    print('测试实体查询')
    # print(entity)
    # print(type(select))
    entity = entity.strip()
    entityRelation = db.getEntityRelationbyEntity(entity, select)
    # print(entityRelation)
    if len(entityRelation) == 0:
        # 若数据库中无法找到该实体，则返回数据库中无该实体
        return {'ctx': '', 'entityRelation': ''}
    else:
        # 返回查询结果
        return {'ctx': json.dumps(entity, ensure_ascii=False),
                'entityRelation': json.dumps(entityRelation, ensure_ascii=False)}




