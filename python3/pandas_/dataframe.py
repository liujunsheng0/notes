#!/usr/bin/python
# -*- coding: utf-8 -*-

from pandas import DataFrame, Series
import pandas as pd
from copy import deepcopy
import numpy as np


class dataframe(object):
    """
    易错点:
        read_csv(engine='python')时路径有中文时, C引擎报错, 使用Python引擎解决问题
        (https://blog.csdn.net/ArcheriesYe/article/details/77992412)

    官方接口解释: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.rank.html

    dataframe 横竖都是Series对象

    所有需要沿着坐标轴计算的方法, 默认axis=0, 一般是将方法应用到每一列数据上

    如果pandas对象的一列中有多种数据类型, dtype返回的是能兼容所有数据类型的类型, 一般为object(祖先类...)
    """
    def __init__(self):
        # 如果指定了行/列序列, DataFrame会按照指定顺序进行排列
        self._df = DataFrame({'Name': ['a', 'b', 'c'], 'Age': [1, 2, 2], 'Height': [1, 3, 4]})
        # 将列名重置为小写, 对列重新命名
        self._df.columns = [x.lower() for x in self._df.columns]

    @property
    def df(self):
        return deepcopy(self._df)

    def init(self):
        d = {'one': Series([1., 2., 3.], index=['a', 'b', 'c']),
             'two': Series([1., 2., 3., 4.], index=['a', 'b', 'c', 'd'])}
        """ one	two
        a	1.0	1.0
        b	2.0	2.0
        c	3.0	3.0
        d	NaN	4.0
        """
        print(DataFrame(d, index=['d', 'b', 'a'], columns=['two', 'three']))
        """	two	three
        d	4.0	NaN
        b	2.0	NaN
        a	1.0	NaN
        """
        print(DataFrame([{'a': 1, 'b': 2}, {'a': 5, 'b': 1, 'c': 2}], index=['x', 'y']))
        ''' a   b     c
         x  1   2   NaN
         y  5   1   2
        '''

    def base(self):
        df = self.df
        print(df.index)    # 行label
        print(df.columns)  # 列label
        print(df.values, type(df.values[0]))  # 返回的是类似于二维数组的格式
        # 查看数据类型
        print(df.dtypes)
        # 查看DataFrame的形状, (行数, 列数)
        print(df.shape)
        # 查看索引、数据类型和内存信息
        print(df.info())
        # 对数据有大概的了解
        print(df.describe())
        # 查看前(后)N列
        print(df.head())
        print(df.tail())

    def correct(self):
        """
        如果将列表或数组赋值给某个列时, 其长度必须跟DataFrame的长度相匹配,
        如果赋值的是一个Series, 就会精确匹配DataFrame的索引, 所有的空位都将被填上缺失值(即df中的索引不在s中的值为NaN)
        """
        df = self.df.loc[:, ['name']]
        # 添加列, 按照索引赋值, 如果索引对不上, 值为NaN
        df.loc[:, 'age'] = Series([1, 2, 3], index=(3, 2, 1))
        df.loc[:, 'copy'] = df.loc[:, 'age']
        # 直接赋值, 这一列都是该值
        df.loc[:, 'school'] = 'NB'
        df.loc[:, 'home'] = ['tianjin', 'beijing', 'shanghai']
        print(df)

    def delete(self):
        df = self.df
        # 删除列
        del df['age']
        df.pop('height')
        print(df)

    def operate(self):
        """
        还可以使用如下运算进行运算, 下述方法功能更强大
        add(), sub(), mul(), div(), radd(), rsub
        """
        df1 = self.df
        df2 = DataFrame({'age': [1, 2, 3], 'home': {'tianjin', 'beijing', 'shanghai'}})
        # df + df
        # 自动对index和column进行数据对齐, 运算结果的index和columns是参与运算的DataFrame的index和columns的并集
        # 双方都存在的index和columns 才会进行运算, 其余都为NaN
        print(df1 + df2)

        s = Series({'age': 1, 'name': 'a', 'height': 1})
        # df + series, df的column和series的index对齐,
        # series可以缺标签, 但是不能多标签, 不然会抛异常, 缺少对应标签处, 值为NaN
        print(df1 + s)

        # +-*/, 注意数据类型
        df = df1.loc[:, ['age', 'height']]
        print(df + 2)
        print(df - 2)
        print(df * 2)
        print(df / 2)

    def get(self):
        """ 官方推荐使用loc, iloc, ix将被弃用 """
        df = self.df
        # 获取 name 列, 返回Series, 以下三种等价, 官方推荐loc
        print(type(df['name']), type(df.loc[:, 'name']))
        print(df['name'])
        print(df.loc[:, 'name'])
        print(df.name)
        # 获取 name 列, 返回DataFrame
        print(type(df[['name']]))
        print(df[['name']])

        print(df.loc[1])  # 取索引为1的那一行, 默认为取所有列
        print(df.loc[1, ['age', 'name']])
        # iloc 根据位置取值, 如取 第一行 第三列的值, 和第一行, 第一列到第三列的的值
        # iloc 可以使用切片
        print(df.iloc[0, 2])
        print(df.iloc[0, :2])

    def query1(self):
        """二元比较方法: eq, ne, lt, gt, le, ge等"""
        df1 = DataFrame({'Age': [1, 2, 3]})
        df2 = DataFrame({'Age': [3, 2, 1]})
        # 使用equals()方法进行比较时,两个对象如果数据不一致必为False,甚至如果label的顺序不一致也返回False
        print(df1.eq(df2).equals(df1 == df2))
        print(df1.ne(df2).equals(df1 != df2))
        print(df1.gt(df2).equals(df1 > df2))
        print(df1.lt(df2).equals(df1 < df2))
        print(df1.le(df2).equals(df1 <= df2))
        print(df1.ge(df2).equals(df1 >= df2))

    def query2(self):
        """可以利用any(all) 降维和筛选数据"""
        df = DataFrame({'Age': [1, 2, 3], 'Height': [3, 2, 1]})
        # 某一行数据全部(存在)大于2, 则返回True
        print((df > 2).all())
        print((df > 2).any())
        print((df > 2).all().all())
        print((df > 2).any().any())

    def astype(self):
        """转换数据类型"""
        df = self.df
        print(df[['age', 'height']].astype(float))

    def agg(self):
        """
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
        df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [np.nan, np.nan, np.nan]], columns=['A', 'B', 'C'])
        print(df.agg(['sum', 'min']))
        print(df.agg({'A': 'sum', 'B': 'min'}))
        print(df.agg({'A': ['sum', 'min'], 'B': 'min'}))
        print(df.agg({'A': ['sum', 'min'], 'B': ['min', 'max']}))
        print(df.agg("mean", axis=1))

    def append(self):
        """
        如果只想对Series或DataFrame对象进行 行拼接(axis=0), 推荐使用append()方法
        注意: 当ignore_index=False时, 如果是对DataFrame对象进行append操作, 要注意他们的索引值交集必须为空!
              即每个DataFrame对象的索引值都不相同, 列名不作要求.()
        """
        df1 = self.df
        df2 = self.df
        df2.index = ['append=%s' % i for i in df2.index]
        print(df1.append(df2))
        print(df1.append([df2, df2], ignore_index=True))
        df2.loc[:, 'other'] = df2.loc[:, 'age']
        print(df1.append(df2))
        print(df1.append([df2, df2], ignore_index=True))

    def align(self):
        """
        使两个df互相对齐, 有点像left.merge(right), right.merge(left)的合并
        left.join(right)
        :return (对齐后的left, 对齐后的right), 类型为DataFrame
        让两个对象同事 <相互对齐> 的最快方法.它含有join参数,
            join='outer': 取得两个对象的索引并集, 这也是join的默认值.
            join='left': 使用调用对象的索引值
            join='right'：使用被调用对象的索引值
            join='inner': 使用两个对象的索引交集
        align()方法返回一个元组,元素元素是重新索引的Series对象.
        """
        df1 = self.df
        df2 = DataFrame({'name':  ['a', 'b', 'c'], 'address': ['tianjin', 'beijing', 'shenyang']}, index=list('abc'))
        for align in (df1.align(df2, join='outer'), df1.align(df2, join='left')):
            print(type(align[0]))
            print(align[0])
            print(align[1])

    def apply(self):
        """ 任意函数都可以直接对DataFrame某一坐标轴进行直接操纵, 只需要使用apply()方法即可 """
        df = DataFrame({'age': [1, 2, 2], 'height': [1, 3, 4]})
        print(df.apply(lambda x: x.max() - x.min()))

        def func(s: Series, a, b=0):
            print('a = %s, b=%s' % (a, b))
            sum_ = s.sum()
            s.loc['max_index'] = s.idxmax()
            s.loc['sum'] = sum_
            return s
        # apply()方法支持接收其他参数
        print(df.apply(func, args=('a', 'b')))  # 对每一列进行操作
        print(df.apply(func, axis=1, a='c', b='d'))  # 对每一行操作

    def applymap(self):
        """ 对单个元素应用Python方法 """
        df = self.df

        def func(x):
            return 'x=%s' % x
        print(df.applymap(func))

    def combine_first(self):
        """
        根据索引将重复数据拼接在一起，用一个对象中的值填充另一个对象中的缺失值
        """
        df1 = self.df
        df2 = DataFrame({'name': ['a', 'b', np.nan], 'age': [np.nan, np.nan, 2], 'height': [1, 3, np.nan]}, index=[1, 2, 3])
        # 根据索引将df2中NaN的元素, 用df1中对应位置的元素替换, 返回一个新的dataframe
        print(df2.combine_first(df1))

    def combine(self):
        """
        对两个df中的列分别进行操作
        DataFrame.combine(other, func, fill_value=None, overwrite=True)
        Add two DataFrame objects and do not propagate(传播, 广播) NaN values, so if for a (column, time) one frame
        is missing a value, it will default to the other frame's value (which might be NaN as well)
        对列进行操作 (两个df相加, 不广播NaN, 如果某个df缺少一个值, 返回另一个df中对应的数据(也可能是NaN))
        func: Function that takes two series as inputs and return a Series (输入两个series对象, 返回series)
        """
        df1 = DataFrame({'A': [0, 0], 'B': [4, 4]})
        df2 = DataFrame({'A': [1, 1], 'B': [3, 3]})

        def func(s1, s2):
            print('==============')
            print(s1, type(s1), s1.index, s1.values, s1.sum())
            print(s2, type(s2), s2.index, s2.values, s2.sum())
            return s1 if s1.sum() < s2.sum() else s2
        df = df1.combine(df2, func)
        print(df)
        """
           A  B
        0  0  3
        1  0  3
        """
        df2.iloc[:, 1] = np.nan
        df = df1.combine(df2, lambda s1, s2: s1 if s1.sum() < s2.sum() else s2)
        print(df)
        """
           A   B
        0  0 NaN
        1  0 NaN
        """
        del df1['A']
        df = df1.combine(df2, lambda s1, s2: s1 if s1.sum() < s2.sum() else s2)
        print(df)
        """
            A   B
        0 NaN NaN
        1 NaN NaN
        """

    def drop(self):
        """
        drop(labels=None, axis=0, index=None, columns=None, level=None, inplace=False, errors='raise')
        labels : single label or list-like, Index or column labels to drop.
        axis : {0 or ‘index’, 1 or ‘columns’}, default 0, 舍弃行
               Whether to drop labels from the index (0 or ‘index’) or columns (1 or ‘columns’).
               index, columns : single label or list-like
               Alternative to specifying axis (labels, axis=1 is equivalent to columns=labels).

        level : int or level name, optional
                For MultiIndex, level from which the labels will be removed.

        inplace : bool, default False, If True, do operation inplace and return None.

        errors : {‘ignore’, ‘raise’}, default ‘raise’
            If ‘ignore’, suppress error and only existing labels are dropped. 出现错误不抛异常, 只是丢弃该条数据
        """
        df = self.df
        # 舍弃行
        print(df.drop(1))
        # 舍弃列
        print(df.drop('age', axis=1))

    def dropna(self):
        """
        DataFrame.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
        根据各标签的值中是否存在缺失数据对轴标签进行过滤,可通过阈值调节对缺失值的容忍度
        默认丢弃任何含有缺失值的行
        axis :
            决定包含NaN的行/列是否被移除
            0, or ‘index’ : Drop rows which contain missing values.(丢弃列)
            1, or ‘columns’ : Drop columns which contain missing value.(丢弃行)
        how : {‘any’, ‘all’}
            any : 如果存在任何NA值,则放弃该标签
            all : 如果所有的值都是NA值,则放弃该标签
        thresh : int, 默认值 None, 每行/列中的NaA个数  >thresh 才移除该条数据
        subset : 只对指定的index/columns中的数据判断是否为NaN
        inplace : 如果=True, 则直接在原对象操作, 返回None
        """
        df = DataFrame({'name': ['a', 'b', np.nan], 'age': [1, np.nan, np.nan]})
        print(df.dropna())
        print(df.dropna(thresh=1))
        # 如果每行中, 'name'为NaN, 则丢弃改行
        print(df.dropna(subset=['name']))
        # 如果列中 index=1处 存在NaN, 则丢弃该列
        print(df.dropna(axis=1, subset=[1]))

    def duplicated(self):
        """
        duplicated(self,subset=None, keep='first')
        标记重复行, 返回一个布尔型Series, 表示各行是否是重复行
        subset：用于识别重复的列标签或列标签序列，默认所有列标签
        keep=‘frist’：除了第一次出现外，其余相同的被标记为重复
        keep='last'：除了最后一次出现外，其余相同的被标记为重复
        keep=False：所有相同的都被标记为重复
        """
        df = DataFrame({'name': ['a', 'a', 'c'], 'age': [2, 2, 2], 'height': [3, 3, 4]})
        df.duplicated()

    def drop_duplicates(self):
        """
        去除指定列下面的重复行, 默认取全部的列
        drop_duplicates(subset=None, keep='first', inplace=False)
        subset : column label or sequence of labels, optional, 用来指定特定的列，默认所有列
        keep : {‘first’, ‘last’, False},
            first: 删除重复项并保留第一次出现的项
            last: 删除重复项并保留最后一次出现的项
            False: 丢弃所有重复行
        inplace : boolean, default False, 是直接在原来数据上修改还是保留一个副本
        """
        df = DataFrame({'name': ['a', 'a', 'c'], 'age': [2, 2, 2], 'height': [3, 3, 4]})
        print(df.drop_duplicates(['name', 'age', 'height']))

    def fillna(self):
        """
        DataFrame.fillna(value=None, method=None, axis=None, inplace=False, limit=None, downcast=None, **kwargs)
        value : scalar, dict, Series, or DataFrame
            value 用于填充缺失值;
            a dict/Series/DataFrame of values specifying which value to use for each index (for a Series)
            or column (for a DataFrame, 对不同的列填充不同的值)
        method : {‘backfill’, ‘bfill’, ‘pad’, ‘ffill’, None}, default None, 填充方法
        inplace: 如果为Ture, 则对原对象操作, 返回None
        limit: 限制填充的个数
        a dict of item->dtype of what to downcast if possible,
        or the string ‘infer’ which will try to downcast(向下转换) to an appropriate equal type
        (eg. float64 to int64 if possible)
        """
        df = DataFrame({'name': ['a', 'b', np.nan], 'age': [np.nan, '2', 3]})
        df1 = DataFrame({'name': ['aa', 'bc', 'cc'], 'age': ['11', '22', '33']})
        print(df.fillna(value="fillna"))
        print(df.fillna(value={'name': 'name fill', 'age': 'age fill'}))
        # 如果值为NaN的话, 一一对应的填坑
        print(df.fillna(df1))

    def groupby(self):
        """
        groupby(self, by=None, axis=0, level=None, as_index=True, sort=True, group_keys=True, squeeze=False, **kwargs)
        by : mapping, function, str, or iterable
            Used to determine the groups for the groupby.
            If ``by`` is a function, it's called on each value of the object's index.
            If a dict or Series is passed, the Series or dict VALUES will be used to determine the groups
                (给出待分组轴上的值与分组名之间的对应关系, 即根据index进行合并, 然后进行series/dict分组)
            If an ndarray is passed, the values are used as-is determine the groups.
            A str or list of strs may be passed to group by the columns in ``self``

        axis : int, default 0(按列分组), 1(按行分组, 用的较少)
        sort : bool, 默认为False, 是否对key排序
        as_index : boolean, default True
            如果groupby分组时有多个group key, 集成后数据默认含有层级索引, 可以通过 "as_index=False" 参数来去掉多级索引
            For aggregated(聚合的) output(如取分组中的最大值等), return object with group labels as the index
            Only relevant for DataFrame input.(该参数只对DataFrame有效)
            as_index=False is effectively(有效的) "SQL-style" grouped output
        """
        df = DataFrame({'name': ['b', 'b', 'a', 'a'], 'a': [1, 2, 3, 4], 'b': [1, 1, 2, 2], 'c': ['a', 'a', 'b', 'b']})
        # 根据 name 进行分组
        gb1 = df.groupby(by='name')
        gb2 = df.groupby(by='name', as_index=False)  # ax_index 只有对于聚合之类的方法才会显现出作用
        print(gb1)
        # groups属性是一个字典, key=分组的key, value=分组后的df
        print(gb1.groups)
        # 获取 key='a' 的分组
        print(gb1.get_group('a'))

        print(gb1.sum())
        # reset_index() 去掉组名构成的多级索引
        print(gb1.sum().reset_index())
        # gb2.sum()等价于 gb1.sum().reset_index()
        print(gb2.sum())

        # 一次应用多个函数, 多个函数作用于每一列
        print(gb1.agg([np.max, np.min, np.sum]))
        # 此时是多级索引
        print(gb1.agg([np.max, np.min, np.sum]).reset_index())

        # 对DataFrame不同列应用不同的函数, 不操作的列会舍弃
        print(gb1.agg({'a': np.max, 'b': np.min}))

    def groupby1(self):
        df = DataFrame({'key1': ['a', 'a', 'b', 'b', 'a'],
                        'key2': ['one', 'two', 'one', 'two', 'one'],
                        'data1': [1, 2, 3, 4, 5],
                        'data2': [5, 4, 3, 2, 1]})
        # 按key1进行分组, 并计算data1列的平均值, 以下两种方式等价
        # 根据index 连接 两个series, 然后根据df['key1']分组
        gb = df['data1'].groupby(df['key1'])
        print(gb.max().reset_index())
        print(df[['data1', 'key1']].groupby(by='key1', as_index=False).max())

        # 没有key2, 因为str不能求平均值, 所以被排除了
        print(df.groupby('key1').mean())

    def max_min(self):
        """ 返回最小值和最大值对应的index, 如果多个数值都是最大值或最小值, 则返回第一次出现对应的索引值 """
        df = self.df
        # df中不能出现非数值类型, 不然 idx_* 会抛异常
        df.pop('name')
        # axis=0, 求的是每一列, axis=1, 每一行
        print(df)
        print(df.idxmax())
        print(df.idxmin())
        # 根据columns中, 值最大/小的 n行
        print(df.nlargest(n=1, columns='height'))
        print(df.nsmallest(n=1, columns='height'))

    def iter(self):
        """ 迭代pandas对象通常会比较慢。所以尽量避免迭代操作, 当迭代进行时永远不要有修改操作"""
        df = self.df
        for col in df:
            print(col)

        for index, s in df.iterrows():  # index, Series(index, 每一行)
            print(index, type(s))

        # 这种方法比iterrows()快, 大多数情况下推荐使用此方法
        for l in df.itertuples():  # namedtuples(每一行)
            print(type(l), l, l.age)

        for i, s in df.iteritems():  # (column name, Series(每一列))
            print(i, type(s), s)

    def mean(self):
        df = self.df
        # 计算每一列的平均值, 沿着 index 计算
        print(df.mean(0))
        # 计算每一行的平均值, 沿着 columns 计算
        print(df.mean(axis=1))

    def merge(self):
        """
        merge(right, how='inner', on=None, left_on=None, right_on=None, left_index=False, right_index=False, sort=False,
              suffixes=('_x', '_y'), copy=True, indicator=False, validate=None)
        A.merge(B)
        how:
            left: 产生表A的完全集, 而B表中匹配的则有值, 没有匹配的则以NaN值取代 (left outer join, 左外连接)
            right: 产生表B的完全集, 而A表中匹配的则有值, 没有匹配的则以NaN值取代 (right outer join, 右外连接)
            inner: AB的交集 (inner join, 内部连接,  inner 交集)
            outer: AB的并集 (full outer join, 全外连接, outer, 并集)

        on join的column名
        left_on = A 的column名
        right_on = B 的column名
        sort bool, 是否排序
        suffixes, 如果AB中有同名的column名, 添加的后缀
        left_index/right_index 使用左/右侧DataFrame中的索引作为连接键
        """
        a = DataFrame({'id': [1, 2], 'age': [1, 2]})
        b = DataFrame({'id': [1, 3], 'name': ['a', 'c']})
        c = DataFrame({'cid': [1, 3], 'name': ['a', 'c']})
        print(a.merge(b, how='left', on='id'))
        print(a.merge(b, how='right', on='id'))
        print(a.merge(b, how='inner', on='id'))
        # id 和 cid 都会出现在结果中
        print(a.merge(c, how='outer', left_on='id', right_on='cid'))

    def merge_index(self):
        df1 = pd.DataFrame({'key': ['a', 'b', 'a', 'a', 'b', 'c'], 'value': range(6)})
        df2 = pd.DataFrame({'score': [100, 99]}, index=['a', 'b'])
        # df2的索引用作连接键
        print(pd.merge(df1, df2, left_on='key', right_index=True, how='left'))

    def pipe(self):
        """
        DataFrame和Series当然能够作为参数传入方法. 然而,如果涉及到多个方法的序列调用,推荐使用pipe().看一下例子：
        f, g 和h是三个方法,接收DataFrame对象,返回DataFrame对象
        f(g(h(df), arg1=1), arg2=2, arg3=3)
        等价写法:
        (df.pipe(h).pipe(g, arg1=1).pipe(f, arg2=2, arg3=3))
        注意 f g h三个方法中DataFrame都是作为第一个参数.
        如果DataFrame作为第二个参数呢？方法是为pipe提供(callable, data_keyword),pipe会自动调用DataFrame对象.
        """
        pass

    def rank(self):
        """
        DataFrame.rank(axis=0, method='average', numeric_only=None, na_option='keep', ascending=True, pct=False)
        该方法用来排名, 排名顺序为1 ~ n,
        默认情况下, 相等的值 等于 他们排名的平均值, 如相同的两个值排名分别为1,2 则这两个值的排名为1.5
        参数的作用
        axis: {0 or 'index',1 or 'columns'} default 0,
            0: 沿着index方向排名, 即给每一列排名
            1: 沿着columns方向排名, 即给每一行排名

        method: {'average','min','max','first','dense'}
        指定排名时用于破坏平级关系的method选项  *** (注 : 值相同的位同一个分组) ***
            'average'	默认: 在相等分组中,为各个值分配平均排名
            'min'	使用整个整个分组的最小排名
            'max'	使用整个分组的最大排名
            'first'	按值在原始数据中的出现顺序分配排名
            'dense'	与'min'类似,但是排名每次只会增加1, ***即并列的数据只占据一个名次***
        
        ascending 是否为升序, 默认为True
        
        na_option用于处理NaN值
            keep: 将NA值保留在原来的位置
            top: 如果升序,将NA值排名第一
    　　    bottom: 如果降序,将NA值排名第一
        pct  名次是否为百分数
        """
        df = DataFrame({'name': list('abc'), 'age': [10, 10, 30], 'height': [1, 3, 2]})
        # 沿着 columns 排名, 即给某一行中的数据排序, 然后排名
        print(df.rank(axis=1, pct=True))
        # 按照降序排名
        print(df.rank(axis=1, ascending=False))
        # 排名选分组中最大的
        print(df.rank(axis=1, method='max'))
        # 相同的数值, 只占用一个名次
        print(df.rank(axis=0, method='dense'))
        print(df.rank(axis=0, method='dense', pct=True))

    def reindex(self):
        """ 根据原有的df, 重新选择数据 (对loc的封装), 不存在的标签值为NaN """
        df = self.df
        print(df.reindex(columns=['name', 'age'], index=[0, 2]))

    def reindex_like(self):
        """ 使得原来对象的label和传入的对象一样( 结构一样 ) """
        df = DataFrame({'name': ['a'], 'address': ['bj']})
        print(df.reindex_like(self.df))

    def rename(self):
        """重命名 index / columns"""
        df = self.df
        # index/columns :  dict-like or function
        print(df.rename(index=lambda x: x*2, columns={'name': 'NAME'}))
        print(df.rename(index={1: '11'}, columns={'name': '外号'}))
        df.index = df.index.map(lambda x: 'index %s' % x)
        print(df)

    def reset_index(self):
        """
        reset_index(self, level=None, drop=False, inplace=False, col_level=0, col_fill=''):
        drop: 是否丢弃索引, 默认不丢弃, 如果不丢弃的话, 会将index插入到columns中
        """
        df = DataFrame({'a': [1, 1, 3, 3], 'b': range(4)}, index=[1, 1, 1, 1])
        print(df.reset_index())
        print(df.reset_index(drop=True))
        gb = df.groupby(by='a').max()
        print(gb)
        print(gb.reset_index())
        print(gb.reset_index(drop=True))

    def sort_index(self):
        """ 按照index排序, 在排序时, 任何缺失值默认都会被放到Series的末尾(不管是升序还是降序) """
        df = self.df
        print(df)
        print(df.sort_index(ascending=False))  # 行index 排序
        print(df.sort_index(axis=1, ascending=False))  # 列columns 排序

    def sort_values(self):
        """ 按照值排序, 在排序时, 任何缺失值默认都会被放到Series的末尾(不管是升序还是降序) """
        df = self.df
        # 根据'age'的值, 给每一列排序
        print(df.sort_values(by=['age'], ascending=False))

    def select_dtypes(self):
        """
        Return a subset of a DataFrame including/excluding columns based on their ``dtype``
        include, exclude : A selection of dtypes or strings to be included/excluded. At least one of these parameters
                           must be supplied.
        """
        df = DataFrame({'a': [1, 2], 'b': [True, False], 'c': [1.0, 2.0]})
        print(df.dtypes)
        # 选择 type(columns) == include 类型的列
        print(df.select_dtypes(include=[np.float64, bool]))
        # 选择 type(columns) != exclude 类型的列
        print(df.select_dtypes(exclude=['float64']))

    def sign(self):
        """ 正数为1 负数为-1, 0还是0 """
        df = DataFrame({'a': [0, -1], 'b': [2, -2]})
        print(np.sign(df))

    def stack(self):
        """
        stack：将数据的列 "旋转" 为行
        unstack：将数据的行 "旋转" 为列
        """
        df = self.df
        s1 = df.stack(dropna=False)
        s2 = df.unstack()
        for s in (s1, s2):
            print(type(s))
            print(s)

    def test(self):
        df = DataFrame({'a': [1, 1, 3, 3], 'b': [1, 2, 1, 2], 'c': [1, 2, 2, 1]})
        # print(df)
        # print(df.groupby(by='a').agg({'c': max, 'b': lambda x: x}).reset_index())
        df = df.append({'a': 10, 'c': 4}, ignore_index=True)
        print(df)


if __name__ == '__main__':
    p = dataframe()
    # p.init()
    # p.base()
    # p.correct()
    # p.delete()
    # p.operate()
    # p.get()
    # p.query1()
    # p.query2()
    # p.append()
    # p.astype()
    # p.agg()
    # p.align()
    # p.apply()
    # p.applymap()
    # p.combine_first()
    # p.combine()
    # p.drop()
    # p.drop_duplicates()
    # p.groupby()
    # p.groupby1()
    # p.fillna()
    # p.max_min()
    # p.iter()
    # p.dropna()
    # p.mean()
    # p.merge()
    # p.merge_index()
    p.rank()
    # p.reindex()
    # p.reindex_like()
    # p.rename()
    # p.reset_index()
    # p.sort_index()
    # p.sort_values()
    # p.select_dtypes()
    # p.sign()
    # p.stack()
    # print(p.test())
