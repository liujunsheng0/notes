#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""
https://www.lintcode.com/problem/substring-with-at-least-k-distinct-characters/description
给定一个仅包含小写字母的字符串 S. 返回 S 中至少包含 k 个不同字符的子串的数量.
10 ≤ length(S) ≤ 1,000,000
1 ≤ k ≤ 26
输入: S = "abcabcabcabc", k = 3
输出: 55
解释: 任意长度不小于 3 的子串都含有 a, b, c 这三个字符.
    比如,长度为 3 的子串共有 10 个, "abc", "bca", "cab" ... "abc"
    长度为 4 的子串共有 9 个, "abca", "bcab", "cabc" ... "cabc"
    ...
    长度为 12 的子串有 1 个, 就是 S 本身.
    所以答案是 1 + 2 + ... + 10 = 55.
"""


class Solution:
    """
    @param s: a string
    @param k: an integer
    @return: the number of substrings there are that contain at least k distinct characters
    """
    def kDistinctCharacters(self, s, k):
        ans = 0
        size = len(s)
        for i in range(size - k + 1):
            for j in range(i + k, size + 1):
                if len(set(s[i:j])) >= k:
                    ans += size + 1 - j
                    break
        return ans


print(Solution().kDistinctCharacters("abcabcabcabc", 3))
