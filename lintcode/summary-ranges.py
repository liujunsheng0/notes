#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
https://www.lintcode.com/problem/summary-ranges/description
给定一个没有重复的排序整数数组，返回其范围的总结。

结果按升序排列
样例 1:
输入: [0,1,2,4,5,7]
输出: ["0->2","4->5","7"]
样例 2:
输入: [0,2,3,4,6,8,9]
输出: ["0","2->4","6","8->9"]
"""


class Solution:
    """
    @param nums:  a sorted integer array without duplicates
    @return: the summary of its ranges
    """
    def summaryRanges(self, nums):
        if not nums:
            return []
        nums.sort()
        start = end = None
        ans = []
        for idx, v in enumerate(nums + nums[:1]):
            if start is None:
                start = end = v
            elif end == v - 1:
                end = v
            else:
                if start == end:
                    ans.append('%s' % start)
                else:
                    ans.append('%s->%s' % (start, end))
                start = end = v
            # end if
        # end for
        return ans
print(Solution().summaryRanges([1,2,3,5,7,10]))