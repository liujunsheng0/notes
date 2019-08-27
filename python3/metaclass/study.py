#!/usr/bin/python3.7
# -*- coding: utf-8 -*-


def call_sequence():
    """ 元类, 调用顺序 """

    class Metaclass(type):
        def __init__(cls, *args, **kwargs):
            print("Metaclass __init__", args, kwargs)
            super().__init__(*args, **kwargs)

        def __call__(cls, *args, **kwargs):
            print("Metaclass __call__", args, kwargs)
            return super().__call__(*args, **kwargs)

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
    # call_order()
    single()
