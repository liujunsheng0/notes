#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
飞行棋 I https://www.lintcode.com/problem/modern-ludo-i/description?_from=ladder&&fromId=62
有一个一维的棋盘，起点在棋盘的最左侧，终点在棋盘的最右侧，棋盘上有几个位置是跟其他的位置相连的，
即如果A与B相连，则当棋子落在位置A时, 你可以选择是否不投骰子，直接移动棋子从A到B。并且这个连接是单向的，即不能从B移动到A，
现在给定这个棋盘的长度length和位置的相连情况connections，你有一个六面的骰子(点数1-6)，最少需要丢几次才能到达终点。

下标从 1 开始
length > 1
起点不与任何其他位置连接
connections[i][0] < connections[i][1]

输入: length = 10 和 connections = [[2, 10]]   输出: 1
解释:
0->2 (投骰子)
2->10(直接相连)

输入: length = 15 和 connections = [[2, 8],[6, 9]]  输出: 2
解释:
0->6 (投骰子)
6->9 (直接相连)
9->15(投骰子)
"""

from collections import defaultdict


class Solution:
    """
    @param length: the length of board
    @param connections: the connections of the positions
    @return: the minimum steps to reach the end
    """

    def modernLudo(self, length, connections: list):
        d = defaultdict(list)
        for i, j in connections:
            d[i].append(j)
        dp = [float('inf')] * (length + 1)
        dp[1] = dp[2] = dp[3] = dp[4] = dp[5] = dp[6] = dp[7] = 1
        for i in range(1, length + 1):
            if i > 7:
                tmp = min(dp[i - 6:i]) + 1
                dp[i] = min(dp[i], tmp)

            if i in d:
                for j in d[i]:
                    dp[j] = min(dp[i], dp[j])
            # end if
        return dp[-1]


# print(Solution().modernLudo(15, [[7, 9], [8, 14]]))
print(Solution().modernLudo(79, [[5, 27], [37, 70], [16, 44], [10, 22], [17, 67], [45, 50]]))
