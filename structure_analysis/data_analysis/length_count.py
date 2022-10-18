import sys
import time
import pandas as pd
from pandas import Series, DataFrame


class Analysis(object):
    def __init__(self, passwdList):
        self.passwdList = passwdList

    def countLength(self):
        count = 0
        list = [0] * 100
        for passwd in self.passwdList:
            count += 1
            list[len(str(passwd)) - 1] += 1
       
        return list


if __name__ == '__main__':
 
    # --------------------读文件模块--------------------#
    data = pd.read_csv('../data/csdn/csdn.csv')
    passwdList = pd.Series(data['passwd'].values) # 读取csv中的额password列


    # --------------------分析模块--------------------#
    data1 = pd.DataFrame(Analysis(passwdList).countLength())
    data1.to_csv('../data/csdn/passwd_length.csv', header=False)

