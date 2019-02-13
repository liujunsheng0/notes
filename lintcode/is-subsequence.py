#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
https://www.lintcode.com/problem/is-subsequence/description
给定字符串s和t，判断s是否为t的子序列。
你可以认为在s和t中都只包含小写字母。t可能是一个非常长（length ~= 500,000）的字符串，而s是一个较短的字符串（length <= 100）。

一个字符串的子序列是在原字符串中删去一些字符（也可以不删除）后，不改变剩余字符的相对位置形成的新字符串
（例如，"ace"是"abcde"的子序列而"aec"不是）。

样例1：s = "abc"，t = "ahbgdc" 返回true。
样例2：s = "axc"，t = "ahbgdc" 返回false。
"""


class Solution:
    """
    @param s: the given string s
    @param t: the given string t
    @return: check if s is subsequence of t
    """
    def isSubsequence(self, s, t):
        len_s, len_t = len(s), len(t)
        i = j = 0
        while i < len_s and j < len_t:
            if s[i] == t[j]:
                i += 1
                j += 1
            else:
                j += 1
        # end while
        return i == len_s

print(Solution().isSubsequence('A', 'V'))