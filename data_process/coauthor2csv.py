import json
import pandas as pd
f = open("D:/Graduation project/Dataset/Academic Social Network/AMiner-Coauthor.txt", encoding='UTF-8')

line = f.readline()
src_ls = []
tar_ls = []
weight_ls = []
cnt = 0
while line:
    string = line.replace('#', '').strip()
    src, tar, weight = string.split('	')

    src_ls.append(src)   # 第一位作者
    tar_ls.append(tar)   # 第二位作者
    weight_ls.append(weight)  # 合作的权重
    cnt += 1
    if cnt % 50000 == 0:
        print(cnt)
    line = f.readline()

f.close()
print('Done:', cnt)
type_ls = ['Collaborate'] * len(src_ls)   # 作者与作者之间的关系是Collaborate
dataframe = pd.DataFrame({"START_ID": src_ls, "END_ID": tar_ls, "n_cooperation": weight_ls, "TYPE": type_ls})
dataframe.to_csv(r"r_coauthor.csv", sep=',', index=False)  # csv文件作者与作者之间合作的关系（关系）


