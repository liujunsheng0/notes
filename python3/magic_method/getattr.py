#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
属性查找
如果obj是某个类的实例, 那么obj.name(等价于getattr(obj,'name')), 首先调用__getattribute__, 如果类定义了__getattr__方法, 
那么在__getattribute__抛出 AttributeError 的时候就会调用到__getattr__.

对于描述符(实现了__get__方法的实例)的调用, 发生在__getattribute__内部的.

so, obj = Class(), 那么obj.attr查找顺序如下：
    (1) 如果 attr 在Class或其基类的__dict__(类属性)中, 且 attr 是data descriptor(数据描述符), 那么调用其__get__方法, 否则
    (2) 如果 attr 出现在obj(实例)的__dict__中, 那么直接返回 obj.__dict__['attr'], 否则
    (3) 如果 attr 出现在Class或其基类的__dict__中(安装MRO顺序查找)
        (3.1) 如果attr是non-data descriptor, 那么调用其__get__方法, 否则
        (3.2) class.__dict__['attr']
    (4) 如果Class有__getattr__方法, 调用__getattr__方法, 否则
    (5) 抛出AttributeError
"""

# 描述符 https://blog.csdn.net/lis_12/article/details/53453665


class DataDescriptor(object):
    """ 数据描述符 实现了__get__ 和 __set__方法的实例 """
    def __init__(self, v):
        self.__v = v

    def __get__(self, item, *args, **kwargs):
        return self.__v

    def __set__(self, *args, **kwargs):
        raise AttributeError('only read')


class NonDataDescriptor(object):
    """ 非数据描述符  仅实现了__get__方法的实例 """
    def __init__(self, v):
        self.v = v

    def __get__(self, item, *args, **kwargs):
        return self.v


class Derive(object):
    a = 'a'
    data_descriptor = DataDescriptor('data_descriptor')
    non_data_descriptor = NonDataDescriptor('non_data_descriptor')

    def __init__(self):
        self.a = 1

    def __getattribute__(self, item, *args, **kwargs):
        print('__getattribute__', "%-20s" % item, end=" ")
        return super().__getattribute__(item, *args, **kwargs)

    def __getattr__(self, item, *args, **kwargs):
        """
        usage: 获取不存在的属性时, 不报错, 返回None
        如果类定义了__getattr__方法, 那么在__getattribute__抛出 AttributeError 的时候就会调用到__getattr__
        """
        print('__getattr__', "%-20s" % item, end=" ")
        return None


if __name__ == '__main__':
    obj = Derive()
    print(obj.a)
    print(obj.b)
    print(obj.data_descriptor)
    print(obj.non_data_descriptor)
