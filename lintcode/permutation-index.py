#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""
https://www.lintcode.com/problem/permutation-index/description

给出一个不含重复数字的排列, 求这些数字的所有排列按字典序排序后该排列的编号. 编号从1开始.
输入:[1,2,4]
输出:1
样例 2:

输入:[3,2,1]
输出:6

"""


class Solution:
    """
    @param A: An array of integers
    @return: A long integer
    """

    def permutationIndex(self, A):
        ans = 0
        idx = len(A) - 2
        # factor 和 n 用于阶乘
        factorial = 1
        n = 2
        # 排列组合, 从后面开始找比当前值小的
        while idx > -1:
            success = len([None for i in A[idx + 1:] if i < A[idx]])
            ans += success * factorial
            factorial *= n
            n += 1
            idx -= 1
        # end for
        # + 1为A的位置
        return ans + 1


if __name__ == '__main__':
    print(Solution().permutationIndex([22, 7, 15, 10, 11, 12, 14, 8, 9, 1, 2, 3, 6, 5, 4]), 1263957845766)
