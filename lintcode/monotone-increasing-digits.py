#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
单调递增的数字 https://www.lintcode.com/problem/monotone-increasing-digits/description

给一非负整数 N, 找到小于等于 N 的最大的 单调递增数. (回想一下, 当且仅当每对相邻的数字 x 和 y 满足 x <= y 时, 这个整数才是单调递增数)
N 为范围 [0, 10^9] 内的整数

样例
给出 N = 10, 返回 9
给出 N = 12345, 返回 12345
给出 N = 10000, 返回 9999
"""


class Solution:
    """
    @param num: a non-negative integer N
    @return: the largest number that is less than or equal to N with monotone increasing digits.
    """
    def monotoneDigits(self, num):
        nums = list(str(num))
        idx, size = 0, len(nums)
        while idx < size - 1:
            if nums[idx] > nums[idx + 1]:
                break
            idx += 1
        # end while
        if idx == size - 1:
            return num
        while idx > 0 and nums[idx] == nums[idx - 1]:
            idx -= 1
        while idx + 1 < size:
            nums[idx + 1] = '0'
            idx += 1
        return int(''.join(nums)) - 1

print(Solution().monotoneDigits(11211))