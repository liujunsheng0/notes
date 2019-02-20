#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
题目描述: 推荐朋友, 平台: https://www.lintcode.com/problem/recommend-friend/
描述
某同性交友网站会给除了第一个用户以外的每个新注册的用户 推荐一位之前已经注册过并且性格值和他最相近的用户,如果有多人满足条件则选,
择性格值较小的。
给定数组val[]表示按时间顺序注册的n位用户的性格值，输出一个大小为n-1的数组，表示系统给这些人推荐的用户的性格值。
2 <= n <= 100000, 0 <= val<= 1000000
样例: 给定val=[8,9,7,3,0,5,11],返回[8,8,7,3,3,9]
"""


class Solution:
    """
    @param val: the personality value of user
    @return: Return their recommend friends' value
    """

    def getAns(self, val):
        # 暴力解法, O(n^2), TODO: 未AC
        ret = []
        visited = set()
        for v in val[1:]:
            result = val[0]
            for i in visited:
                if abs(i - v) < abs(result - v):
                    result = i
            # end for
            visited.add(v)
            ret.append(result)
        # end for
        return ret


print(Solution().getAns([3, 2, 1, 3, 4]))
