#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
前K个偶数长度的回文数和 https://www.lintcode.com/problem/sum-of-first-k-even-length-palindrome-numbers
给一整数 k, 得出前 k 个偶数长度的回文数和. 这里的偶数长度是指一个数字的位数为偶数.

输入:  k = 3
输出: 66
解释:
11 + 22 + 33  = 66 (前三个偶数长度的回文数和)
样例2
输入:  k = 10
输出: 1496
解释:
11 + 22 + 33 + 44 + 55 + 66 + 77 + 88 + 99 + 1001 = 1496
"""


"""
f(1) = 11
f(2) = 22
...
f(9) = 99
f(10) = 1001
f(11) = 1111
...
f(99) = 9999
f(100) = 100001
可以看出来，第n个数的值，就是将n作为字符串str，翻转之后得到revstr，然后将str和revstr拼接，再转换为整数，就是所需要的结果
"""


class Solution:
    """
    @param k: Write your code here
    @return: the sum of first k even-length palindrome numbers
    """
    def sumKEven(self, k):
        return sum([int(str(i) + str(i)[::-1]) for i in range(1, k + 1)])

print(Solution().sumKEven(10))
