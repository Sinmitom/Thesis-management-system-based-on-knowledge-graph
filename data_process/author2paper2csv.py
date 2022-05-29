import json
import pandas as pd

f = open("D:/Graduation project/Dataset/Academic Social Network/AMiner-Author2Paper.txt", encoding='UTF-8')
# 作者 ID 和论文 ID AMiner-Author2Paper.zip 之间的关系。第 1 列是索引，第 2 列是作者 id，第 3 列是论文 id，第 4 列是作者位置。
line = f.readline()
src_ls = []
tar_ls = []
pos_ls = []
type_ls = []
cnt = 0
while line:
    _, src, tar, pos = line.split('	')

    src_ls.append(src)  # 作者id
    tar_ls.append(tar)  # 论文id
    pos_ls.append(pos.strip('\n'))  # 作者位置
    cnt += 1
    if cnt % 50000 == 0:
        print(cnt)
    line = f.readline()

f.close()
type_ls = ['own'] * len(src_ls)  # 作者与论文之间的关系是own
print('Done:', cnt)

dataframe = pd.DataFrame({"START_ID": src_ls, "END_ID": tar_ls, "author_position": pos_ls, "TYPE": type_ls})
dataframe.to_csv(r"r_author2paper.csv", sep=',', index=False)  # csv文件存储作者与论文的关系（关系）
