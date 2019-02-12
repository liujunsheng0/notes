#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
装饰器和类
"""


class Decorator(object):
    def __call__(self, func):
        """ __call__ 解释 https://blog.csdn.net/lis_12/article/details/54631368 """
        def wrapper(*args, **kwargs):
            self.record(func)
            return func(*args, **kwargs)
        return wrapper

    @classmethod
    def record(cls, f):
        print('run func name = %s' % f.__name__)


# 用类装饰函数
@Decorator()
def job(a, b):
    return a + b

print(job(1, 2))


def decorator(c):
    def wrapper(*args, **kwargs):
        """ 这里可以做很多事... """
        def set_attr(self, k: str, v):
            """ 属性值都变为大写 """
            self.__dict__[k.upper()] = v
        c.__setattr__ = set_attr
        obj = c(*args, **kwargs)
        return obj
    return wrapper


# 用函数装饰类
@decorator
class Job(object):
    def __init__(self, a: str='a', b: str='b'):
        self.a = a
        self.b = b

print(Job().__dict__)


def decorator(f):
    def wrapper(*args, **kwargs):
        print("run func=%s" % f.__name__)
        return f(*args, **kwargs)
    return wrapper


class Job(object):
    # 函数装饰类中的方法
    @decorator
    def job_method(self):
        pass

Job().job_method()
