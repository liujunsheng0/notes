#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
https://www.lintcode.com/problem/4sum-ii/description
给出 A, B, C, D 四个整数列表，计算有多少的tuple (i, j, k, l)满足A[i] + B[j] + C[k] + D[l]为 0。
为了简化问题，A, B, C, D 具有相同的长度，且长度N满足 0 ≤ N ≤ 500。所有的整数都在范围(-2^28, 2^28 - 1)内以及保证结果最多为2^31 - 1。
输入:
A = [ 1, 2]
B = [-2,-1]
C = [-1, 2]
D = [ 0, 2]

输出:
2
这两个tuple为:
1. (0, 0, 0, 1) -> A[0] + B[0] + C[0] + D[1] = 1 + (-2) + (-1) + 2 = 0
2. (1, 1, 0, 0) -> A[1] + B[1] + C[0] + D[0] = 2 + (-1) + (-1) + 0 = 0
"""

from collections import Counter


class Solution:
    """
    @param A: a list
    @param B: a list
    @param C: a list
    @param D: a list
    @return: how many tuples (i, j, k, l) there are such that A[i] + B[j] + C[k] + D[l] is zero
    """
    def fourSumCount(self, A: list, B: list, C: list, D: list):
        """时间复杂度N^2, 空间换时间"""
        d = Counter([i + j for i in C for j in D])
        ans = 0
        for a in A:
            for b in B:
                ans += d.get(-(a + b), 0)
        return ans
