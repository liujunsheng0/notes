#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
01矩阵走路问题 https://www.lintcode.com/problem/01-matrix-walking-problem/description

给定一个大小为 n*m 的 01 矩阵 grid，1 是墙，0 是路，你现在可以把 grid 中的一个 1 变成 0，请问从左上角走到右下角是否有路可走？
如果有路可走，最少要走多少步？

样例
给定 a = [[0,1,0,0,0],[0,0,0,1,0],[1,1,0,1,0],[1,1,1,1,0]]，返回 7
将（0,1）处的 `1` 变成 `0`，最短路径如下：
 (0,0)->(0,1)->(0,2)->(0,3)->(0,4)->(1,4)->(2,4)->(3,4) 其他长度为 `7` 的方案还有很多，这里不一一列举。

给定 a = [[0,1,1],[1,1,0],[1,1,0]]，返回 -1
解释：
不管把哪个 `1` 变成 `0`，都没有可行的路径。
"""


class Solution:
    """
    @param grid: The gird
    @return: Return the steps you need at least
    """

    def getBestRoad(self, grid):
        rows, cols = len(grid), len(grid[0])
        q = [(0, 0, 0)]
        used = set((0, 0, 0))
        ans = 0
        while q:
            tmp = []
            for x, y, use1 in q:
                if x == rows - 1 and y == cols - 1:
                    return ans
                for i in (1, -1):
                    if 0 <= x + i < rows:
                        if grid[x + i][y] == 0:
                            if (x + i, y, use1) not in used:
                                used.add((x + i, y, use1))
                                tmp.append((x + i, y, use1))
                        elif use1 == 0 and (x + i, y, 1) not in used:
                            used.add((x + i, y, 1))
                            tmp.append((x + i, y, 1))
                    # end if

                    if 0 <= y + i < cols:
                        if grid[x][y + i] == 0:
                            if (x, y + i, use1) not in used:
                                used.add((x, y + i, use1))
                                tmp.append((x, y + i, use1))
                        elif use1 == 0 and (x, y + i, 1) not in used:
                            used.add((x, y + i, 1))
                            tmp.append((x, y + i, 1))
                    # end if
                # end for
            ans += 1
            q = tmp
        # end while
        return -1


grid = [[0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0],
        [1, 1, 1, 0, 0]]
print(Solution().getBestRoad(grid))
