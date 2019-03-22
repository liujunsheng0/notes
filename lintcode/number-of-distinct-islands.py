#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
不同岛屿的个数 https://www.lintcode.com/problem/number-of-distinct-islands/description

给定一个由0和1组成的非空的二维网格，一个岛屿是指四个方向（包括横向和纵向）都相连的一组1（1表示陆地）。
你可以假设网格的四个边缘都被水包围。 找出所有不同的岛屿的个数。如果一个岛屿与另一个岛屿形状相同（不考虑旋转和翻折），
我们认为这两个岛屿是相同的

  [
    [1,1,0,0,1],
    [1,0,0,0,0],
    [1,1,0,0,1],
    [0,1,0,1,1]
  ]
输出: 3
解释:
  11   1    1
  1        11
  11
   1

输入:
  [
    [1,1,0,0,0],
    [1,1,0,0,0],
    [0,0,0,1,1],
    [0,0,0,1,1]
  ]
输出: 1
"""


class Solution:
    """
    @param grid: a list of lists of integers
    @return: return an integer, denote the number of distinct islands
    """

    def numberofDistinctIslands(self, grid):
        m = len(grid)
        if m < 1:
            return 0
        n = len(grid[0])
        if n < 1:
            return 0
        ans = set()
        for i in range(m):
            for j in range(n):
                if grid[i][j] != 1:
                    continue
                ans.add(self.bfs(grid, m, n, i, j))
            # end for
        # end for
        return len(ans)

    def bfs(self, grid, m, n, x, y):
        path = ''
        grid[x][y] = 0
        if y + 1 < n and grid[x][y + 1] == 1:
            path += "r" + self.bfs(grid, m, n, x, y + 1)
        if x + 1 < m and grid[x + 1][y] == 1:
            path += "d" + self.bfs(grid, m, n, x + 1, y)
        if x > 0 and grid[x - 1][y] == 1:
            path += "u" + self.bfs(grid, m, n, x - 1, y)
        if y > 0 and grid[x][y - 1] == 1:
            path += "l" + self.bfs(grid, m, n, x, y - 1)
        return path if path else ';'  # 这里很重要

        # 如果不加最后的;
        # 1 1  与 1 1  的结果是一样的
        # 1         1

l = [[0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1], [0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1], [0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0], [0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0], [0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1], [0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0]]

print(Solution().numberofDistinctIslands(l))
