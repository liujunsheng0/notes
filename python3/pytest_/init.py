#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import inspect


"""
pytest定义了类似于unittest中setup和teardown方法, 也可以使用固件实现类似的功能

    模块的固定装            setup_module   teardown_module
    类的固定装置            setup_class    teardown_class
    函数的固定装置          setup          teardown (注意作用域)
    module级别方法装置      setup_function teardown_function
    class级别方法装置       setup_method   teardown_method
    pytest_fixtrue.py

    def setup_module()
    def teardown_module()
    def setup_function()
    def teardown_function()
    def module_function()
    class class_name:
        def setup()
        def teardown()
        def setup_class()
        def teardown_class()
        def setup_method()
        def teardown_method()
        def class_function()
"""


def setup_module():
    print(inspect.stack()[0][3])


def teardown_module():
    print(inspect.stack()[0][3])


def setup_function():
    print(inspect.stack()[0][3])


def teardown_function():
    print(inspect.stack()[0][3])


# setup, teardown 是指在模块, 函数, 类开始运行以及结束运行时执行一些动作
# 在此定义的不会作用于类中的测试案例, 如果需要作用于类中的测试案例需要在类中重新定义
def setup():
    print(inspect.stack()[0][3])


def teardown():
    print('\n', inspect.stack()[0][3], sep='')


def test_1():
    pass


def test_2():
    pass


class Test(object):
    # 此处未定义setup和teardown, 外边的setup和teardown函数不会起作用
    def setup(self):
        print("class", inspect.stack()[0][3])

    def teardown(self):
        print("\nclass", inspect.stack()[0][3])

    def setup_class(self):
        print("class", inspect.stack()[0][3])

    def teardown_class(self):
        print("class", inspect.stack()[0][3])

    def setup_method(self):
        print("class", inspect.stack()[0][3])

    def teardown_method(self):
        print("class", inspect.stack()[0][3])

    def test_1(self):
        pass

    def test_2(self):
        pass


"""
$ pytest -s init.py
结果如下:
setup_module

setup_function
setup
.
teardown
teardown_function

setup_function
setup
.
teardown
teardown_function

class setup_class

class setup_method
class setup
.
class teardown
class teardown_method

class setup_method
class setup
.
class teardown
class teardown_method

class teardown_class

teardown_module
"""