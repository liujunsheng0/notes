#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
房屋染色  https://www.lintcode.com/problem/paint-house/description

这里有n个房子在一列直线上，现在我们需要给房屋染色，分别有红色蓝色和绿色。每个房屋染不同的颜色费用也不同，你需要设计一种染色方
案使得相邻的房屋颜色不同，并且费用最小，返回最小的费用。费用通过一个nx3 的矩阵给出，
比如cost[0][0]表示房屋0染红色的费用，cost[1][2]表示房屋1染绿色的费用。所有费用都是正整数

输入: [[14,2,11],[11,14,5],[14,3,10]]  输出: 10
解释: 蓝 绿 蓝, 2 + 5 + 3 = 10
输入: [[1,2,3],[1,4,6]]
输出: 3
"""

"""
房屋染色 II https://www.lintcode.com/problem/paint-house-ii/description
这里有n个房子在一列直线上，现在我们需要给房屋染色，共有k种颜色。每个房屋染不同的颜色费用也不同，你需要设计一种染色方案使得相邻的房屋颜色不同，并且费用最小。
费用通过一个nxk 的矩阵给出，比如cost[0][0]表示房屋0染颜色0的费用，cost[1][2]表示房屋1染颜色2的费用。
所有费用都是正整数
costs = [[14,2,11],[11,14,5],[14,3,10]] return 10
房屋 0 颜色 1, 房屋 1 颜色 2, 房屋 2 颜色 1， 2 + 5 + 3 = 10
挑战
用O(nk)的时间复杂度解决
"""


class Solution:
    """
    @param costs: n x 3 cost matrix
    @return: An integer, the minimum cost to paint all houses
    """

    def minCost(self, costs):
        if len(costs) < 1:
            return 0
        costs = [list(i) for i in costs]
        for idx, v in enumerate(costs[1:]):
            v[0] += min(costs[idx][1], costs[idx][2])
            v[1] += min(costs[idx][0], costs[idx][2])
            v[2] += min(costs[idx][0], costs[idx][1])
        # end for
        return min(costs[-1])

    """
    @param costs: n x k cost matrix
    @return: an integer, the minimum cost to paint all houses
    """
    def minCostII_(self, costs):
        """ 超时 """
        if len(costs) < 1:
            return 0
        for idx, cost in enumerate(costs[1:]):
            for idy in range(len(cost)):
                cost[idy] += min(costs[idx][:idy] + costs[idx][idy + 1:])
        # end for
        return min(costs[-1])

    def minCostII(self, costs):
        """ 优化后, AC过"""
        if len(costs) < 1:
            return 0
        if len(costs[0]) < 2:
            return sum([i[0] for i in costs])
        for idx, cost in enumerate(costs[1:]):
            sort = list(sorted([(i, j) for j, i in enumerate(costs[idx])]))
            for idy in range(len(cost)):
                cost[idy] += sort[0][0] if idy != sort[0][1] else sort[1][0]
        # end for
        return min(costs[-1])


print(Solution().minCostII([[1,5,6],[14,15,5],[4,3,3],[15,15,9],[9,2,7],[6,5,7],[19,4,4],[6,13,3],[8,16,20],[18,7,9]]))
