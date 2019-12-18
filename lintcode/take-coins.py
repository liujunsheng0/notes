#!/usr/bin/python3.6
# -*- coding: utf-8 -*-


"""
拿硬币 https://www.lintcode.com/problem/take-coins/description
有n个硬币排成一排, 每次要你从最左边或者最右侧拿出一个硬币.总共拿k次, 写一个算法, 使能拿到的硬币的和最大.

输入： list = [5,4,3,2,1], k = 2,
输出：9
解释：从左边开始连取两个硬币即可.

输入： list = [5,4,3,2,1,6], k = 3
输出：15.
解释：从左边开始连取两个硬币,右边取一个即可.
"""


class Solution:

    def takeCoins(self, l, k):
        """
        左连续 右连续 双指针
        @param l: The coins
        @param k: The k
        @return: The answer
        """
        size = len(l)
        if k >= size:
            return sum(l)
        left, right = k - 1, size - 1
        sum_ = sum(l[:k])
        ans = sum_
        while left >= 0:
            sum_ = sum_ - l[left] + l[right]
            ans = max(ans, sum_)
            left -= 1
            right -= 1
        # end while
        return ans


print(Solution().takeCoins([5, 4, 3, 2, 1, 6], 3))
