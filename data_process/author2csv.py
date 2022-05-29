import json
import pandas as pd

f = open("D:/Graduation project/Dataset/Academic Social Network/AMiner-Author.txt", encoding='UTF-8')
line = f.readline()
# 结点 作者
id_ls = []
name_ls = []
pc_ls = []
cn_ls = []
hi_ls = []
pi_ls = []
upi_ls = []

# 结点 工作单位
all_aff_dict = {}
all_aff_ls = []
all_aff_id_ls = []

# 结点 研究兴趣
all_cpt_dict = {}
all_cpt_ls = []
all_cpt_id_ls = []

# 关系 作者与工作单位
aa_author_id = []
aa_aff_id = []
aa_type = []

# 关系 作者与研究兴趣
ac_author_id = []
ac_cpt_id = []
ac_type = []

cnt = 0
ID = ''
while line:
    if '#index ' in line:
        ID = line[line.index(' ') + 1:].strip(' ').strip('\n')
        id_ls.append(ID)  # 存储作者Id
        cnt += 1
        if cnt % 1000 == 0:
            print(cnt)
    elif '#n ' in line:
        name = line[line.index(' ') + 1:].strip(' ').strip('\n')
        name_ls.append(name)  # 存储作者姓名
    elif '#a ' in line:
        raw_line = line[line.index(' ') + 1:].strip(' ').strip('\n')
        items = raw_line.split(';')
        for i in items:
            if i != '':
                if all_aff_dict.get(i, 'NONE') == 'NONE':  # 若是字典中没有工作单位就添加
                    all_aff_dict[i] = str(len(all_aff_dict) + 1)
                aa_author_id.append(ID)  # 存储作者的ID号
                aa_aff_id.append(all_aff_dict[i])  # 存储作者的工作单位

    elif '#pc ' in line:
        pc = line[line.index(' ') + 1:].strip(' ').strip('\n')
        pc_ls.append(pc)  # 存储作者发表的论文数
    elif '#cn' in line:
        cn = line[line.index(' ') + 1:].strip(' ').strip('\n')
        cn_ls.append(cn)  # 存储该作者的总引用次数
    elif '#hi ' in line:
        hi = line[line.index(' ') + 1:].strip(' ').strip('\n')
        hi_ls.append(hi)  # 该作者论文的高引用次数，越高代表他的论文影响力越大
    elif '#pi ' in line:
        pi = line[line.index(' ') + 1:].strip(' ').strip('\n')
        pi_ls.append(pi)  # 该作者的 P-index 与 A-index 相等
    elif '#upi ' in line:
        upi = line[line.index(' ') + 1:].strip(' ').strip('\n')
        upi_ls.append(upi)  # 该作者的 A 指数不等的 P 指数
    elif '#t ' in line:  # 作者的研究领域
        raw_line = line[line.index(' ') + 1:].strip(' ').strip('\n')
        items = raw_line.split(';')
        for i in items:
            if i != '':
                if all_cpt_dict.get(i, 'NONE') == 'NONE':  # 若是字典中没有此研究领域就添加
                    all_cpt_dict[i] = str(len(all_cpt_dict) + 1)
                ac_author_id.append(ID)  # 存储作者的id号
                ac_cpt_id.append(all_cpt_dict[i])  # 存储作者研究兴趣
    line = f.readline()  # 读取下一行数据

f.close()
print('Done:', cnt)

for key, val in all_aff_dict.items():
    all_aff_ls.append(key)  # 存储工作单位
    all_aff_id_ls.append(val)  # 存储工作单位索引号

for key, val in all_cpt_dict.items():
    all_cpt_ls.append(key)  # 存储研究兴趣
    all_cpt_id_ls.append(val)  # 存储研究兴趣索引号

aa_type = ['belong2'] * len(aa_aff_id)  # 作者与工作单位的关系为belong
ac_type = ['interest'] * len(ac_cpt_id)  # 作者与研究领域的关系为 interest

dataframe = pd.DataFrame({"authorID:ID": id_ls, "name": name_ls, "pc": pc_ls, "cn": cn_ls, "hi": hi_ls,
                          "pi": pi_ls, "upi": upi_ls})
dataframe.to_csv(r"e_author.csv", sep=',', index=False)  # csv文件存储作者基本信息（结点）

dataframe2 = pd.DataFrame({"affiliationID": all_aff_id_ls, "affiliationName": all_aff_ls})
dataframe2.to_csv(r"e_affiliation.csv", sep=',', index=False)  # csv文件存储工作单位基本信息（结点）

dataframe3 = pd.DataFrame({"conceptID": all_cpt_id_ls, "conceptName": all_cpt_ls})
dataframe3.to_csv(r"e_concept.csv", sep=',', index=False)  # csv文件存储研究领域基本信息（结点）

'''
# R author2affiliation
aa_author_id = []
aa_aff_id = []

# R author2concept
ac_author_id = []
ac_cpt_id = []
'''

dataframe4 = pd.DataFrame({":START_ID": aa_author_id, ":END_ID": aa_aff_id, ":TYPE": aa_type})
dataframe4.to_csv(r"r_author2affiliation.csv", sep=',', index=False)  # csv文件存储作者与工作单位的关系（关系）

dataframe5 = pd.DataFrame({":START_ID": ac_author_id, ":END_ID": ac_cpt_id, ":TYPE": ac_type})
dataframe5.to_csv(r"r_author2concept.csv", sep=',', index=False)  # csv文件存储作者与研究领域的关系（关系）
