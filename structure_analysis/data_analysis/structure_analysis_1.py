import sys

import configparser
import time
import re
import csv

import pandas as pd
from pandas import Series, DataFrame


class Analysis(object):
    def __init__(self, passwdList):
        self.passwdList = passwdList

    #统计口令结构
    def countStruc(self):
        strucList = []
        for passwd in self.passwdList:  # 遍历每一行口令

            struc = ''
            passwd = str(passwd)  # 将passwd对象转为字符串
            for ch in passwd:  # 遍历每口令中的每一个字符
                if ch.isdigit():
                    struc += 'D'
                elif ch.isalpha():
                    struc += 'L'
                else:
                    struc += 'S'
            strucList.append(struc)

        # print("step one:", strucList)  # step one : for test

        # 统计每种结构的口令数量
        nums = {}  # 定义一个dic,键为口令结构，值为结构数量
        for stru in strucList:  # 在结构数组中遍历每一种结构

            if stru in nums.keys():  # 如果该结构已经被统计（即在字典nums的键中能找），则结构出现次数+1
                nums[stru] += 1
            else:  # 如果该结构没有被统计过，则更新字典，并将出现次数设定为1
                nums[stru] = 1

        # print("step two:", nums)  # step two for test
        df = DataFrame(columns=('structure', 'nums', 'freq'))  # 输出csv文件的列名，共存储三列，分别存储口令结构，口令数量以及该结构口令出现的频率
        for x in nums.keys():  # 遍历字典的每一个键，即遍历每一种结构

            char = x[0]  # 将第一个字母定为标志字符
            stru = x[1:]  # stru为结构的第二个字符往后的字符串
            c = 1  # 计数器置为1
            res = ''
            for i in stru:  # 遍历第二个字符往后的每一个字符
                if i == char:  # 如果某一个字符与第一个字符相同
                    c += 1  # 计数器加一
                else:  # 如果该字符与第一个字符不想图
                    res += char  # 则将该字符存入结果字符串中
                    res += str(c)  # 并且记录该字符的个数
                    char = i  # 更新当前字符为标志字符
                    c = 1  # 重置计数器
            res += char
            res += str(c)

            ge = '{:.18f}'.format(int(nums[x]) * 1.0 / len(strucList))  # 计算频率
            df.loc[x] = [x, nums[x], ge]  # 将结构串，数量，以及频率存储到DataFrame中
            pd.set_option('mode.chained_assignment', None)

            df['structure'][x] = res

        df = df.sort_values(by='nums',ascending=False)  # 根据nums进行排序

        # print("step three:", df)
        return df




if __name__ == '__main__':
    time1 = time.perf_counter()

    # --------------------读文件模块--------------------#
    # 读取文件
    data = pd.read_csv('../data/csdn/csdn.csv',encoding='gbk')
    passwdList = pd.Series(data['passwd'].values)

    # 记录读文件的时间
    time2 = time.perf_counter()
    #print( 'read file time : ', (time2 - time1))

    # --------------------分析模块--------------------#
    ana = Analysis(passwdList)

    # 分析生成口令结构/对应数量/出现概率的字符串
    ana.countStruc().to_csv('../data/csdn/str_analysis_csdn.csv',index = False)


    # 记录分析生成的时间
    time3 = time.perf_counter()
    #print( 'Analysis time : ', (time3 - time2))
