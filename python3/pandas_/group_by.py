#!/usr/bin/python
# -*- coding: utf-8 -*-

from pandas import DataFrame, Series
import numpy as np
from copy import deepcopy


class GroupBy(object):
    """
    GroupBy: 拆分 - 应用 - 合并, 任何分组关键词中的缺失值, 都会被从结果中除去
    GroupBy对象包含的方法
    """

    def __init__(self):
        self._df = DataFrame({'name': ['b', 'b', 'b', 'a', 'a'],
                              'date': [2018, 2017, 2018, 2018, 2017],
                              'score': [1, 2, 3, 4, 5]},
                             columns=['name', 'date', 'score'])
        self._gb = self._df.groupby('name')
        """
        df
           name  date   score
        0    b   2018      1
        1    b   2017      2
        2    b   2018      3
        3    a   2018      4
        4    a   2017      5
        """

    @property
    def df(self):
        return deepcopy(self._df)

    @property
    def gb(self):
        return deepcopy(self._gb)

    @classmethod
    def print_gb(cls, gb):
        for name, g in gb:
            print('组名=', name, type(g))
            print(g)

    def agg(self):
        """
        聚合函数, agg=aggregate
        agg(func, axis=0, *args, **kwargs)
        Aggregate(聚合) using one or more operations over the specified(指定的) axis.
        参数
        func :
            Accepted combinations are:
                string function name.
                function.
                list of functions.
                dict of column names -> functions (or list of functions).
                axis : {0 or ‘index’, 1 or ‘columns’}, default 0
        axis : default 0
            0 or ‘index’: apply function to each column.(对每一列操作)
            1 or ‘columns’: apply function to each row. (对每一行操作)
        """
        gb = self.gb
        print(gb.agg({'score': max, 'date': min}).reset_index())

        def func(s):
            # 每个分组的每一列
            print(type(s))
            print(s)
            return s.max() - s.min()
        print(gb.agg(func).reset_index())

        # 多个操作
        print("对每一行进行多个操作")
        print(gb.agg(['max', 'min', 'mean']).reset_index())

    def count(self):
        """ 统计每一组的个数 """
        print(self.gb.count())

    def group_by_column(self):
        """ 根据某一列分组  """
        df = self.df
        # 根据日期分组
        gb = df.loc[:, 'name'].groupby(df.loc[:, 'date'])
        print(type(gb))
        for name, g in gb:
            print(g)
        print(gb.sum().reset_index())

    def group_by_dict(self):
        people = DataFrame(np.random.randn(5, 5),
                           columns=['a', 'b', 'c', 'd', 'e'],
                           index=['Joe', 'Steve', 'Wes', 'Jim', 'Travis'])
        mapping = {'a': 'red', 'b': 'red', 'c': 'blue',
                   'd': 'blue', 'e': 'red', 'f': 'orange'}
        gb = people.groupby(mapping, axis=1)
        self.print_gb(gb)
        print(gb.sum())
        print(gb.count())

    def group_by_func(self):
        df = self.df
        # 对index 进行操作
        gb = df.groupby(lambda x: x % 2)
        self.print_gb(gb)

    def iter(self):
        """对分组进行迭代"""
        gb = self.gb
        for name, group in gb:  # 组名, 组中数据
            print("name = %s" % name)
            print(group, type(group))
        print(gb.count().shape)

    def size(self):
        print(self.gb.size())
        """
        (组名, 个数)
        name
        a     2
        b     3
        dtype: int64
        """

    def to_list(self):
        for i in list(self.gb):
            # 组名, df, 长度为2
            print(i, len(i))

    def to_dict(self):
        d = dict(list(self.gb))
        for k, v in d.items():
            # k 组名, v 分组后的df
            print(k, type(v))
            print(v)

    def transform(self):
        df = self.df
        df.columns = ['%s7' % i for i in df.columns]
        print(df)
        gb = df.groupby(by='name')
        print(gb.size())
        print(gb.size().reset_index(name='num'))
        # print(gb.count())
        print(df.merge(gb.size().reset_index(name='num'), on='name', how='left'))
        # 对每个分组取和, 然后赋值给每个分组中的成员
        # tf = gb.transform(sum)
        # print(tf)

if __name__ == '__main__':
    o = GroupBy()
    # o.agg()
    # o.count()
    # o.group_by_column()
    # o.group_by_dict()
    # o.group_by_func()
    o.iter()
    # o.size()
    # o.to_list()
    # o.to_dict()
    # o.transform()
