#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
描述 https://www.lintcode.com/problem/4-way-unique-paths/description?_from=cat

一个机器人位于一个m*n的网格的左上角。机器人可以在任何时间点移动任何方向，但是每个网格只能达到一次。机器人正试图到达网格右下角。
有多少种可能的独特路径?(只能上下左右的走)
给出 m= 2 和 n= 3,返回 4.
给出 m= 3 和 n= 3,返回 12.
"""


class Solution:
    def __init__(self):
        self.ans = 0

    """
    @param m: the row
    @param n: the column
    @return: the possible unique paths
    """

    def uniquePaths(self, m, n):
        if m < 1 or n < 1:
            return 0
        self.ans = 0
        matrix = [[0] * n for _ in range(m)]
        matrix[0][0] = 1
        self.help(matrix, m, n, 0, 0)
        return self.ans

    def help(self, matrix, m, n, x, y):
        if x == m - 1 and y == n - 1:
            # print(matrix)
            self.ans += 1
            return
        # print(x, y)
        if x + 1 < m and matrix[x + 1][y] == 0:
            matrix[x + 1][y] = 1
            self.help(matrix, m, n, x + 1, y)
            matrix[x + 1][y] = 0
        if x > 0 and matrix[x - 1][y] == 0:
            matrix[x - 1][y] = 1
            self.help(matrix, m, n, x - 1, y)
            matrix[x - 1][y] = 0

        if y + 1 < n and matrix[x][y + 1] == 0:
            matrix[x][y + 1] = 1
            self.help(matrix, m, n, x, y + 1)
            matrix[x][y + 1] = 0
        if y > 0 and matrix[x][y - 1] == 0:
            matrix[x][y - 1] = 1
            self.help(matrix, m, n, x, y - 1)
            matrix[x][y - 1] = 0

print(Solution().uniquePaths(2, 3))
