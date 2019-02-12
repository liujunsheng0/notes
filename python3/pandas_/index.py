#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

class Index(object):
    """ 标签类, pd.Index, 不可变对象 """
    def __init__(self):
        s = pd.Series([1, 2, 3], index=[1, 2, 3])
        self.index1 = s.index.astype(np.int64)
        self.index2 = pd.Index([3, 4, 5])

    def base(self):
        index1, index2 = self.index1, self.index2
        print('index1', index1)
        print('index2', index2)
        print("isinstance(obj, pd.Index)", isinstance(index1, pd.Index))
        # index[0] = 1 # 值不可变
        # 连接另一个index, 新对象
        print("append", index1.append(index2))
        # 差集, 交集, 并集
        print(index1.difference(index2), index1.intersection(index2), index1.union(index2))
        # 删除指定索引处的值, 越界会崩溃
        print("delete", index1.delete(1))
        # 删除指定的值, 不在会或值不唯一的话会引起崩溃
        print("drop", index1.drop(1))
        # 指定位置插入值
        print("insert", index1.insert(0, 100))
        print('is_unique', index1.is_unique)
        # 取唯一值
        print('unique', index1.append(index2).unique())


if __name__ == '__main__':
    i = Index()
    i.base()
