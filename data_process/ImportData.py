import csv
import py2neo
from py2neo import Graph, Node, Relationship, NodeMatcher
import pandas as pd


# 账号密码
g = Graph('http://localhost:7474', user='neo4j', password='password')

# 打开文件

with open('E:/neo4j-community-4.4.4/import/e_concept.csv', 'r', encoding='utf-8') as f:
    reader = pd.read_csv('E:/neo4j-community-4.4.4/import/e_concept.csv', encoding='utf-8')  # 读每一行数据
    count = 0  # 计数
    for item in reader:
        if reader.line_num == 1:  # 第一行数据无用
            continue
        count = count + 1
        if count % 1000 == 0:
            print(count)
        node = Node("CONCEPT", conceptID=item[0], conceptName=item[1])  # 创建结点
        g.merge(node, "CONCEPT", "conceptID")  # 导入concept结点数据
