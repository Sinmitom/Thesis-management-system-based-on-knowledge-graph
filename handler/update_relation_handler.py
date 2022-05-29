import os
import json
from toolkit.pre_load import neo4jconn


def update_relation(entity1, relation, entity2):  # 更新实体关系

    db = neo4jconn  # 连接图数据库
    entity1 = entity1.strip()
    entity2 = entity2.strip()
    print("更新实体关系测试：****", entity1, entity2)
    if len(entity1) != 0 and relation == 'refer' and len(entity2) != 0:  # 若添加的关系是论文引用关系
        searchResult = db.updateRelation1(entity1, relation, entity2)
        print('论文引用测试：', searchResult)
        if len(searchResult) > 0:
            return {'ctx': '', 'searchResult': json.dumps(searchResult, ensure_ascii=False)}
    elif len(entity1) != 0 and relation == 'own' and len(entity2) != 0:  # 若添加的关系是作者-论文关系

        searchResult = db.updateRelation2(entity1, relation, entity2)
        print('作者-论文测试：', searchResult)
        if len(searchResult) > 0:
            return {'ctx': '', 'searchResult': json.dumps(searchResult, ensure_ascii=False)}

    elif len(entity1) != 0 and relation == 'belong' and len(entity2) != 0:  # 若添加的关系是作者-机构or论文-单位关系

        searchResult = db.updateRelation3(entity1, relation, entity2)
        print('作者-机构测试or论文-单位测试：', searchResult)
        if len(searchResult) > 0:
            return {'ctx': '', 'searchResult': json.dumps(searchResult, ensure_ascii=False)}

    elif len(entity1) != 0 and relation == 'interest' and len(entity2) != 0:  # 若添加的关系是作者-感兴趣领域关系

        searchResult = db.updateRelation4(entity1, relation, entity2)
        print('作者-领域：', searchResult)
        if len(searchResult) > 0:
            return {'ctx': '', 'searchResult': json.dumps(searchResult, ensure_ascii=False)}

        # 若输入全为空值 or entity1 or entity2有一个为空值，则返回报错
    elif len(entity1) == 0 or len(entity2) == 0 or relation == '无限制':
        return {'ctx': 'padding', 'searchResult': ''}  # 返回空值

    else:
        return {'ctx': 'padding', 'searchResult': ''}  # 返回空值

    return {'ctx': 'padding', 'searchResult': ''}  # 返回空值


def delete_relation(entity1, relation, entity2):  # 删除实体关系

    db = neo4jconn  # 连接图数据库
    entity1 = entity1.strip()
    entity2 = entity2.strip()
    print("删除实体关系测试：****", entity1, entity2)
    if len(entity1) != 0 and relation == 'refer' and len(entity2) != 0:  # 若删除的关系是论文引用关系
        searchResult = db.deleteRelation1(entity1, relation, entity2)
        print('论文引用测试：', searchResult)
        if len(searchResult) > 0:
            return {'ctx': '', 'searchResult': json.dumps(searchResult, ensure_ascii=False)}
    elif len(entity1) != 0 and relation == 'own' and len(entity2) != 0:  # 若删除的关系是作者-论文关系

        searchResult = db.deleteRelation2(entity1, relation, entity2)
        print('作者-论文测试：', searchResult)
        if len(searchResult) > 0:
            return {'ctx': '', 'searchResult': json.dumps(searchResult, ensure_ascii=False)}

    elif len(entity1) != 0 and relation == 'belong' and len(entity2) != 0:  # 若删除的关系是作者-机构or论文-单位关系

        searchResult = db.deleteRelation3(entity1, relation, entity2)
        print('作者-机构测试or论文-单位测试：', searchResult)
        if len(searchResult) > 0:
            return {'ctx': '', 'searchResult': json.dumps(searchResult, ensure_ascii=False)}

    elif len(entity1) != 0 and relation == 'interest' and len(entity2) != 0:  # 若删除的关系是作者-感兴趣领域关系
        searchResult = db.deleteRelation4(entity1, relation, entity2)
        print('作者-领域：', searchResult)
        if len(searchResult) > 0:
            return {'ctx': '', 'searchResult': json.dumps(searchResult, ensure_ascii=False)}

        # 若输入全为空值 or entity1 or entity2有一个为空值，则返回报错
    elif len(entity1) == 0 or len(entity2) == 0 or relation == '无限制':
        return {'ctx': 'padding', 'searchResult': ''}  # 返回空值

    else:
        return {'ctx': 'padding', 'searchResult': ''}  # 返回空值

    return {'ctx': 'padding', 'searchResult': ''}  # 返回空值
