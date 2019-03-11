#!/usr/bin/python
# -*- coding: utf-8 -*-

from pandas import Series
from copy import deepcopy
import pandas as pd
import numpy as np

class series(object):
    """
    Series是一种类似于一维数组的对象, 它由一组数据(各种NumPy数据类型) 以及一组与之相关的数据标签(labels, 即索引)组成,
    它会根据运算的索引标签自动对齐数据.

    label: 标签, 可标签可重复, 取数据时如果碰到重复标签, 则全部取出

    NaN : 即"非数字" not a number, 在pandas中, 它用于表示缺失或NA值
    NA : not available

    切片操作: 包含末端数据
    """
    def __init__(self):
        # 如果没有指定索引会自动创建一个0到N-1(N为数据的长度)的整数型索引
        self._s = Series((1, 2, 3), index=('a', 'b', 'c'))
        """
    (索引, 标签)  值
        a         1
        b         2
        c         3
        dtype: int64
        """

    @property
    def s(self):
        return deepcopy(self._s)

    def base(self):
        s = self.s
        # s的索引(标签)
        print(s.index, s.values)   # Index(['a', 'b', 'c'], dtype='object') [1 2 3]
        print(s.shape, len(s))     # (3,) 3
        # 判断 val 是否在s的索引中, in 取的是s中的索引值
        print('a' in s, 100 in s)  # True False
        # for 取的是s中的值
        print([i for i in s])      # [1, 2, 3]

        # 重复标签, 重命名index
        s.index = ['a', 'a', 'b']
        print(s)
        print(s.loc['a'])

    def choice(self):
        s = self.s
        # s 中大于2的那部分数据
        print(len(s.loc[s > 2]))

    def get(self):
        s = self.s
        # 如果不在s中会抛异常, 取值的方式类似于dict
        if 'a' in s:
            print('s[0]', s[0], s['a'])  # 二者等价, Series可看做一个ndarray来处理,根据下标取值
        print('get', s.get('a', 'default'), s.get('e', 'default'))

        print('部分标签')
        # 部分标签, 以下两种方式等价, 但是根据标签取值更好, 推荐使用loc, iloc
        # 标签取值
        print(s[['a', 'c']])
        print(s.loc[['a', 'c']])
        # 下标取值
        print(s[[0, 2]])
        print(s.iloc[[0, 2]])

        # 切边, 下标的切片不包含2,右边是开区间; 标签的切片包含'c',右边是闭区间
        print('切片')
        print(s[:2])
        print(s[:'c'])

    def operate(self):
        """
        Series之间的操作会基于label(标签)对数据自动对齐
        pandas最重要的一个功能是, 可以对不同索引的对象进行算术运算. 在将对象相加时, 如果存在不同的索引对,
        则结果的索引就是该索引对的并集, 除并集的索引处值为NA
        """
        s1 = self.s
        print(s1 + 2)
        print(s1 - 2)
        print(s1 * 2)
        print(s1 / 2)
        print(" +-*/ ")
        s2 = Series((1, 2, 3, 4), index=('a', 'b', 'c', 'd'))
        # 只有双方都有的标签才会进行对应的操作, 其余为NaN
        print(s1 + s2)
        print(s1 - s2)
        print(s1 * s2)
        print(s1 / s2)

    def count(self):
        # 返回series中非NaN的个数
        print(self.s.count())

    def cut(self):
        """
        用处: 连续数据常常被离散化或拆分为"面元(bin)", 假设有一组人员数据, 将它们划分为不同的年龄组, 则可使用cut
        返回: Categorical对象
        qcut: 根据样本分位数对数据进行面元划分
        cut可能无法使各个面元中含有相同数量的数据点, 即根据范围划分;
        qcut由于使用的是样本分位数, 因此可以得到大小基本相等的面元, 即保证每个面元个数基本相等

        cut(x, bins, right=True, labels=None, retbins=False, precision=3, include_lowest=False)
        x : array-like
            Input array to be binned(容器). It has to be 1-dimensional(一维数组)

        bins(面元) : int, sequence of scalars(数量, 标量), or IntervalIndex
            If `bins` is an int, it defines the number of equal-width bins in the
            range of `x`.However, in this case, the range of `x` is extended(延伸, 扩展)
            by .1% on each side to include the min or max values of `x`.
            If `bins` is a sequence it defines the bin edges allowing for
            non-uniform bin width. No extension of the range of `x` is done in
            this case.
        
        x, array对象,且必须为一维
        bins, 整数、序列、或间隔索引.
              如果bins是一个整数,它定义了x宽度范围内的等宽面元数量,但是在这种情况下,x的范围在每个边上被延长1%,
              以保证包括x的最小值或最大值.
              如果bin是序列,它定义了允许非均匀bin宽度的bin边缘.在这种情况下没有x的范围的扩展.
        right, 布尔值.是否是左开右闭区间
        labels,用作结果箱的标签.必须与结果箱相同长度.如果FALSE,只返回整数指标面元.
        retbins,布尔值.是否返回面元
        precision, 整数.返回面元的小数点几位(限定小数位数)
        include_lowest,布尔值.第一个区间的左端点是否包含
        """
        s = Series([3, 2, 2.1, 2, 2, 2, 2, 2, 1])
        # 传入的是数字, 根据数据的最小值和最大值计算等长面元
        print(pd.cut(s, 4))
        # 分为 (0,1], (1,2], (2,3]三个面元
        c = pd.cut(s, [0, 1, 2, 3])
        print(c)
        # 设置面元名称
        print(pd.cut(s, [0, 1, 2, 3], labels=['0-1', '1-2', '2-3']))
        # qcut, series中的值 必须唯一
        print(pd.qcut(s.unique(), 4))

    def concat(self):
        """
        concat 合并, 连接
        concat(objs, axis=0, join='outer', join_axes=None, ignore_index=False, keys=None, levels=None,
               names=None, verify_integrity=False, copy=True)
        join: 连接方式 {'inner', 'outer'}, default 'outer'
        join_axes: 指定要使用的索引
        """
        s1 = pd.Series([0, 1, 1], index=['a', 'b', 'c'])
        s2 = pd.Series([2, 3, 4], index=['c', 'd', 'e'])
        s3 = pd.Series([5, 6], index=['f', 'g'])
        # 并集
        print(pd.concat([s1, s2, s3]))  # 返回series
        # 按列合并, 每个series是一列, 索引为index的并集, 不在series的index值为NaN, 返回dataframe
        print(pd.concat([s1, s2, s3], axis=1))

        # 取交集
        s4 = pd.concat([s1, s3])
        print(pd.concat([s1, s4], axis=1, join='inner'))
        print(pd.concat([s1, s2], axis=1, join_axes=[['a', 'e']]))

    def dt(self):
        """Series中的对象如果是datetime/period,可以用自带的.dt访问器返回日期、小时、分钟"""
        s = pd.Series(pd.date_range('20160101 09:10:12', periods=4))
        print(s)
        print(s.dt.day)
        print(s.dt.second)

    def drop(self):
        """丢弃某个标签, 如果标签不在抛异常"""
        s = self.s
        print(s.drop(['a']))

    def dropna(self):
        """ 丢弃值为 Na的数据 """
        s = Series([1, np.nan, 2])
        print(s.dropna())  # 等价于s.loc[s.notnull()]

    def fillna(self):
        """ 将NA替换为指定的值 """
        s = Series([1, np.nan, 2])
        print(s.fillna(value='fill'))

    def iter(self):
        s = self.s
        for k, v in s.iteritems():
            print(k, v)

        for v in s:
            print(v)

    def idx_(self):
        """返回最小值和最大值对应的index"""
        s = self.s
        print(s.idxmax())
        print(s.idxmin())

    def isin(self):
        """ 如果值在数据中, 为True, 否则为False, 返回相同index的Series """
        s = self.s
        print(s.isin([1, 2]))

    def max_min(self):
        s = self.s
        print(s)
        print('index=-1: ', s.iloc[-1])
        # 返回前N个最大/最小值
        print(s.nsmallest(2))
        print(s.nlargest(2))

    def map(self):
        """ 对Series中的每个元素进行操作 """
        s = self.s
        # 函数
        print(s.map(lambda x: x * 2))
        # dict, v -> dict.get(v, NaN)
        print(s.map({1: '11', 2: '22'}))

    def null(self):
        s = Series([1, 2, 3, np.NaN])
        print(s.isnull())
        print(s.loc[s.isnull()])
        print(s.notnull())
        print(s.loc[s.notnull()])

    def replace(self):
        """ 替换值 """
        s = self.s
        print(s.replace(1, 11))
        # 值 in [1, 2] 替换为 11
        print(s.replace([1, 2], 11))
        # 值为1的替换为11, 值为2的替换为22
        print(s.replace([1, 2], [11, 22]))

    def reindex(self):
        """
        重新索引, reindex(index=None, **kwargs)
        根据新的索引创建一个新对象, 用该Series的reindex将会根据新索引进行重排。如果某个索引值当前不存在，就引入缺失值
        index : 新的index 序列
        method: 填充方式
        fill_value: 值为NaN的替换值
        """
        s = self.s
        print(s.reindex(['a', 'c', 'e']))

    def string(self):
        """
        官方文档: https://pandas.pydata.org/pandas-docs/stable/api.html#string-handling
        series 自带的字符串方法, 即基本类型 str 的方法
        """
        s = Series(['a_b', 'c_d'])
        print(s.str.upper())
        print(s.str.len())
        print(s.str.strip())
        t = s.str.split('_')
        print(type(t), t)
        # expand : bool, default False, expand(扩展, 扩张)
        # * If True, return DataFrame/MultiIndex expanding dimensionality; If False, return Series/Index.
        t = s.str.split('_', expand=True)
        print(type(t), t)
        print("str.contains")
        print(s.str.contains('_c', na='', regex=False, case=False))
        # 正则表达式
        print(s.str.findall('[a-z]'))
        print(s.str[:2])

    def sort_index(self):
        """在排序时，任何缺失值默认都会被放到Series的末尾(不管是升序还是降序)"""
        s = self.s
        print(s.sort_index(ascending=False))

    def take(self):
        s1 = pd.Series([0, 1, 0, 0] * 2)
        s2 = pd.Series(['apple', 'orange'])
        # s1.value 根据s2的index, 找到对应值
        s3 = s2.take(s1)
        print(type(s3))
        print(s3.index, s3.values)
        # index 为1和2的数据
        print(s1.take([1, 2]))

    def tolist(self):
        s = self.s
        print(s.tolist())  # value 的list

    def to_dict(self):
        s = self.s
        print(s.to_dict())

    def to_datetime(self):
        """ 解析多种不同的日期表示形式 """
        t = Series(['2011-01-01 12:00:00',
                    '2011/1/2',
                    '2011-1-3',
                    '2011年1月2日'])
        # 解析错误的转换为NaT, (NOT A TIME)
        s = pd.to_datetime(t, errors='coerce')
        s1 = pd.to_datetime(t, errors='coerce', format='%Y年%m月%d日')
        nat = s.loc[3]
        print(type(nat), nat > s.loc[1], s.loc[1].day - nat.day)
        print(s)
        print(s1)

    def uniques(self):
        """获取唯一值数据"""
        s = pd.Series([1, 1, 2, 1, 2])
        print(s.unique())

    def value_counts(self):
        """按值出现频率降(升)序排列"""
        c = Series((1, 2, 3, 2)).value_counts()
        print(type(c), c.index)
        print(c)

    def test(self):
        s = Series([-1,-2,-3])
        print(abs(s))
if __name__ == '__main__':
    o = series()
    # o.base()
    # o.choice()
    # o.get()
    # o.operate()
    # o.cut()
    # o.concat()
    # o.dt()
    # o.drop()
    # o.dropna()
    # o.fillna()
    # o.iter()
    # o.idx_()
    # o.isin()
    # o.max_min()
    # o.map()
    # o.null()
    # o.reindex()
    # o.replace()
    o.string()
    # o.tolist()
    # o.to_datetime()
    # o.take()
    # o.uniques()
    # o.value_counts()
    # o.test()
