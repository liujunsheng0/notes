#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
https://www.lintcode.com/problem/n-queens/description
描述
中文
English
n皇后问题是将n个皇后放置在n*n的棋盘上，皇后彼此之间不能相互攻击。
给定一个整数n，返回所有不同的n皇后问题的解决方案。
每个解决方案包含一个明确的n皇后放置布局，其中“Q”和“.”分别表示一个女王和一个空位置。

输入:1
输出:
   [["Q"]]

输入:4
输出:
[
  [".Q..",
   "...Q",
   "Q...",
   "..Q."
  ],
  ["..Q.",
   "Q...",
   "...Q",
   ".Q.."
  ]
]
"""


class Solution1:
    """
    @param: n: The number of queens
    @return: All distinct solutions
    """
    def solveNQueens(self, n):
        if n < 1:
            return []
        ans = []
        tmp = ['.'] * n
        for queen in self.dfs(n, [0] * n, 0):
            addr = []
            for j in queen:
                tmp[j] = 'Q'
                addr.append(''.join(tmp))
                tmp[j] = '.'
            # end for
            ans.append(addr)
        # end for
        return ans

    def is_ok(self, queens, idx, v):
        for i, j in enumerate(queens[: idx]):
            if j == v or abs(j - v) == idx - i:
                return False
        return True

    def dfs(self, n, queens, idx):
        if idx >= n:
            return [list(queens)]
        ans = []
        for i in range(n):
            if self.is_ok(queens, idx, i):
                queens[idx] = i
                ans.extend(self.dfs(n, queens, idx + 1))
            # end if
        # end for
        return ans

print(Solution1().solveNQueens(4))

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


class Solution2:

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

print(Solution2().totalNQueens(4))