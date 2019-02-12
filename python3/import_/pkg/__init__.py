#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
延迟导入: 对于一个很大的模块, 可能只想组件在需要时被加载, 所以可用 延迟导入
延迟加载的真实例子, 见标准库 multiprocessing/__init__.py 的源码.
"""


def a():
    print('import a')
    from .a import a
    return a()


def b():
    print('import b')
    from .b import b
    return b()
