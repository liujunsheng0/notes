#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
错位词分组 https://www.lintcode.com/problem/group-anagrams/description
给一字符串数组, 将 错位词(指相同字符不同排列的字符串) 分组, 所有的输入均为小写字母

输入: ["eat","tea","tan","ate","nat","bat"]  输出: [["ate","eat","tea"], ["bat"], ["nat","tan"]]
输入: ["eat","nowhere"]                      输出: [["eat"], ["nowhere"]]
"""

from collections import defaultdict


class Solution:
    """
    @param strs: the given array of strings
    @return: The anagrams which have been divided into groups
    """
    def groupAnagrams(self, strs):
        ans = defaultdict(list)
        for s in strs:
            sort = ''.join(sorted(s))
            ans[sort].append(s)
        return list(ans.values())


print(Solution().groupAnagrams(["123", '321']))
