#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
将数组重新排序以构造最小值  https://www.lintcode.com/problem/reorder-array-to-construct-the-minimum-number/description
给定一个整数数组，请将其重新排序，以构造最小值。

The result may be very large, so you need to return a string instead of an integer.

您在真实的面试中是否遇到过这个题？  是
题目纠错
样例
给定 [3, 32, 321]，通过将数组重新排序，可构造 6 个可能性数字：

3+32+321=332321
3+321+32=332132
32+3+321=323321
32+321+3=323213
321+3+32=321332
321+32+3=321323
其中，最小值为 321323，所以，将数组重新排序后，该数组变为 [321, 32, 3]。

挑战
在原数组上完成，不使用额外空间。
"""


from itertools import dropwhile
from functools import cmp_to_key


class Solution:
    """
    @param nums: n non-negative integer array
    @return: A string
    """
    def minNumber(self, nums):
        cmp = lambda x, y: -1 if x + y < y + x else 1
        nums = sorted(map(str, nums), key=cmp_to_key(cmp))
        ans = ''.join(dropwhile(lambda _: _ == '0', nums))
        return ans if ans else '0'

print(Solution().minNumber([1, 32, 2, 1, 0]))
