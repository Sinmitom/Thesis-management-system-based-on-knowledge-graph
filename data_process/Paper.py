import json
import re
import pandas as pd

f = open("D:/Graduation project/Dataset/Academic Social Network/AMiner-Paper.txt", encoding='UTF-8')  # 打开数据文件
line = f.readline()  # 按行读取
# 结点 论文
pid_ls = []  # 论文id
title_ls = []  # 论文标题
year_ls = []  # 论文发表年份
abs_ls = []  # 论文摘要

# 结点 论文收录期刊
all_vue_dict = {}
all_vue_ls = []
all_vue_id_ls = []

# 关系 论文-出版地点
pv_paper_id = []
pv_vue_id = []
pv_type = []

# 关系 引用关系
pp_start_id = []
pp_end_id = []
pp_type = []

cnt = 0

ID = ''
title = ''
year = ''
abstract = ''
raw_line = None
dstID = []

cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9^(^)^.^\s]")  # 匹配所有中文;字母a->z,A->Z;数字0-9;括号和小数点

while line:
    if '#index ' in line:  # 读取到索引行
        ID = line[line.index(' ') + 1:].strip(' ').strip('\n')  # 提取论文的Index号
    if '#* ' in line:
        title = line[line.index(' ') + 1:].strip(' ').strip('\n')
        title.replace('\\', '').replace('\n', '.').replace("\"", '').replace("'", '')  # 去除读取出的杂乱字符
        title = cop.sub('', title)  # 提取论文的标题
    if '#t ' in line:
        year = line[line.index(' ') + 1:].strip(' ').strip('\n')  # 提取论文的发表年份
    if '#! ' in line:
        abstract = line[line.index(' ') + 1:].strip(' ').strip('\n')
        abstract.replace('\\', '').replace('\n', '.').replace("\"", '').replace("'", '')
        abstract = cop.sub('', abstract)  # 提取论文的摘要
    if '#c ' in line:
        raw_line = line[line.index(' ') + 1:].strip(' ').strip('\n')  # 论文的出版地点
    if '#%' in line:
        dstID.append(line[line.index(' ') + 1:].strip(' ').strip('\n'))  # 引用的论文id号
    if line == '\n':  # 读完一条论文数据
        pid_ls.append(ID)  # 列表存储论文id
        title_ls.append(title)  # 列表存储论文标题
        year_ls.append(year)  # 列表存储论文年份
        abs_ls.append(abstract)  # 列表存储论文摘要
        items = raw_line.split(';')
        for i in items:
            if i != '':
                i.replace('\\', '').replace('\n', '.').replace("\"", '').replace("'", '')
                i = cop.sub('', i)  # 提取数据
                if all_vue_dict.get(i, 'NONE') == 'NONE':  # 若是字典中没有收录期刊就添加
                    all_vue_dict[i] = str(len(all_vue_dict) + 1)
                pv_paper_id.append(ID)  # 存储论文的ID号
                pv_vue_id.append(all_vue_dict[i])  # 存储论文的收录期刊
        for i in dstID:  # 论文间的引用关系
            pp_start_id.append(ID)
            pp_end_id.append(i)
        ID = ''
        title = ''
        year = ''
        abstract = ''
        raw_line = None
        dstID = []
        cnt += 1
        if cnt % 5000 == 0:
            print(cnt)
    line = f.readline()  # 读取下一行

f.close()
print('Done:', cnt)

for key, val in all_vue_dict.items():
    all_vue_ls.append(key)  # 存储出版地点列表
    all_vue_id_ls.append(val)  # 存储出版地点的索引号

pv_type = ['belong2'] * len(pv_paper_id)  # 论文与出版地点关系为belong
pp_type = ['refer'] * len(pp_start_id)  # 论文与论文之间关系为相互引用

dataframe = pd.DataFrame({"paperID": pid_ls, "title": title_ls, "year": year_ls, "abstract": abs_ls})
dataframe.to_csv(r"e_paper.csv", sep=',', index=False)  # csv文件存储论文基本信息（结点）

dataframe2 = pd.DataFrame({"venueID": all_vue_id_ls, "name": all_vue_ls})
dataframe2.to_csv(r"e_venue.csv", sep=',', index=False)  # csv文件存储论文出版地点基本信息（结点）

dataframe3 = pd.DataFrame({"START_ID": pv_paper_id, "END_ID": pv_vue_id, "TYPE": pv_type})
dataframe3.to_csv(r"r_paper2venue.csv", sep=',', index=False)  # csv文件存储论文与出版机构之间的关系（关系）

dataframe4 = pd.DataFrame({"START_ID": pp_start_id, "END_ID": pp_end_id, "TYPE": pp_type})
dataframe4.to_csv(r"r_citation.csv", sep=',', index=False)  # csv文件存储论文之间的引用关系（关系）
