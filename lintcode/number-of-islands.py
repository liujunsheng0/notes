#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
岛屿的个数 https://www.lintcode.com/problem/number-of-islands/description
给一个 01 矩阵，求不同的岛屿的个数。
0 代表海，1 代表岛，如果两个 1 相邻，那么这两个 1 属于同一个岛。我们只考虑上下左右为相邻。
输入：
[
  [1,1,0,0,0],
  [0,1,0,0,1],
  [0,0,0,1,1],
  [0,0,0,0,0],
  [0,0,0,0,1]
]
输出：
3
"""


class Solution:
    """
    @param grid: a boolean 2D matrix
    @return: an integer
    """

    def numIslands(self, grid):
        # write your code here
        m = len(grid)
        if m < 1:
            return 0
        n = len(grid[0])
        if n < 1:
            return 0
        ans = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] != 1:
                    continue
                self.bfs(grid, m, n, i, j)
                ans += 1
                # end for
        # end for
        return ans

    def bfs(self, grid, m, n, x, y):
        grid[x][y] = 0
        if y + 1 < n and grid[x][y + 1] == 1:
            self.bfs(grid, m, n, x, y + 1)
        if x + 1 < m and grid[x + 1][y] == 1:
            self.bfs(grid, m, n, x + 1, y)
        if x > 0 and grid[x - 1][y] == 1:
            self.bfs(grid, m, n, x - 1, y)
        if y > 0 and grid[x][y - 1] == 1:
            self.bfs(grid, m, n, x, y - 1)


"""
岛屿的个数2 https://www.lintcode.com/problem/number-of-islands-ii/description
给定 n, m, 分别代表一个二维矩阵的行数和列数, 并给定一个大小为 k 的二元数组A. 初始二维矩阵全0. 二元数组A内的k个元素代表k次操作,
设第i个元素为 (A[i].x, A[i].y), 表示把二维矩阵中下标为A[i].x行A[i].y列的元素由海洋变为岛屿. 问在每次操作之后, 二维矩阵中岛屿
的数量. 你需要返回一个大小为k的数组.
设定0表示海洋, 1代表岛屿, 并且上下左右相邻的1为同一个岛屿.
输入: n = 4, m = 5, A = [[1,1],[0,1],[3,3],[3,4]]
输出: [1,1,2,2]
解释:
0.  00000
    00000
    00000
    00000
1.  00000
    01000
    00000
    00000
2.  01000
    01000
    00000
    00000
3.  01000
    01000
    00000
    00010
4.  01000
    01000
    00000
    00011
"""


class Point:
    def __init__(self, a=0, b=0):
        self.x = a
        self.y = b


# TODO 超时, 未AC
class Solution:
    """
    @param n: An integer
    @param m: An integer
    @param operators: an array of point
    @return: an integer array
    """

    def numIslands2(self, n, m, operators):
        ans = []
        islands = []
        for p in operators:
            p = Point(*p)
            if p.x < n and p.y < m:
                merge_id = None
                x, y = p.x, p.y
                for idx, s in enumerate(islands):
                    if (x, y) in s or (x + 1, y) in s or (x - 1, y) in s or (x, y + 1) in s or (x, y - 1) in s:
                        merge_id = idx
                        s.add((p.x, p.y))
                        break
                # end for
                if merge_id is None:
                    islands.append(set([(p.x, p.y)]))
                else:
                    pop_ids = []
                    # 合并相邻的岛屿
                    for idx, s in enumerate(islands[merge_id + 1:]):
                        if (x, y) in s or (x - 1, y) in s or (x + 1, y) in s or (x, y + 1) in s or (x, y - 1) in s:
                            islands[merge_id].update(s)
                            pop_ids.append(idx + merge_id + 1)
                    for i in pop_ids[::-1]:
                        islands.pop(i)

            ans.append(len(islands))
        # end for
        return ans


ans = Solution().numIslands2(12, 20,
                             [[6, 2], [0, 9], [0, 6], [9, 3], [0, 12], [8, 6], [5, 3], [9, 19], [5, 4], [11, 11],
                              [9, 15], [4, 4], [4, 11], [6, 12], [8, 5], [2, 2], [10, 18], [8, 14], [5, 16], [3, 0],
                              [9, 10], [10, 6], [10, 3], [6, 1], [9, 13], [5, 11], [0, 7], [8, 4], [7, 7], [0, 1],
                              [11, 7], [6, 9], [10, 16], [10, 0], [4, 18], [11, 15], [2, 12], [4, 3], [8, 3], [0, 4],
                              [0, 15], [11, 18], [2, 3], [8, 0], [6, 0], [10, 14], [2, 8], [2, 18], [9, 9], [2, 7],
                              [7, 12], [5, 18], [4, 15], [3, 3], [11, 8], [11, 0], [9, 11], [1, 3], [4, 17], [9, 16],
                              [6, 7], [7, 10], [0, 18], [3, 14], [3, 2], [5, 19], [3, 18], [5, 2], [7, 14], [7, 1],
                              [6, 15], [1, 2], [8, 8], [4, 9], [5, 15], [8, 16], [8, 19], [6, 17], [2, 0], [2, 9],
                              [1, 9], [4, 12], [5, 1], [5, 0], [1, 19], [7, 16], [0, 2], [1, 16], [9, 7], [5, 8],
                              [4, 1], [8, 9], [8, 17], [2, 15], [8, 11], [7, 13], [7, 6], [9, 8], [3, 12], [0, 14],
                              [2, 17], [3, 7]])
print(ans)
