#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
查询区间 https://www.lintcode.com/problem/interval-search/description?_from=ladder&&fromId=62
给定一个包含若干个区间的List数组, 区间的长度是 1000, 例如 [500,1500], [2100,3100].给定一个 number ,
请问number是否在这些区间内.返回 True 或 False.

输入: List = [[100,1100],[1000,2000],[5500,6500]] 和 number = 6000
输出: true
解释: 6000 在区间[5500,6500]里

样例2
输入: List = [[100,1100],[2000,3000]] 和 number = 3500
输出: false
解释:
3500不在list的任何一个区间中
"""


class Solution:
    """
    @param intervalList:
    @param number:
    @return: return True or False
    """
    def isInterval(self, intervalList, number):
        for s, e in intervalList:
            if s <= number <= e:
                return True
        return False
