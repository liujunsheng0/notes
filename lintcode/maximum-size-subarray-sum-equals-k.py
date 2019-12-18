#!/usr/bin/python3.6
# -*- coding: utf-8 -*-


"""
最大子数组之和为k https://www.lintcode.com/problem/maximum-size-subarray-sum-equals-k/description
给一个数组nums和目标值k, 找到数组中最长的连续子数组, 使其中的元素和为k. 如果没有, 则返回0.
(连续子数组)
数组之和保证在32位有符号整型数的范围内

输入: nums = [1, -1, 5, -2, 3], k = 3
输出: 4
解释: 子数组[1, -1, 5, -2]的和为3, 且长度最大


样例2
输入: nums = [-2, -1, 2, 1], k = 1
输出: 2
解释: 子数组[-1, 2]的和为1, 且长度最大
"""


class Solution:
    """
    @param nums: an array
    @param k: a target value
    @return: the maximum length of a subarray that sums to k
    """

    def maxSubArrayLen1(self, nums, k):
        """时间复杂度: O(n ^ 2) 超时"""
        if not nums:
            return 0
        ans = 0
        for idx, i in enumerate(nums):
            if i == k:
                ans = max(ans, 1)
            for idy, j in enumerate(nums[idx + 1:]):
                i += j
                if i == k:
                    ans = max(ans, idy + 2)
        return ans

    def maxSubArrayLen2(self, nums, target):
        """
        前缀和: sum[i], sum[j] j > i
        if: sum[i] + k = sum[j] then: k = sum[j] - sum[i]
        因此每次计算完前缀和后, 只需要判断: 前缀和 - target 是否在dict中, 如果在, 则nums[i + 1: j]即为所求
        """
        prefix = 0
        index = dict()
        ans = 0
        for idx, i in enumerate(nums):
            if i == target:
                ans = max(ans, 1)
            prefix += i
            if prefix == target:
                ans = max(ans, idx + 1)
            if prefix - target in index:
                ans = max(ans, idx - index[prefix - target])
            if prefix not in index:
                index[prefix] = idx
        return ans


if __name__ == '__main__':
    from random import randint
    for _ in range(100):
        nums = [randint(-50, 50) for _ in range(randint(5, 30))]
        target = randint(0, 100)
        if not Solution().maxSubArrayLen1(nums, target) == Solution().maxSubArrayLen2(nums, target):
            print(nums, target)
