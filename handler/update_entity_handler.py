from toolkit.pre_load import neo4jconn
import os
import json

relationCountDict = {}
filePath = os.path.abspath(os.path.join(os.getcwd(), "."))


# 添加实体
def add_entity(entityId, entityName, select, entityInfo=None):
    # 根据传入的参数添加实体
    # 连接数据库
    db = neo4jconn
    print('测试添加实体')
    print(entityName)
    entityId = entityId.strip()
    entityName = entityName.strip()
    if select == 1:
        entityInfo = entityInfo.strip()
    # 添加实体
    entityRelation = db.addEntity(entityId, entityName, entityInfo, select)
    # print(entityRelation)
    if len(entityRelation) == 0:
        # 若数据库中无法找到该实体，则返回数据库中无该实体
        return {'ctx': '', 'entityRelation': ''}
    else:
        # 返回查询结果
        return {'ctx': json.dumps(entityName, ensure_ascii=False),
                'entityRelation': json.dumps(entityRelation, ensure_ascii=False)}


# 添加实体
def delete_entity(entityId, entityName, select, entityInfo=None):
    # 根据传入的参数添加实体
    # 连接数据库
    db = neo4jconn
    print('测试删除实体')
    print(entityName)
    entityId = entityId.strip()
    entityName = entityName.strip()
    # entityInfo = entityInfo.strip()
    # 添加实体
    entityRelation = db.deleteEntity(entityId, entityName, entityInfo, select)
    # print(entityRelation)
    if len(entityRelation) == 0:
        # 若数据库中无法找到该实体，则返回数据库中无该实体
        return {'ctx': '', 'entityRelation': ''}
    else:
        # 返回删除结果
        return {'ctx': json.dumps(entityName, ensure_ascii=False),
                'entityRelation': json.dumps(entityRelation, ensure_ascii=False)}