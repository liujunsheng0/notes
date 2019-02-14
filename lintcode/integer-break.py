#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
整数拆分 https://www.lintcode.com/problem/integer-break/description
给定一个正整数 n ，将其拆分成至少两个正整数之和，并且使这些整数之积最大。返回这个最大乘积。
你可以认为 n 不小于 2 ，并且不大于 58。
给定 n = 2，返回 1 (2 = 1 + 1)；给定 n = 10，返回 36 (10 = 3 + 3 + 4)。
"""


class Solution:
    """
    @param n: a positive integer n
    @return: the maximum product you can get
    """
    def integerBreak(self, n):
        if n < 2:
            return 0
        dp = [0] * (n + 1)
        dp[2] = 1
        for i in range(3, n + 1):
            for j in range(1, i):
                dp[i] = max(dp[i], max(i - j, dp[i - j]) * j)
        return dp[n]

print(Solution().integerBreak(10))
