#!/usr/bin/python3.7
# -*- coding: utf-8 -*-

"""函数相关小技巧"""
import functools


def keyword_func():
    # 只接受关键字参数, 必须以关键字的形式赋值
    def func(*args, arg1: int, arg2: int = 0) -> int:
        print(f"args={args}, arg1={arg1}, arg2={arg2}")
        return arg1 + arg2

    func(1, 2, 3, arg1=4)
    func(1, 2, 3, arg2=4, arg1=5)


# 让带有N个参数的可调用对象以较少的参数形式调用, 可以与lambda函数相结合使用
def func_partial():
    f = lambda a, b, c, d: sum([a, b, c, d])
    print(f(*range(4)))
    # 指定一部分参数的值, 返回一个新的可调用的参数
    f_partial = functools.partial(f, 1, 2)
    # f(3, 4)等价于func(1, 2, 3 ,4), f(5, 6)等价于func(1, 2, 5 ,6)
    print(f_partial(3, 4), f_partial(5, 6))


# 扩展函数中的某个闭包, 允许它能访问和修改函数的内部变量
def closure():
    def _closure():
        """
        通常来说, 闭包的内部变量对于外界来讲是完全隐藏的, 但是, 可以通过编写访问函数并将其作为函数属性绑定到闭包上来实现这个目的
        """
        v = 0

        def func():
            print(f"v = {v}")

        def get_v():
            return v

        def set_v(value):
            # nonlocal 声明可以让我们修改内部变量的值, 去掉nonlocal, 无法修改外面 v 的值
            nonlocal v
            old_v = v
            v = value
            return f"{old_v}->{v}"

        setattr(func, 'get', get_v)
        setattr(func, 'set', set_v)
        return func
    # end _closure
    s = _closure()
    print(s.set(1), s())
    print(s.set(2), s())


if __name__ == '__main__':
    # keyword_func()
    # func_partial()
    closure()
