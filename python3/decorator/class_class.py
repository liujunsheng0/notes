#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
装饰器 - 类装饰类
"""


class Decorator(object):
    def __init__(self, cls):
        self.cls = cls

    def __call__(self, *args, **kwargs):
        """ __call__ 解释 https://blog.csdn.net/lis_12/article/details/54631368 """
        print('run cls name = %s' % self.cls.__name__)
        obj = self.cls(*args, **kwargs)
        # 给被包装的实例增加新成员
        obj.age = 10
        obj.address = 'BeiJing'
        return obj


@Decorator
class Base(object):
    def __init__(self, *args, **kwargs):
        print(args, kwargs)
        self.args = args

    def get_args(self):
        return self.args

print(Base(1, 2, 3, 4).age)