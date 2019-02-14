#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
https://www.lintcode.com/problem/words-compression/description
有一种单词压缩方法，对于字符串数组s，我们将压缩串赋值为s[0]，然后让压缩串和s[1]两个字符串进行拼接，
且压缩串后缀和s[1]前缀的重复部分将再不重复,如”aba”+”cba”-->”abacba”,”aba”+”bac”-->”abac”。
然后让压缩串与字符串数组中的其他字符串依次进行拼接，得到目标压缩串
现在给定字符串数组s,请你输出s中每个字符串在目标压缩串中第一次出现的位置

样例
给定s=["aba","cba","acb","cb"]，返回[0,3,2,3]
解释：
首先压缩串为”aba”
    压缩串与`s[1]`拼接后的串为”abacba”
    压缩串与`s[2]`拼接后的串为”abacbacb”
    压缩串与`s[3]`拼接后的串为”abacbacb”
    所以目标压缩串为”abacbacb”
    “aba”在目标压缩串中的第一次出现位置为0
    “cba”在目标压缩串中的第一次出现位置为3
    “acb”在目标压缩串中的第一次出现位置为2
    “cb”在目标压缩串中的第一次出现位置为3
所以返回`[0,3,2,3]`

注意事项
s中字符串长度之和<=800000
s中字符串数量<=5
s只包含小写英文字母
"""


class Solution:
    """
    @param s: the given strings
    @return: Output the first occurrence of each string in `s` in the target compression string.
    """

    def wordsCompression(self, words):
        s = ''
        for w in words:
            ok = True
            for i in range(len(w), 0, -1):
                if s.endswith(w[:i]):
                    s += w[i:]
                    ok = False
                    break
            # end for
            if ok:
                s += w
        # end for
        return [s.find(i) for i in words]


# [0,4,2,11,12]
print(Solution().wordsCompression(["aaaba", "abbb", "aba", "bbaa", "baaa"]))
