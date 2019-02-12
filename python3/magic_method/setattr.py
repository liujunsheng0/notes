#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
属性赋值
obj = Class(), 那么obj.attr = var, 按照以下顺序：
    (1) 如果Class定义了__setattr__方法，那么调用该方法, 否则
　　(2) 如果 attr 是出现在Class或其基类的__dict__中, 且attr是data descriptor, 那么调用其__set__方法, 否则
　　(3) 等价于调用obj.__dict__['attr'] = var

"""


class Descriptor(object):
    """ 数据描述符 实现了__get__ 和 __set__方法的实例 """
    def __init__(self, v):
        self.v = v

    def __get__(self, item, *args, **kwargs):
        return self.v

    def __set__(self, instance, value, *args, **kwargs):
        print('__set__', instance.__class__.__name__, value)
        self.v = value


class Base1(object):
    descriptor = Descriptor('')

    def __setattr__(self, key, value):
        print('__setattr__ %s->%s' % (key, value))
        # 如果是数据描述符, object.__setattr__() 还会继续调用其 __set__方法
        super().__setattr__(key, value)
        # self.__dict__[key] = value


class Base2(object):
    descriptor = Descriptor('')


if __name__ == '__main__':
    obj1 = Base1()
    obj1.descriptor = 'obj1'
    obj2 = Base2()
    obj2.descriptor = 'obj2'
    print(obj1.descriptor, obj2.descriptor)


