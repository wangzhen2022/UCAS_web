# -*- coding: utf-8 -*
import pandas as pd
import codecs
import sys
import importlib

importlib.reload(sys)


f = codecs.open('../data/yahoo/yahoo.csv', mode='r', encoding='utf-8')  # 打开txt文件，以‘utf-8’编码读取
line = f.readline()  # 以行的形式进行读取文件
list1 = []
count=1
while line:
    count=count+1 # count用来观察数据处理进度
    a = line.split()
    #print(a[0])
    if len(a) != 0:

        b = a[0]  # 这是选取需要读取的位数
        list1.append(b)  # 将其添加在列表之中
        line = f.readline()
f.close()

# 保存为csv格式
data1 = pd.DataFrame(list1)
data1.columns = ['passwd']  # 设置列表头
data1.to_csv('../data/test.csv', index=False)
