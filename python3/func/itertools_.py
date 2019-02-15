#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
https://juejin.im/post/5af56230f265da0b93485cca
"""

from itertools import (count, cycle, repeat, accumulate)
import itertools


def get_item_from_iter(iter_obj, times=10) -> list:
    ans = []
    for i in iter_obj:
        if times <= 0:
            return ans
        times -= 1
        ans.append(i)
    # end for
    return ans


class Infinite(object):
    """可以无限产出的迭代器"""

    def count(self):
        """
        无限生成数
        start, [step]	start, start+step, start+2*step, ...	count(10) --> 10 11 12 13 14 ...
        """
        print(get_item_from_iter(count(1, 3)))

    def cycle(self):
        """
        重复返回给定序列中的元素
        p0, p1, ... plast, p0, p1, ...
        cycle('ABCD') --> A B C D A B C D ...
        """
        print(get_item_from_iter(cycle('abc'), 6))

    def repeat(self):
        """	返回某个数N次, 默认为无数次"""
        print(get_item_from_iter(repeat(1), 5))
        print(get_item_from_iter(repeat(1, 3), 5))

    @staticmethod
    def test():
        o = Infinite()
        o.count()
        o.cycle()
        o.repeat()


class Finite(object):
    """ 有限迭代器 """
    def accumulate(self):
        """
        创建一个迭代器, 默认返回累计的和或其他二元函数的累计结果
        即f(0)=a[0], f(1)=func(f(0), a[1]), f(2)=func(f(1), a[2]), ... , f(i)=func(f(i-1), a[i]) i>0
        如果提供了 func, 它应该是两个参数的函数.
        iterable 的元素可以是任何能够被接受为 func 参数的类型.
        如果传入的迭代器为空, 则输出迭代器也将为空
        """
        # 1, 1+2, 1+2+3, 1+2+3+4, 1+2+3+4+5
        print(list(accumulate([1, 2, 3, 4, 5])))
        # 1, 1*2, 1*2*3, 1*2*3*4, 1*2*3*4*5
        print(list(accumulate([1, 2, 3, 4, 5], func=lambda x, y: x * y)))
        print(list(accumulate([1])))

    def chain(self):
        """
        用于将连续序列作为单个序列进行处理。
        创建一个迭代器，它从第一个迭代器中返回元素，直到它耗尽，然后继续下一个迭代器，直到所有迭代器都耗尽。
        """
        print(list(itertools.chain(range(3), range(5, 10))))

    def dropwhile(self):
        """
        dropwhile(predicate, iterable),
        将 iterable 中的元素依次交给 predicate 处理，直到 predicate(elem) 的值为 False 时，
        返回iterable中剩下的元素
        """
        print(list(itertools.dropwhile(lambda x: x < 5, [1, 2, 6, 2, 1])))

    def groupby(self):
        """
        根据 key 给 iterable 中的元素分组，如果 key 为 None，则依据元素自身分组。
        ***注意：必须先排序后才能分组，因为 groupby 是通过比较相邻元素来分组的***
        """
        for k, v in itertools.groupby([1, 4, 7, 2, 5, 1], lambda x: x % 3):
            print(k, list(v))
        # 1 [1, 4, 7]
        # 2 [2, 5]
        # 1 [1], 因为1和前面的1, 4, 7不相邻

    def starmap(self):
        """
        把 iterable 中的元素传递给 function(*elem) 处理，然后返回结果
        类似于
        def starmap(function, iterable):
            # starmap(pow, [(2,5), (3,2), (10,3)]) --> 32 9 1000
            for args in iterable:
                yield function(*args)
        """
        func = lambda *args: sum(args)
        print(list(itertools.starmap(func, ((1, 2), (3, 4), (5, 6)))))
        print(list(itertools.starmap(max, ((1, 2), (3, 4), (5, 6)))))

    @staticmethod
    def test():
        o = Finite()
        o.accumulate()
        o.chain()
        o.dropwhile()
        o.groupby()
        o.starmap()


class Combination(object):
    """ 组合迭代器 """
    def product(self):
        """
        大致相当于生成器表达式中的嵌套 for 循环。例如，product(A, B) 与 ((x,y) for x in A for y in B) 返回的结果相同。
        repeat=1 关键字参数指定重复次数。例如，product(A, repeat=4) 意味着与 product(A, A, A, A)
        """
        print(list(itertools.product('abc', '123')))

    def permutations(self):
        """
        排列, itertools.permutations(iterable, r=None)
        将 iterable 中的元素按照 r 个 r 个排列, 不会去重. 如果未指定 r 或者是 None，那么 r 默认为 iterable 的长度。
        """
        print(list(itertools.permutations('123')))
        print(list(itertools.permutations('123', 2)))
        # 不会去重
        print(list(itertools.permutations('122', 2)))

    def combinations(self):
        """
        **排列顺序不可变**，元素不重复（同一个组合内不重复）。
        """
        print(list(itertools.combinations('123', 2)))  # [('1', '2'), ('1', '3'), ('2', '3')]
        print(list(itertools.combinations('122', 2)))  # [('1', '2'), ('1', '2'), ('2', '2')]

    @staticmethod
    def test():
        o = Combination()
        o.product()
        o.permutations()
        o.combinations()

if __name__ == '__main__':
    Infinite.test()
    Finite.test()
    Combination.test()
