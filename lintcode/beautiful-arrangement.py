#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
美丽的排列 https://www.lintcode.com/problem/beautiful-arrangement-ii/description
给两个整数 n 和 k，你需要构造一个包含 n 个不同正整数的列表，范围从 1 到 n 并遵守以下要求：
假设这个列表是[a1，a2，a3，...，an]，并且列表[| a1 - a2 |，| a2 - a3 |，| a3 - a4 |，...，| an-1 - an |]恰好具有 k 个不同的整数。
如果有多个答案，返回任意一个即可。

n 和 k 的范围为 1 <= k < n <= 10^4.

输入: n = 3, k = 1
输出: [1, 2, 3]
解释: [1, 2, 3] 在范围 1 到 3 内有三个不同的正整数。 而[1,1]恰好有1个不同的整数：1。

输入: n = 3, k = 2
输出: [1, 3, 2]
解释: [1, 3, 2] 在范围 1 到 3 内有三个不同的正整数, 以及 [2, 1] 恰好有2个不同的整数： 1 and 2.
"""


class Solution:
    """
    @param n: the number of integers
    @param k: the number of distinct integers
    @return: any of answers meet the requirment
    """
    def constructArray(self, n, k):
        if k >= n or n < 1:
            return []
        return list(range(1, n - k + 1)) + [n-k + i//2 if i % 2 == 0 else n - i//2 for i in range(1, k + 1)]


r = Solution().constructArray(100, 99)
visited = set()
for idx, v in enumerate(r[1:]):
    visited.add(abs(v - r[idx]))
print(visited)
