#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
装饰器 - 类装饰函数
"""


class Decorator(object):
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        """ __call__ 解释 https://blog.csdn.net/lis_12/article/details/54631368 """
        print('run func name = %s' % self.function.__name__)
        return self.function(*args, **kwargs)


# 用类装饰函数, job = Decorator(job), job() 相当于调用类Decorator的实例
@Decorator
def job(a, b):
    return a + b

# 等价于job不加装饰器时, Decorator(job)(1, 2)
# print(Decorator(job)(1, 2))
print(job(1, 2))
