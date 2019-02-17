#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
完美平方 https://www.lintcode.com/problem/perfect-squares/description
给一个正整数 n, 请问最少多少个完全平方数(比如1, 4, 9...)的和等于n。

样例 1:

输入: 12
输出: 3
解释: 4 + 4 + 4
样例 2:

输入: 13
输出: 2
解释: 4 + 9
"""


class Solution:
    """
    @param n: a positive integer
    @return: An integer
    """
    def numSquares(self, n):
        # write your code here
        if n < 2:
            return 1
        dp = [n] * (n + 1)
        dp[0], dp[1], dp[2] = 0, 1, 2
        for i in range(3, n + 1):
            for j in range(1, i):
                if i - j ** 2 < 0:
                    break
                dp[i] = min(dp[i - j ** 2] + 1, dp[i])
                # end for
        # end for
        return dp[-1]

print(Solution().numSquares(12))