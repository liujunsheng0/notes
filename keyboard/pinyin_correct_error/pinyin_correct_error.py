#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""
利用bktree进行拼音纠错
"""

import os

import pybktree


PWD = os.path.abspath(os.path.dirname(__file__))


def calculate_edit_distance(word1: str, word2: str) -> int:
    """
    计算编辑距离
    https://blog.csdn.net/qq_34552886/article/details/72556242
    :param word1: 字符串1
    :param word2: 字符串2
    :return: int, 编辑距离
    """
    if word1 is None and word2 is None:
        return 0
    if word1 is None or not word1:
        return len(word2)
    if word2 is None or not word2:
        return len(word1)
    len1, len2 = len(word1) + 1, len(word2) + 1
    dp = [[0] * len2 for _ in range(len1)]
    for i in range(len1):
        dp[i][0] = i
    for i in range(len2):
        dp[0][i] = i
    for i in range(1, len1):
        for j in range(1, len2):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
            # end if
        # end for
    # end for
    return dp[-1][-1]


class BkTreeWrapper(object):
    def __init__(self, distance_func=calculate_edit_distance):
        """
        :param distance_func: 计算编辑距离, 输入(str, str), 输出: int
        """
        self._bk = pybktree.BKTree(distance_func)

    def init(self):
        file = os.path.join(PWD, 'pinyins.txt')
        with open(file, encoding='utf-8') as f:
            for i in f:
                self._bk.add(i.strip())

    def add(self, word: str):
        if word:
            self._bk.add(word.lower())

    def find(self, word: str, max_edit_distance: int=2) -> list:
        """
        :param word: 查询字符串
        :param max_edit_distance: 最大编辑距离
        :return: list of (distance, item) tuples ordered by distance
        """
        if word is None:
            word = ''
        return self._bk.find(word.lower(), max_edit_distance)


if __name__ == '__main__':
    bk = BkTreeWrapper()
    bk.init()
    print(bk.find('shxng', max_edit_distance=2))
