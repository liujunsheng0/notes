#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
分割标签 https://www.lintcode.com/problem/partition-labels/description
给出一个由小写字母组成的字符串S。将这个字符串分割成尽可能多的部分，使得每个字母只出现在一个部分中，并且返回每个部分的长度。

S的长度在[1, 500]范围内。 S只包含小写字母（'a' 至 'z'）。
样例
输入: S = "ababcbacadefegdehijhklij"
输出: [9,7,8]
解释:
    原字符串分割为 "ababcbaca", "defegde", “hijhklij”。
    这样的分割使得每个字母最多出现在一个部分里。
    将原字符串分为"ababcbacadefegde", “hijhklij”是不正确的，因为它没有将S分割成尽可能多的部分。
"""

from collections import OrderedDict


class Solution:
    """
    @param S: a string
    @return: a list of integers representing the size of these parts
    """
    def partitionLabels(self, S):
        if not S:
            return []
        d = OrderedDict()
        for idx, c in enumerate(S):
            if c not in d:
                d[c] = []
            d[c].append(idx)
        # end for
        l = [(v[0], v[-1]) if len(v) > 1 else (v[0], v[0]) for _, v in d.items()]
        start, end = l[0]
        ans = []
        for idx, (s, e) in enumerate(l[1:]):
            if s > end:
                ans.append(end - start + 1)
                start, end = s, e
            else:
                end = max(end, e)
        # end for
        return ans + [end - start + 1]

print(Solution().partitionLabels("aba"))