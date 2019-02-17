#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
删除数字 https://www.lintcode.com/problem/delete-digits/description

给出一个字符串 A, 表示一个 n 位正整数, 删除其中 k 位数字, 使得剩余的数字仍然按照原来的顺序排列产生一个新的正整数。
找到删除 k 个数字之后的最小正整数。

N <= 240, k <= N

样例 给出一个字符串代表的正整数 A 和一个整数 k, 其中 A = 178542, k = 4 返回一个字符串 "12"
"""


from itertools import dropwhile


class Solution:
    """
    @param A: A positive integer which has N digits, A is a string
    @param k: Remove k digits
    @return: A string
    """
    def DeleteDigits(self, A, k):
        """贪心, 一位一位的删除, 寻找最小, 注意开头为0!!!"""
        if len(A) <= k:
            return ""
        while k > 0:
            k -= 1
            tmp = A[1:]
            for i in range(1, len(A)):
                tmp = min(tmp, A[:i] + A[i + 1:])
            # end for
            A = tmp
        # end while
        return ''.join(dropwhile(lambda _: _ == '0', A))

print(Solution().DeleteDigits('43021', 2))
