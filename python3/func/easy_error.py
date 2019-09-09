#!/usr/bin/python3.7
# -*- coding: utf-8 -*-

"""函数中的易错点"""


def error_default_parameter():
    def f1(l=[]):
        l.append(1)
        return l
    f1(), f1()
    print(f1())


# 尽量不要使用可变变量作为默认参数, 不然会一堆坑, 如果想用可变变量作为默认参数参考以下
def right_default_parameter(l: list = None):
    if l is None:  # 必须用is, 如果用not l, "", False, (), [], {} 等都会进入此处
        l = []
    l.append(l)
    return l


# 函数中的变量是在执行时绑定
def func_bound_in_run():
    x = 1
    f1 = lambda z: x + z
    x = 2
    f2 = lambda z: x + z
    f3 = [lambda: i for i in range(10)]
    # 此时 x等于2, f3中的任意函数返回值都是9
    print(f1(1), f2(1), [f3[i]() for i in range(10)])  # 3 3 [9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
    x = 4
    print(f1(1), f2(1), [f3[i]() for i in range(10)])  # 5 5 [9, 9, 9, 9, 9, 9, 9, 9, 9, 9]

    # 可利用默认参数解决上述问题, 默认参数只在函数定义时绑定一次
    x = 1
    f1 = lambda z, y = x: z + y
    x = 2
    f2 = lambda z, y = x: z + y
    f3 = [lambda i=i: i for i in range(10)]
    print(f1(1), f2(1), [f3[i]() for i in range(10)])  # 11 21 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


if __name__ == '__main__':
    # error_default_parameter()
    func_bound_in_run()
