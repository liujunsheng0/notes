#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
使用pandas遇到的坑
"""
import pandas as pd
import numpy as np

def is_na():
    s1 = pd.Series(range(3))
    s2 = pd.Series(['a', 'b'])
    s1 = s1.reindex(index=[1, 4])
    s2 = s2.reindex(index=[1, 4])
    s = pd.concat([s1, s2], ignore_index=True)
    # 不会报错..., 只能说nan是个神奇的存在, 更详细的测试见http://www.cnblogs.com/itdyb/p/5806688.html
    print(float('nan'))
    print(type(s))
    for i in s:
        # 判断某个元素是否为NaN时, 不要使用 i == np.nan
        print('i=', i, type(i), type(np.nan), i == 0, i == np.nan)
        # i= 1.0 <class 'float'> <class 'float'> False False
        # i= nan <class 'float'> <class 'float'> False False
        # i= b   <class 'str'>   <class 'float'> False False
        # i= nan <class 'float'> <class 'float'> False False
        try:
            # np.isnan不能传str类型, 貌似只支持数值类型
            print(np.isnan(i))
        except TypeError as e:
            print(False, e)
            #  False
            #  True
            #  False, 'isnan' not supported for the input types,
            #  True
    # 使用自带方法
    print(s.isnull())
    # 0    False
    # 1     True
    # 2    False
    # 3     True
    # dtype: bool

def file_name():
    """ 文件名字/路径包含中文时, pandas引擎需要为Python, C语言对中文的解析有错误 """
    print(pd.read_csv('一.csv', engine='python'))

if __name__ == '__main__':
    # is_na()
    file_name()
