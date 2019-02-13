#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
装饰器 - 函数装饰类

函数装饰器不管是装饰函数、还是装饰类，所遵循的思想原理是一样的，实现的方式也是大同小异。
注意：函数装饰器装饰类，实际上是装饰类的构造函数哦！
"""


def decorator(cls):
    """
    从某种意义上来说, 函数和类是一样的, 因为它们都是对象(python一切皆对象),
    对类和类的实例进行操作
    """

    def wrapper(*args, **kwargs):
        def set_attr(self, k: str, v):
            """ 属性值都变为大写 """
            self.__dict__[k.upper()] = v

        cls.__setattr__ = set_attr
        obj = cls(*args, **kwargs)
        return obj

    return wrapper


# 用函数装饰类
@decorator
class Job(object):
    def __init__(self, a: str = 'a', b: str = 'b'):
        self.a = a
        self.b = b


print(Job(a='1', b='2').__dict__)


# 利用函数装饰类, 构造单例模式
def singleton(cls):
    """
    :param cls: 表示一个类名，即所要设计的单例类名称
    :return:
    """
    instance = {}

    def wrapper(*args, **kwargs):
        # 有这个类的实例就不在创建实例, 直接使用已存在的实例
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        else:
            instance[cls].args = args
            instance[cls].kwargs = kwargs
        return instance[cls]

    return wrapper


@singleton
class Mouse(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

s1 = Mouse(x=0, y=0)
s2 = Mouse(x=1, y=2)
print(s1.kwargs, s2.kwargs)
print(s1 is s2)
print(id(s1), id(s2), sep=', ')
