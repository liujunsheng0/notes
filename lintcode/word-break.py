#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
单词拆分I https://www.lintcode.com/problem/word-break/description
给定字符串 s 和单词字典 dict，确定 s 是否可以分成一个或多个以空格分隔的子串，并且这些子串都在字典中存在。

输入:  "lintcode", ["lint", "code"]  输出:  true
输入: "a", ["a"]                     输出:  true
"""


class Solution:
    """
    @param: s: A string
    @param: dict: A dictionary of words dict
    @return: A boolean
    """
    def wordBreak(self, s, dicts):
        """ DFS 内存溢出 """
        if not s:
            return True
        for i in dicts:
            if s.startswith(i) and self.wordBreak(s[len(i):], dicts):
                return True
        return False

    def wordBreak2(self, s, dicts):
        if not s:
            return True
        size = len(s)
        # dp[i] == True 表示 s中0~i是可以由dicts中的单词组成的
        dp = [False] * (size + 1)
        dp[0] = True
        for idx, v in enumerate(dp):
            if not v:
                continue
            for w in dicts:
                tmp = len(w)
                if w == s[idx: idx + tmp]:
                    dp[idx + tmp] = True
            # end for
        # end for
        return dp[-1]

print(Solution().wordBreak("abcdadada", ["a", "d", "c", "b"]))
print(Solution().wordBreak2("abcdadada", ["a", "d", "c", "b"]))
