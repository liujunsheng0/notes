#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
装饰器-函数装饰函数, 最常见
"""

from time import sleep
from datetime import datetime


# 无参数的装饰器
# 利用装饰器记录job函数的执行时间
def record_runtime(f):
    def wrapper(*args, **kwargs):
        start = datetime.now().timestamp()
        r = f(*args, **kwargs)
        print('run func=%s run time = %s s' % (f.__name__, datetime.now().timestamp() - start))
        return r
    return wrapper


# 等价于 job=record_runtime(job)
@record_runtime
def job(a, b):
    """
    :param a: int
    :param b: int
    :return: sum(a, b)
    """
    sleep(1)
    return a + b

print(job(1, 2))


# 带参数的装饰器
# 加个开关, 控制是否打印运行时间的装饰器
def record_runtime(is_print: bool=True):
    def record_runtime_(f):
        def wrapper(*args, **kwargs):
            start = datetime.now().timestamp()
            print(args, kwargs, f.__name__)
            r = f(*args, **kwargs)
            if is_print:
                print('run func=%s run time = %s s' % (f.__name__, datetime.now().timestamp() - start))
            return r
        return wrapper
    return record_runtime_


@record_runtime(False)
def job(a, b):
    sleep(1)
    return a + b


print(job(2, 3))


class Test(object):
    @record_runtime(False)
    def job1(self, a, b):
        sleep(1)
        return a + b

    @classmethod
    @record_runtime(False)
    def job2(cls, a, b):
        sleep(1)
        return a + b


print(Test().job1(2, 3))
print(Test().job2(2, 3))