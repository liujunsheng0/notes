#!/usr/bin/python3.7
# -*- coding: utf-8 -*-


def prepare():
    """
    __prepare__: https://www.python.org/dev/peps/pep-3115/
    解释器在调用之前总是检测__prepare__的存在; 如果它不存在, 则使用常规字典. 实现大致如下
    def prepare_class(name, *bases, metaclass=None, **kwargs):
        if metaclass is None:
            metaclass = compute_default_metaclass(bases)
        prepare = getattr(metaclass, '__prepare__', None)
        if prepare is not None:
            return prepare(name, bases, **kwargs)
        else:
            return dict()

    __prepare__返回一个字典对象, 用于存储类成员定义
    __prepare__方法通常被实现为类方法而不是实例方法, 因为它是在创建元类实例(即类本身)之前调用的
    官方demo见PEP-3115
    """
    class Metaclass(type):
        @classmethod
        def __prepare__(mcs, name, bases):
            """used to create the namespace for the class statement(用于创建类的命名空间, 即存放类属性的地方)"""
            return {'prepare': 'prepare'}

    class Test(metaclass=Metaclass):
        pass

    # 因为元类中定义了"prepare"
    print(Test.prepare)


def call_sequence():
    """ 元类, 调用顺序 """

    class Metaclass(type):
        def __init__(cls, name, bases: tuple, attrs: dict):
            """
            :param name: 类名
            :param bases: 父类
            :param attrs: 类属性
            """
            print(f"Metaclass __init__ name={name}, bases={bases}")
            for k, v in attrs.items():
                print(k, v)
            print()
            super().__init__(name, bases, attrs)

        def __new__(mcs, name, bases, attrs):
            """
            :param name: 类名
            :param bases: 父类
            :param attrs: 类属性
            """
            print(f"Metaclass __new__ name={name}, bases={bases}")
            for k, v in attrs.items():
                print(k, v)
            print()
            return super().__new__(mcs, name, bases, attrs)

        def __call__(cls, *args, **kwargs):
            """ 类实例化 """
            print("Metaclass __call__", args, kwargs)
            return super().__call__(*args, **kwargs)

        @classmethod
        def __prepare__(mcs, name, bases):
            """used to create the namespace for the class statement(用于创建类的命名空间, 即存放类属性的地方)"""
            print(f"Metaclass __prepare__ name={name} bases={bases}")
            return {}

    class Test(metaclass=Metaclass):
        def __init__(self, *args, **kwargs):
            print("Test __init__", args, kwargs)
            self.args = args
            self.kwargs = kwargs

        def __new__(cls, *args, **kwargs):
            print("Test __new__", args, kwargs)
            return super().__new__(cls)

    # Test = Metaclass('Test', (), {})
    # Test() = Metaclass('Test', (), {}).__call__(*args, **kwargs)
    #                   (类名, 父类的元组(针对继承的情况,可以为空), 包含属性的字典(名称和值,类属性))
    t = Test(1, a=2)
    print(t.args, t.kwargs)


def single():
    """ 用元类实现单例 """

    class SingleMetaclass(type):
        def __init__(cls, *args, **kwargs):
            super().__init__(*args, **kwargs)
            cls._ins = None

        def __call__(cls, *args, **kwargs):
            if cls._ins is None:
                cls._ins = super().__call__(*args, **kwargs)
            return cls._ins

    class Single1(metaclass=SingleMetaclass):
        def __init__(self):
            print(self.__class__, "init")

    class Single2(metaclass=SingleMetaclass):
        def __init__(self):
            print(self.__class__, "init")

    a = Single1()
    b = Single1()
    c = Single2()
    d = Single2()
    print(a is b, c is d)


if __name__ == '__main__':
    prepare()
    # call_sequence()
    # single()
