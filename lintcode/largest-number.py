#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
最大数 https://www.lintcode.com/problem/largest-number/description

给出一组非负整数，重新排列他们的顺序把他们组成一个最大的整数。
最后的结果可能很大，所以我们返回一个字符串来代替这个整数。

样例
给出 [1, 20, 23, 4, 8]，返回组合最大的整数应为8423201。
给出 [1, 20, 86, 7, 8]，返回组合最大的整数应为8867201。

挑战
在 O(nlogn) 的时间复杂度内完成。
"""

from functools import cmp_to_key


class Solution:
    """
    @param nums: A list of non negative integers
    @return: A string
    """

    def largestNumber(self, nums):
        nums = sorted(map(str, nums), key=cmp_to_key(lambda x, y: -1 if x + y > y + x else 1))
        return "".join(nums) if nums[0] != '0' else '0'

print(Solution().largestNumber([1, 2]))
