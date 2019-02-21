#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
会议室 II https://www.lintcode.com/problem/meeting-rooms-ii/description
给定一系列的会议时间间隔intervals，包括起始和结束时间[[s1,e1],[s2,e2],...] (si < ei)，找到所需的最小的会议室数量。

输入：intervals = [(0,30),(5,10),(15,20)], 返回2
"""

from collections import defaultdict


class Interval(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Solution:
    """
    @param intervals: an array of meeting time intervals
    @return: the minimum number of conference rooms required
    """

    def minMeetingRooms1(self, intervals):
        """ 粗暴, 超时 """
        d = defaultdict(int)
        for i in intervals:
            for j in range(i.start, i.end + 1):
                d[j] += 1
        return max(d.values())

    def minMeetingRooms(self, intervals):
        """ 起点 + 1, 终点 - 1"""
        points = []
        for interval in intervals:
            points.append([interval.start, 1])
            points.append([interval.end, -1])
        points = sorted(points, key=lambda x: x[0])
        ans = cur = 0
        for i in range(len(points)):
            cur += points[i][1]
            ans = max(ans, cur)
        return ans


print(Solution().minMeetingRooms([Interval(5, 8), Interval(6, 8)]))
