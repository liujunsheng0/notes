#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
描述  https://www.lintcode.com/problem/edit-distance/description
给出两个单词word1和word2，计算出将word1 转换为word2的最少操作次数。

你总共三种操作方法：
插入一个字符
删除一个字符
替换一个字符

给出 work1="mart" 和 work2="karma"  返回 3

状态转移方程 dp[i][j] = ?

if s[i] == t[j]: dp[i][j] = dp[i - 1][j - 1]

if s[i] != t[j]: 以ab -> bc来计算
    1. dp[i - 1][j] + 1, 即a->bc, 插入c
    2. dp[i][j - 1] + 1, 即ab->bc => abc->bc => ab->c, 即先插入c, abc->bc的编辑距离等于ab->b的编辑距离
    3. dp[i][j]     + 1, 即a->b, 替换
    则: dp[i][j] = min(dp[i - 1][j - 1] + 1, dp[i - 1][j] + 1, dp[i][j] + 1)
"""


class Solution:
    """
    @param word1: A string
    @param word2: A string
    @return: The minimum number of steps.
    """
    def minDistance(self, word1, word2):
        # https://blog.csdn.net/qq_34552886/article/details/72556242
        len1, len2 = len(word1) + 1, len(word2) + 1
        dp = [[0] * len2 for _ in range(len1)]
        for i in range(len1):
            dp[i][0] = i
        for i in range(len2):
            dp[0][i] = i
        for i in range(1, len1):
            for j in range(1, len2):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
                # end if
            # end for
        # end for
        return dp[-1][-1]

print(Solution().minDistance("abc", "bcd"))
