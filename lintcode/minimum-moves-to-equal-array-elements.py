#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
使数组元素相同的最少步数  https://www.lintcode.com/problem/minimum-moves-to-equal-array-elements/description

给定一个大小为n的非空整数数组, 找出使得数组中所有元素相同的最少步数, 其中一步被定义为将数组中n - 1个元素加一。

输入：
[1,2,3]
输出：
3
说明：
只需要三步即可（每一步将其中两个元素加一）：
[1,2,3]  =>  [2,3,3]  =>  [3,4,3]  =>  [4,4,4]
"""


class Solution:
    """
    @param nums: an array
    @return: the minimum number of moves required to make all array elements equal
    对于长度n的数组中, 将n-1个元素的值加一, 其实可以等价于将某个元素减一,
    所以需要的步数就等于sum(1,n) - minNum * length,
    其中sum(1,n)sum(1,n)为数组所有元素的和, minNum为数组中最小的元素, length为数组长度.
    """

    def minMoves(self, nums):
        return sum(nums) - min(nums) * len(nums)


print(Solution().minMoves([1, 2, 3]))

"""
使数组元素相同的最少步数II https://www.lintcode.com/problem/minimum-moves-to-equal-array-elements-ii/description
给定一个非空的整数数组, 找出使得数组中所有元素相同的最少步数, 其中一步被定义为将数组内任一元素加一或减一.
数组中最多包含10,000个元素.
输入：
[1,2,3]
输出：
2
说明：
只需要两步即可（每一步将一个元素加一或减一）：
[1,2,3]  =>  [2,2,3]  =>  [2,2,2]
"""


class Solution:
    """
    @param nums: an array
    @return: the minimum number of moves required to make all array elements equal
    排序, 往中间位靠拢
    """

    def minMoves2(self, nums: list):
        size = len(nums)
        nums.sort()
        idx = size // 2
        return sum([abs(nums[idx] - i) for i in nums])

print(Solution().minMoves2([1, 2, 3, 99]))
