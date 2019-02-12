#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
中文翻译: https://www.jianshu.com/p/161364dd0acf

参数的意义:
    NaN : 即"非数字" not a number, 在pandas中, 它用于表示缺失或NA值,
    NA : not available
    axis=0(index, 默认), axis=1(columns)
        官方：It specifies the axis along which the means are computed. 沿着轴操作.
        默认axis=0,也就是竖轴,操作的结果是行数的增加或减少
        axis=1,也就是横轴,操作的结果每一列属性增加或减少

    level   用于具有层次索引的对象, index和columns可能有多重, levels就是用来指定使用哪一层index和columns的
            https://stackoverflow.com/questions/45235992/what-are-levels-in-a-pandas-dataframe

    skipna  计算过程中是否剔除缺失值, skipna默认值一般为True
    inplace: 直接修改调用者, 不产生副本


pandas支持三种不同的索引方式：
    .loc 基于label进行索引, 当然也可以和boolean数组一起使用
        '.loc'接受的输入
            1. 一个单独的label, 比如5 'a', 注意, 这里的5是index值, 而不是整形下标
            2. label列表或label数组, 比如['a', 'b', 'c']
    .iloc 是基本的基于整数位置(从0到axis的length-1)的, 当然也可以和一个boolean数组一起使用. 当提供检索的index越界时会有IndexError错误,注意切片索引(slice index)允许越界.
    .ix 支持基于label和整数位置混合的数据获取方式.默认是基本label的. .ix是最常用的方式,它支持所有.loc和.iloc的输入.如果提供的是纯label或纯整数索引,我们建议使用.loc或 .iloc

方法的作用:(所有需要沿着坐标轴计算的方法, 默认axis=0, 即将方法应用到每一列数据上)
    count	沿着坐标轴统计非空的行数
    sum	    沿着坐标轴取加和
    mean	沿着坐标轴求均值
    mad	    沿着坐标轴计算平均绝对偏差
    median	沿着坐标轴计算中位数
    min	    沿着坐标轴取最小值
    max 	沿着坐标轴取最大值
    mode	沿着坐标轴取众数
    abs	    计算每一个值的绝对值
    prod	沿着坐标轴求乘积
    std	    沿着坐标轴计算标准差
    var	    沿着坐标轴计算无偏方差
    sem	    沿着坐标轴计算标准差
    skew	沿着坐标轴计算样本偏斜
    kurt	沿着坐标轴计算样本峰度
    quantile    沿着坐标轴计算样本分位数,单位%
    cumsum	沿着坐标轴计算累加和
    cumprod	沿着坐标轴计算累积乘
    cummax	沿着坐标轴计算累计最大
    cummin	沿着坐标轴计算累计最小
    argmax, argmin 取得最大(小)值的索引位置(整数)
    idxmax, idxmin 取得最大(小)值的索引值

"""
