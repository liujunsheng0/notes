#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""函数相关小技巧"""
import functools


# 只接受关键字参数, 必须以关键字的形式赋值
def keyword_func(*args, arg1: int, arg2: int=0) -> int:
    print(args, arg1, arg2)
    return arg1 + arg2


def test_keyword_func():
    keyword_func(1, 2, 3, arg1=4)
    keyword_func(1, 2, 3, arg2=4, arg1=5)


# 让带有N个参数的可调用对象以较少的参数形式调用, 可以与lambda函数相结合使用
def test_func_partial():
    f = lambda a, b, c, d: sum([a, b, c, d])
    print(f(*range(4)))
    # 指定一部分参数的值, 返回一个新的可调用的参数
    f_partial = functools.partial(f, 1, 2)
    # f(3, 4)等价于func(1, 2, 3 ,4), f(5, 6)等价于func(1, 2, 5 ,6)
    print(f_partial(3, 4), f_partial(5, 6))

if __name__ == '__main__':
    test_keyword_func()
    test_func_partial()
