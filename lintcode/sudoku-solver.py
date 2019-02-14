#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
https://www.lintcode.com/problem/sudoku-solver/description

编写一个程序，通过填充空单元来解决数独难题。
空单元由数字0表示。
你可以认为只有一个唯一的解决方案。
"""


class Solution:
    """
    @param board: the sudoku puzzle
    @return: nothing
    """

    def solveSudoku(self, board):
        """ Python3 超时, Python2通过 """
        if not board or len(board) != 9 or len(board[0]) != 9:
            return
        self.dfs(board, 0, 0)

    def is_ok(self, board, x, y):
        s = [board[x][i] for i in range(9) if board[x][i] != 0]
        if len(s) > len(set(s)):
            return False
        s = [board[i][y] for i in range(9) if board[i][y] != 0]
        if len(s) > len(set(s)):
            return False
        x_, y_ = x // 3, y // 3
        s = [board[x_ * 3 + i][y_ * 3 + j] for i in range(3) for j in range(3) if board[x_ * 3 + i][y_ * 3 + j] != 0]
        if len(s) > len(set(s)):
            return False
        return True

    def dfs(self, board, x, y):
        x += y // 9
        y %= 9
        if x >= 9:
            return True
        if board[x][y] != 0:
            return self.dfs(board, x, y + 1)
        for i in range(1, 10):
            board[x][y] = i
            if self.is_ok(board, x, y) and self.dfs(board, x, y + 1):
                return True
            board[x][y] = 0
        # end for
        return False


matrix = [[0, 0, 9, 7, 4, 8, 0, 0, 0],
          [7, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 2, 0, 1, 0, 9, 0, 0, 0],
          [0, 0, 7, 0, 0, 0, 2, 4, 0],
          [0, 6, 4, 0, 1, 0, 5, 9, 0],
          [0, 9, 8, 0, 0, 0, 3, 0, 0],
          [0, 0, 0, 8, 0, 3, 0, 2, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 6],
          [0, 0, 0, 2, 7, 5, 9, 0, 0]]
print(Solution().solveSudoku(matrix))
print(matrix)

z = [[5, 1, 9, 7, 4, 8, 6, 3, 2],
     [7, 8, 3, 6, 5, 2, 4, 1, 9],
     [4, 2, 6, 1, 3, 9, 8, 7, 5],
     [3, 5, 7, 9, 8, 6, 2, 4, 1],
     [2, 6, 4, 3, 1, 7, 5, 9, 8],
     [1, 9, 8, 5, 2, 4, 3, 6, 7],
     [9, 7, 5, 8, 6, 3, 1, 2, 4],
     [8, 3, 2, 4, 9, 1, 7, 5, 6],
     [6, 4, 1, 2, 7, 5, 9, 8, 3]]

# for i in range(9):
#     for j in range(9):
#         print(i, j, Solution().is_ok(z, i, j))
