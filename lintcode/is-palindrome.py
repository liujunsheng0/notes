#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
判断一个正整数是否为回文整数
"""

class Solution(object):
    def is_palindrome(self, n):
        return int(''.join(list(reversed(str(n))))) == n


print(Solution().is_palindrome(2221222))