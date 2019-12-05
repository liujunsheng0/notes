#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
螺旋矩阵  https://www.lintcode.com/problem/spiral-matrix/description
给定一个包含 m x n 个要素的矩阵，（m 行, n 列），按照螺旋顺序，返回该矩阵中的所有要素。

输入:[[ 1, 2, 3 ], [ 4, 5, 6 ], [ 7, 8, 9 ]]
输出: [1,2,3,6,9,8,7,4,5]

输入:[[ 6,4,1 ], [ 7,8,9 ]]
输出: [6,4,1,9,8,7]
"""


class Solution:
    """
    @param matrix: a matrix of m x n elements
    @return: an integer list
    """
    def spiralOrder(self, matrix):
        m = len(matrix)
        if m < 1:
            return []
        n = len(matrix[0])
        if n < 1:
            return []
        l, r, u, d = 0, n - 1, 0, m - 1
        ans = []

        while l <= r and u <= d:
            # ->
            for i in range(l, r + 1):
                ans.append(matrix[u][i])
            u += 1

            # ↓
            for i in range(u, d + 1):
                ans.append(matrix[i][r])
            r -= 1

            # <-
            if u <= d:  # 说明此层未被遍历
                for i in range(r, l - 1, -1):
                    ans.append(matrix[d][i])
            d -= 1
            # ↑
            if l <= r:  # 说明此层未被遍历
                for i in range(d, u - 1, -1):
                    ans.append(matrix[i][l])
            l += 1
        # end while
        return ans


print(Solution().spiralOrder([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
print(Solution().spiralOrder([[6, 4, 1], [7, 8, 9]]))
print(Solution().spiralOrder([[1, 2, 3, 4, 5, 6, 7, 8, 9]]))


"""
https://www.lintcode.com/problem/spiral-matrix-ii/description
给定一个数n, 生成一个包含1~n^2n的螺旋形矩阵.
输入: 3
输出:
[
  [ 1, 2, 3 ],
  [ 8, 9, 4 ],
  [ 7, 6, 5 ]
]
"""


class Solution:
    """
    @param n: An integer
    @return: a square matrix
    """
    def generateMatrix(self, n):
        # write your code here
        num = 1
        matrix = [[0] * n for _ in range(n)]
        left = up = 0
        right = down = n - 1
        while num <= (n * n):
            for i in range(left, right + 1):
                matrix[up][i] = num
                num += 1
            up += 1
            for i in range(up, down + 1):
                matrix[i][right] = num
                num += 1
            right -= 1
            for i in range(right, left - 1, -1):
                matrix[down][i] = num
                num += 1
            down -= 1
            for i in range(down, up - 1, -1):
                matrix[i][left] = num
                num += 1
            left += 1
        # end while
        return matrix

print(Solution().generateMatrix(3))