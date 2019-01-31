#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
描述 https://www.lintcode.com/problem/contiguous-array/description
给一个二进制数组，找到0 和 1 数量相等的连续子数组的最大长度

给出的二进制数组的长度不会超过 50,000。

样例 1:
输入: [0,1]
输出: 2
解释: [0, 1] 是具有相等数量的 0 和 1 的最长子数组。
样例 2:

输入: [0,1,0]
输出: 2
解释: [0, 1] (或者 [1, 0]) 是具有相等数量 0 和 1 的最长子数组。
"""

from collections import namedtuple


class Solution:
    """
    @param nums: a binary array
    @return: the maximum length of a contiguous subarray
    """

    def findMaxLength(self, nums):
        """
        0 -> -1, 前缀和排序, 如果两者和相等, 说明不是交集的那部分 0和1的数量相等
        时间复杂度度, N * logN
        """
        prefix_sum = []
        nums = map(lambda x: -1 if x == 0 else x, nums)
        tmp = 0
        pair = namedtuple('pair', ('idx', 'sum'))
        for idx, v in enumerate(nums):
            tmp += v
            prefix_sum.append(pair(idx, tmp))
        # end for
        prefix_sum.sort(key=lambda x: x.sum)
        ans = 0
        for i, v in enumerate(prefix_sum):
            if v.sum == 0:
                ans = max(ans, v.idx + 1)
            tmp = 1
            while (i - tmp) > 0 and v.sum == prefix_sum[i - tmp].sum:
                ans = max(ans, abs(v.idx - prefix_sum[i - tmp].idx))
                tmp += 1
            # end while
        # end for
        return ans

    def findMaxLength2(self, nums):
        """
        进一步优化上述代码, 无需排序, 只是为了找值相等的前缀和
        时间复杂度 O(N)
        """
        nums = map(lambda x: -1 if x == 0 else x, nums)
        hit = {0: -1}
        sum_ = ans = 0
        for idx, v in enumerate(nums):
            sum_ += v
            if sum_ in hit:
                ans = max(ans, idx - hit[sum_])
            else:
                hit[sum_] = idx
        # end for
        return ans


l = [0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0,
     1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0,
     0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0,
     1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1,
     1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1,
     1, 0, 0, 1, 1, 1, 0, 1, 0, 1]

print(Solution().findMaxLength(l))
