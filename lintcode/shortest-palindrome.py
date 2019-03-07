#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
最短回文串 https://www.lintcode.com/problem/shortest-palindrome/description
给一个字符串 S, 你可以通过在前面添加字符将其转换为回文串.找到并返回用这种方式转换的最短回文串.

输入： "aacecaaa"
输出： "aaacecaaa"
解释：
在输入字符串前面添加一个'a'。

输入： "abcd"
输出： "dcbabcd"
"""


class Solution:
    """
    @param s: String
    @return: String
    """
    def convertPalindrome(self, s):
        size = len(s)
        for i in range(size, 1, -1):
            if s[:i] == s[i - 1::-1]:
                return s[-1:i - 1:-1] + s
        return s[-1:0:-1] + s


print("zyxwvutsrqponmlkjihgfedcbabcdefghijklmnopqrstuvwxyz" == Solution().convertPalindrome("abcdefghijklmnopqrstuvwxyz"))
