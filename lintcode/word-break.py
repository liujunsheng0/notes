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
        """ DFS 内存超出限制 """
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


"""
描述 https://www.lintcode.com/problem/word-break-ii/description
给一字串s和单词的字典dict,在字串中增加空格来构建一个句子，并且所有单词都来自字典。返回所有有可能的句子。
给一字串lintcode,字典为["de", "ding", "co", "code", "lint"] 则结果为["lint code", "lint co de"]
"""

# TODO: 未AC
class Solution:
    """
    @param: s: A string
    @param: wordDict: A set of words.
    @return: All possible sentences.
    """
    def wordBreak(self, s, wordDict):
        """内存超出限制"""
        if not s:
            return True
        size = len(s)
        # dp[i] == True 表示 s中0~i是可以由dicts中的单词组成的
        dp = [[False, []] for _ in range(size + 1)]
        dp[0][0] = True
        for idx, (v, path) in enumerate(dp):
            if not v:
                continue
            for w in wordDict:
                tmp = len(w)
                if w == s[idx: idx + tmp]:
                    dp[idx + tmp][0] = True
                    dp[idx + tmp][1] += [i + [w] for i in path] if path else [[w]]
                # end if
            # end for
        # end for
        return [" ".join(i) for i in dp[-1][-1]]

print(Solution().wordBreak("abcdadada", ["a", "d", "c", "b"]))
print(Solution().wordBreak("lintcode", ["de","ding","co","code","lint"]))
print(Solution().wordBreak("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                           ["a","aa","aaa","aaaa","aaaaa","aaaaaa","aaaaaaa","aaaaaaaa","aaaaaaaaa","aaaaaaaaaa"]))
