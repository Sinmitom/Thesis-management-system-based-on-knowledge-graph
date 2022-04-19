from py2neo import Graph, Node, Relationship, NodeMatcher
import json

graph = Graph('bolt://localhost:7687', user='neo4j', password='password')

entity1 = "Anon et al"
entity2 = "Cryptologia"
answer = graph.run("MATCH (n1:Author {Name:\"" + entity1 + "\"}),(n2:Venue{Name:\"" +
                   entity2 + "\"}),p=shortestpath((n1)-[rel*..10]-(n2)) RETURN p").evaluate()
print("原始answer")
print(answer)
relationDict = []
if answer is not None:
    for x in answer:
        print('x的值')
        print(x)
        tmp = {}
        start_node = x.start_node
        end_node = x.end_node
        tmp['n1'] = start_node
        tmp['n2'] = end_node
        tmp['rel'] = x
        relationDict.append(tmp)
    print('传出的值:')
    print(relationDict)

res = {'ctx': '', 'searchResult': json.dumps(relationDict, ensure_ascii=False)}
print('\n传出的第二步的值')
print(res)
searchResult = res['searchResult']
print("\nResult的值：")
print(searchResult)
searchResult = json.loads(searchResult)
print("\n传入html的值：")
print(searchResult[0]['n1']['Name'])
print(searchResult[1]['n2']['Name'])
print(searchResult)
print(len(searchResult))

# 用表格列出所有的关系
tableData = []
for i in range(len(searchResult)):
    relationData = {}
    relationData['entity1'] = searchResult[i]['n1']['Name'];
    relationData['relation'] = searchResult[i]['rel']['type'];
    relationData['entity2'] = searchResult[i]['n2']['Name'];
    tableData.append(relationData);

print('表格数据\n')
print(tableData)

# echarts 数据
data = []
links = []

# 构造展示的数据
maxDisPlayNode = 15
id = 0
for i in range(len(searchResult)):
    # 获取node1d
    node1 = {}
    node1['name'] = searchResult[i]['n1']['Name']
    node1['draggable'] = True
    if ('url' in searchResult[i]['n1']):
        node1['category'] = 1

    else:
        node1['category'] = 2

    flag = 1

    relationTarget = str(id)
    for j in range(len(data)):
        if data[j]['name'] == node1['name']:
            flag = 0
            relationTarget = data[j]['id']
            break

    node1['id'] = relationTarget
    if (flag == 1):
        id += 1
        data.append(node1)

        # 获取node2
    node2 = {}
    node2['name'] = searchResult[i]['n2']['Name']
    node2['draggable'] = True
    if 'url' in searchResult[i]['n2']:
        node2['category'] = 1
    else:
        node2['category'] = 2

    flag = 1
    relationTarget = str(id)
    for j in range(len(data)):

        if data[j]['name'] == node2['name']:
            flag = 0
            relationTarget = data[j]['id']
            break

    node2['id'] = relationTarget;
    if flag == 1:
        id += 1
    data.append(node2)


    # 获取relation
    relation = {}
    relation['source'] = node1['id']
    relation['target'] = node2['id']
    relation['category'] = 0
    flag = 1
    for j in range(len(links)):

        if links[j]['source'] == relation['source'] and links[j]['target'] == relation['target']:

            links[j]['value'] = links[j]['value'] + searchResult[i]['rel']['type']
            flag = 0
            break


    if flag == 1:
        relation['value'] = searchResult[i]['rel']['type']
        relation['symbolSize'] = 10
        links.append(relation)
print('最终结果：')
print(data)
print(links)


    # answer = {'ctx':json.dumps(value, ensure_ascii=False),'entityRelation':json.dumps(answer,ensure_ascii=False)}
    # answer = answer['entityRelation']
    # answer = json.loads(answer)

    # print(answer)

    # print(answer[0]['entity1'])
