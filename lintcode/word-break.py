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



"""
https://www.lintcode.com/problem/word-break-iii/description?_from=ladder&&fromId=137
给出一个单词表和一条去掉所有空格的句子，根据给出的单词表添加空格, 返回可以构成的句子的数量, 保证构成的句子中所有的单词都可以在单词表中找到.
忽略大小写

输入：
"CatMat"
["Cat", "Mat", "Ca", "tM", "at", "C", "Dog", "og", "Do"]
输出： 3
解释：
我们可以有如下三种方式：
"CatMat" = "Cat" + "Mat"
"CatMat" = "Ca" + "tM" + "at"
"CatMat" = "C" + "at" + "Mat"
"""


class Solution:
    """
    @param: : A string
    @param: : A set of word
    @return: the number of possible sentences.
    """

    def wordBreak3(self, s: str, words: list):
        s = s.lower()
        words = set([i.lower() for i in words])
        # return self.recursion(s, words)
        return self.dp(s, words)

    # 枚举, Time Limit Exceeded
    def recursion(self, s: str, words):
        if not s:
            return 1
        ans = 0
        for w in words:
            if s.startswith(w):
                ans += self.recursion(s[len(w):], words)
        return ans

    # 动态规划
    def dp(self, s: str, words: set):
        size = len(s)
        dp = [0] * (size + 1)
        dp[0] = 1
        for i in range(1, size + 1):
            for w in words:
                w_size = len(w)
                if i - w_size >= 0 and s[i - w_size: i] == w:
                    # 子串的拼法组合而成
                    dp[i] += dp[i - w_size]
        return dp[-1]


#
words = ["a","aa","aaa","aaaa","aaaaa","aaaaaa","aaaaaaa","aaaaaaaa","aaaaaaaaa","aaaaaaaaaa"]
# 84675106
# 265816832
print(Solution().wordBreak3("aaaaaaaaaaaaaaaaaaaaaaaaaaaaa", words) == 265816832)

words = ["Cat", "mat", "Ca", "tm", "at", "C", "Dog", "og", "Do"]
print(Solution().wordBreak3("Catmat", words))
