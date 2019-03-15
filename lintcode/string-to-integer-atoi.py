#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
转换字符串到整数  https://www.lintcode.com/problem/string-to-integer-atoi/description
实现atoi这个函数，将一个字符串转换为整数。
如果没有合法的整数，返回0。
如果整数超出了32位整数的范围，
返回INT_MAX(2147483647)如果是正整数，
或者INT_MIN(-2147483648)如果是负整数。
"10" =>10
"-1" => -1
"123123123123123" => 2147483647
"1.0" => 1
"""


class Solution:
    INT_MAX = 2147483647
    INT_MIN = -2147483648
    """
    @param str: A string
    @return: An integer
    """
    def atoi(self, s: str):
        s = ''.join(s.split('.')[0].split())
        if not s:
            return 0
        symbol = 1
        if s[0] == '-':
            symbol = -1
            s = s[1:]
        elif s[0] == "+":
            s = s[1:]
        idx = len(s)
        for i, v in enumerate(s):
            if v < '0' or v > '9':
                idx = i
                break
        s = s[:idx]
        if not s:
            return 0
        if len(s) > 10:
            return self.INT_MAX if symbol > 0 else self.INT_MIN
        if len(s) == 10:
            if symbol > 0 and s > '2147483647':
                return self.INT_MAX
            if symbol < 0 and s > '2147483648':
                return self.INT_MIN
        # end if
        return int(s) * symbol


print(Solution().atoi("-15 + 4"))