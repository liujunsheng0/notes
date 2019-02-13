#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
单词接龙 II (https://www.lintcode.com/problem/word-ladder-ii/description)
给出两个单词（start和end）和一个字典，找出所有从start到end的最短转换序列。

变换规则如下：
    每次只能改变一个字母。
    变换过程中的中间单词必须在字典中出现。
    所有单词具有相同的长度。
    所有单词都只包含小写字母。
给出数据如下：
    start = "hit"
    end = "cog"
    dict = ["hot","dot","dog","lot","log"]
返回 [ ["hit","hot","dot","dog","cog"], ["hit","hot","lot","log","cog"] ]
"""


# TODO:: 未AC
class Solution:
    """
    @param: start: a string
    @param: end: a string
    @param: dict: a set of string
    @return: a list of lists of string
    """

    def __init__(self):
        self.ans = []

    def findLadders1(self, start, end, words):
        """  超时 """
        if len(start) != len(end) or start == end or not words:
            return []
        self.ans = []
        self.help(start, end, set(words), {start: 1, end: 1}, [start])
        return self.ans

    def help(self, start, end, words, visited, path):
        if start == end:
            if not self.ans or len(path) == len(self.ans[0]):
                self.ans.append(path)
            elif len(path) < len(self.ans[0]):
                self.ans = [path]
            # end if
            return
        # end if
        if self.ans and len(path) >= len(self.ans[0]):
            return
        for i in range(len(start)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                tmp = start[:i] + c + start[i + 1:]
                if (tmp in words and visited.get(tmp, 0) == 0) or tmp == end:
                    visited[tmp] = 1
                    self.help(tmp, end, words, visited, path + [tmp])
                    visited[tmp] = 0
                # end if
            # end for
        # end for

    def findLadders(self, start, end, words):
        """ 内存溢出... """
        size = len(start)
        if size != len(end) or start == end or not words:
            return []
        words = set(words)
        words.add(end)
        q = [[start, [start], {start: 1}]]
        while q:
            qq = []
            for word, path, visited in q:
                for i in range(size):
                    for c in 'abcdefghijklmnopqrstuvwxyz':
                        tmp = word[:i] + c + word[i + 1:]
                        if tmp in words and visited.get(tmp, 0) == 0:
                            qq.append([tmp, path + [tmp], dict(visited)])
                        # end if
                    # end for
                # end for
            # end for
            ans = []
            for word, path, _ in qq:
                if word == end:
                    ans.append(path)
            if ans:
                return ans
            q = qq
        # end while
        return []


start1 = "hit"
end1 = "cog"
dict1 = set(["hot","dot","dog","lot","log"])
for p in Solution().findLadders(start1, end1, dict1):
    print('1', p)
