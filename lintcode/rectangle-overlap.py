#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
矩形重叠 https://www.lintcode.com/problem/rectangle-overlap/description

给定两个矩形，判断这两个矩形是否有重叠。

l1代表第一个矩形的左上角
r1代表第一个矩形的右下角
l2代表第二个矩形的左上角
r2代表第二个矩形的右下角
保证：l1 != r2 并且 l2 != r2

输入 : l1 = [0, 8], r1 = [8, 0], l2 = [6, 6], r2 = [10, 0] 输出 : true
输入 : [0, 8], r1 = [8, 0], l2 = [9, 6], r2 = [10, 0]      输出 : false
"""


class Point:
    def __init__(self, a=0, b=0):
        self.x = a
        self.y = b


class Solution:
    """
    @param l1: top-left coordinate of first rectangle
    @param r1: bottom-right coordinate of first rectangle
    @param l2: top-left coordinate of second rectangle
    @param r2: bottom-right coordinate of second rectangle
    @return: true if they are overlap or false
    """

    def doOverlap(self, l1: Point, r1: Point, l2: Point, r2: Point):
        """由于这里矩形都是与坐标轴平行的, 所以分别投影到x轴与y轴, 判断投影后的线段是否重合即可"""
        return max(l1.x, l2.x) <= min(r1.x, r2.x) and max(r1.y, r2.y) <= min(l1.y, l2.y)


print(Solution().doOverlap(Point(0, 8), Point(8, 0), Point(6, 6), Point(10, 0)) == True)
print(Solution().doOverlap(Point(0, 8), Point(8, 0), Point(9, 6), Point(10, 0)) == False)
print(Solution().doOverlap(Point(0, 5), Point(8, 3), Point(8, 3), Point(10, 0)) == True)
print(Solution().doOverlap(Point(-1, 10), Point(10, 5), Point(5, 15), Point(12, 11)) == False)
