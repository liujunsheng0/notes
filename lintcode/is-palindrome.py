#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
判断一个正整数是否为回文整数
"""

class Solution(object):
    def is_palindrome(self, n):
        return int(''.join(list(reversed(str(n))))) == n

    def is_palindrome2(self, n):
        cur = n
        reverse = 0
        while cur > 0:
            reverse = reverse * 10 + cur % 10
            cur //= 10
        # end while
        return reverse == n

print(Solution().is_palindrome2(21))
