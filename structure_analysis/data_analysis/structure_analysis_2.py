#-*- coding: UTF-8 -*-
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

    def countDorL(self):

        dic = { 'D1': {}, 'D2': {}, 'D3': {}, 'D4': {}, 'D5': {}, 'D6': {}, 'D7': {}, 'D8': {}, 'D9': {},
               'D10': {},'D11': {}, 'D12': {}, 'D13': {}, 'D14': {}, 'D15': {}, 'D16': {}, 'D17': {}, 'D18': {}, 'D19': {},}

        patternLetter = re.compile(r'[A-Za-z]+$')  # 生成一个正则表达式对象，用于匹配字母
        patternDigit = re.compile(r'\d+$')  # 这两个正则表达式对象用于匹配数字和特殊字符
        patternSig = re.compile(r'\W+$')  # 正则表达式是一个特殊的字符序列，它能帮助你方便的检查一个字符串是否与某种模式匹配。

        for line in self.passwdList:  # 遍历每一条口令

            line = str(line)
            l = ''
            if patternLetter.match(line):   # 如果是纯字母
                l = 'L' + str(len(line))
     
            elif patternDigit.match(line):  # 如果是纯数字
                l = 'D' + str(len(line))
            elif patternSig.match(line):    # 如果是纯特殊字符
                l = 'S' + str(len(line))

            if l in dic:                # 去字典中查询该纯口令
                if line in dic[l]:
                    dic[l][line] += 1  # 记录该纯口令出现的次数
                else:
                    dic[l][line] = 1

        df = DataFrame(columns=('structure', 'nums', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'))
        
        for tp in dic:  # 逐行遍历字典
            every_dic = dic[tp]  # tp为字典中的逐个纯字符串,every_dic为每行的所有键值对 tp=S1
            sums = sum(every_dic.get(x) for x in every_dic)  # 记录纯字符串总数 every_dic={'*': 1, '%': 1} sums=2
            rows = [tp, sums]  # 键值对
            every_dic = sorted(every_dic.items(), key=lambda x: x[1], reverse=True)  # 给所有的字典值排序（按照数量，降序）

            for r in range(10): # 统计最常见的十种口令，不足十个的用0补齐
                if r < len(every_dic):
                    rows.append(str(every_dic[r]))
                else:
                    rows.append(0)
            df.loc[tp] = rows  # 将rows存储到每行中
        df = df.sort_values(by='nums')  # 按照nums进行排序
        return df


if __name__ == '__main__':
    time1 = time.perf_counter()

    # --------------------读文件模块--------------------#
    # 读取文件
    data = pd.read_csv('../data/csdn/csdn.csv')
    passwdList = pd.Series(data['passwd'].values)

    # 记录读文件的时间
    # time2 = time.perf_counter()
    #print( 'read file time : ', (time2 - time1))
    
    # --------------------分析模块--------------------#
    ana = Analysis(passwdList)

    # 分析生成仅由字母/数字组成的口令数量, 以及每种结构频率TOP10的口令
    ana.countDorL().to_csv('../data/csdn/onlyLorD_analysis_csdn.csv', index=False)

    # 记录分析生成的时间
    # time3 = time.perf_counter()
    # print( 'Analysis time : ', (time3 - time2))
