#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
https://www.lintcode.com/problem/n-queens-ii/description
根据n皇后问题，现在返回n皇后不同的解决方案的数量而不是具体的放置布局
example:
输入: n=4
输出: 2
解释:
  1:
    0 0 1 0
    1 0 0 0
    0 0 0 1
    0 1 0 0
  2:
    0 1 0 0
    0 0 0 1
    1 0 0 0
    0 0 1 0
"""


class Solution:

    """
    @param n: The number of queens.
    @return: The total number of distinct solutions.
    """
    def totalNQueens(self, n):
        if n < 1:
            return 0
        return self.dfs(n, [0] * n, 0)

    def is_ok(self, queens, idx, v):
        for i, j in enumerate(queens[: idx]):
            if j == v or abs(j - v) == idx - i:
                return False
        return True

    def dfs(self, n, queens, idx):
        if idx >= n:
            return 1
        ans = 0
        for i in range(n):
            if self.is_ok(queens, idx, i):
                queens[idx] = i
                ans += self.dfs(n, queens, idx + 1)
            # end if
        # end for
        return ans

print(Solution().totalNQueens(15))