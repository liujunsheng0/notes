#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from dateutil.parser import parse

"""
常用类
datetime.date　　　 表示日期的类 常用的属性有year, month, day
datetime.time　　　 表示时间的类 常用的属性有hour, minute, second, microsecond
datetime.datetime　 表示日期时间
datetime.timedelta　表示时间间隔 即两个时间点之间的
"""


def method():
    """ 获取当前时间 """
    now = datetime.now()       # 获取当前日期 + 时间
    print(type(now))
    print('today() == now()', datetime.today() == now)
    print('time =', now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond)
    # 获取周几
    print('weekday()', now.weekday())
    # 时间替换
    print('replace()', now.replace(year=2000, month=1, day=2, hour=3, minute=4, second=5, microsecond=0))
    print('date()', now.date())  # 获取当前日期
    print('time()', now.time())  # 获取当前时间
    print('timestamp()', now.timestamp()) # 返回时间戳
    # 构造时间
    t = datetime(year=2000, month=1, day=2, hour=3, minute=4, second=5)
    print('init()', t)
    # 根据时间戳, 获取时间
    print('timestamp->datetime', datetime.fromtimestamp(t.timestamp()))


def strftime():
    """
    时间 -> 字符串
    %Y  4位数的年份
    %y  2位数的年份(最后两位)
    %m  2位数的月, [01, 12]
    %d  2位数的日, [01, 31]
    %H  小时, 24小时制
    %l  小时, 12小时制
    %M  2位数的分钟
    %S  2位数的秒
    %w  星期几, [0, 6], 0表示星期日
    %U  每年的第几周
    %F  %Y-%m-%d的简写形式
    %D  %m/%d/%y的简写形式

    """
    t = datetime.now()
    print(t.strftime('%Y-%y-%m-%d'))
    print(t.strftime('%F'))


def strptime():
    """
    字符串 -> datetime
    strptime 缺点: 已知时间格式
    parse : 不用知道时间格式
    缺点：实用但不完美的工具, 它会把一些原本不是日期的字符串认作是日期(比如"1111")
    """
    t = '2011-01-03'
    print(datetime.strptime(t, '%Y-%m-%d'))
    print(parse('1111'))
    print(parse('2011-01-03'))
    print(parse('2011/01/03'))
    # 这种格式解析不了, 会报错
    # print(parse('2011年01月03日'))


def timedelta_():
    """ 表示时间差 """
    delta = datetime(2011, 1, 7) - datetime(2011, 1, 8, 8, 15)
    print(delta.days)
    # 2018.1.1 十天以后的日期
    t = datetime(2018, 1, 1) + timedelta(days=10)
    print(t)

if __name__ == '__main__':
    method()
    # timedelta_()
    # strftime()
    # strptime()
