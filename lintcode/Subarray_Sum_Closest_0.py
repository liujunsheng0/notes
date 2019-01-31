#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
描述: https://www.lintcode.com/problem/subarray-sum-closest/description
给定一个整数数组，找到一个和最接近于零的子数组。返回第一个和最右一个指数。你的代码应该返回满足要求的子数组的起始位置和结束位置
给出[-3, 1, 1, -3, 5]，返回[0, 2]，[1, 3]， [1, 1]， [2, 2] 或者 [0, 4]。(位置连续)
"""


from collections import namedtuple


class Solution:
    """
    @param: nums: A list of integers
    @return: A list of integers includes the index of the first number and the index of the last number
    """
    def subarraySumClosest1(self, nums):
        # O(N^2)
        ans = [0, 0]
        min_v = float('inf')
        for idx, _ in enumerate(nums):
            tmp = 0
            for idy, y in enumerate(nums[idx:]):
                tmp += y
                if tmp == 0:
                    return [idx, idx + idy]
                if abs(tmp) < min_v:
                    min_v, ans = abs(tmp), [idx, idx + idy]
            # end for
        # end for
        return ans

    def subarraySumClosest(self, nums):
        """
        O(N * logN)
        https://segmentfault.com/a/1190000012735926
        按照sum排序，计算相邻sum的差值。理由：sum的差值[绝对值]越小，表明之间的元素和越接近0
        先统计前缀和0~n的和prefix,排序,假设prefix(n)和prefix(n-1)和相差最小, prefix(n) = prefix(n - 1) + f(n), 即f(n)接近0
        """
        if not nums:
            return []
        prefix_sum = []
        pair = namedtuple('pair', ['index', 'v'])
        tmp = 0
        for i, j in enumerate(nums):
            tmp += j
            prefix_sum.append(pair(i, tmp))
        # end for
        prefix_sum.sort(key=lambda x: x.v)
        min_v, ans = abs(prefix_sum[0].v), [0, prefix_sum[0].index]
        for i in range(1, len(prefix_sum)):
            index, v = prefix_sum[i].index, prefix_sum[i].v
            if min_v > abs(v):
                min_v, ans = abs(v), [0, index]
            # end if
            diff = abs(v - prefix_sum[i - 1].v)
            if min_v > diff:
                min_v, ans = diff, [min(prefix_sum[i - 1].index, index) + 1, max(prefix_sum[i - 1].index, index)]
            # end if
            if min_v == 0:
                return ans
        # end for
        return ans

print(Solution().subarraySumClosest([-3, 1, 1, -3, 5]))
