#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
题目描述: 借教室, 平台: https://www.lintcode.com/problem/borrow-classroom/

参考博客:
        http://www.cnblogs.com/COLIN-LIGHTNING/p/8467795.html
        http://www.cnblogs.com/COLIN-LIGHTNING/p/8436624.html
        http://www.cnblogs.com/COLIN-LIGHTNING/p/8543330.html

在大学期间，经常需要租借教室。大到院系举办活动，小到学习小组自习讨论，都需要向学校申请借教室。教室的大小功能不同，
借教室人的身份不同，借教室的手续也不一样。面对海量租借教室的信息，我们自然希望编程解决这个问题。
我们需要处理接下来n天的借教室信息，其中第i天学校有ri个教室可供租借。共有m份订单，每份订单用三个正整数描述，分别为dj,sj,tj，
表示某租借者需要从第sj天到第tj天租借教室（包括第sj天和第tj天），每天需要租借dj个教室。我们假定，租借者对教室的大小、地点没有要求。
即对于每份订单，我们只需要每天提供dj个教室，而它们具体是哪些教室，每天是否是相同的教室则不用考虑。
借教室的原则是先到先得，也就是说我们要按照订单的先后顺序依次为每份订单分配教室。
如果在分配的过程中遇到一份订单无法完全满足，则需要停止教室的分配，通知当前申请人修改订单。
这里的无法满足指从第sj天到第tj天中有至少一天剩余的教室数量不足dj个。
现在我们需要知道，是否会有订单无法完全满足。如果有，需要通知哪一个申请人修改订单。
输入格式：
    第一行包含两个正整数n,m，表示天数和订单的数量。
    第二行包含n个正整数，其中第i个数为ri，表示第i天可用于租借的教室数量。
    接下来有m行，每行包含三个正整数dj,sj,tj，表示租借的数量，租借开始、结束分别在第几天。
    每行相邻的两个数之间均用一个空格隔开。天数与订单均用从1开始的整数编号。
输出格式：
    如果所有订单均可满足，则输出只有一行，包含一个整数 0。否则（订单无法完全满足）
    输出两行，第一行输出一个负整数-1，第二行输出需要修改订单的申请人编号。
"""


class Segment(object):
    def __init__(self, start, end, min_v=float('inf')):
        self.start, self.end, self.min_v = start, end, min_v
        self.left = self.right = None


def build_segment(r, start, end):
    if not r or start > end:
        return None
    if start == end:
        return Segment(start, end, r[start])
    node = Segment(start, end)
    mid = (start + end) // 2
    node.left = build_segment(r, start, mid)
    node.right = build_segment(r, mid + 1, end)
    node.min_v = min(node.left.min_v, node.right.min_v)
    return node


def modify(node: Segment, start, end, val):
    if start > end:
        return
    if start == node.start and end == node.end and start == end:
        node.min_v -= val
        return
    mid = (node.start + node.end) // 2
    if end <= mid:
        modify(node.left, start, end, val)
    elif start > mid:
        modify(node.right, start, end, val)
    else:
        modify(node.left, start, mid, val)
        modify(node.right, mid + 1, end, val)
    node.min_v = min(node.left.min_v, node.right.min_v)


def query(node, start, end):
    if start > end:
        return 0
    if start == node.start and end == node.end:
        return node.min_v
    mid = (node.start + node.end) // 2
    if end <= mid:
        return query(node.left, start, end)
    elif start > mid:
        return query(node.right, start, end)
    return min(query(node.left, start, mid), query(node.right, mid + 1, end))


class Solution:
    """
    @param r: the number of classrooms available for rent
    @param d: the number of classrooms you need to borrow
    @param s: the start day you borrow the classroom
    @param t: the end day you borrow the classroom
    @return: which applicant to modify the order
    """

    def getApplicant1(self, r, d, s, t):
        """ 简单粗暴的方法 时间复杂度:N * N"""
        size = len(r)
        for index, (rooms, start, end) in enumerate(zip(d, s, t)):
            if end > size:
                return False
            for i in range(start, end + 1):
                r[i - 1] -= rooms
                if r[i - 1] < 0:
                    return index + 1
                    # end for
        # end for
        return 0

    def getApplicant2(self, r, d, s, t):
        """ 线段树求解, 大概70%左右超时 时间复杂度: N * logN """
        node = build_segment(r, 0, len(r) - 1)
        # segment tree time: n * log(n)
        for idx, (room, start, end) in enumerate(zip(d, s, t)):
            modify(node, start - 1, end - 1, room)
            if node.min_v < 0:
                return idx + 1
        # end for
        return 0

    def is_valid(self, r, d, s, t, days, f, sum_):
        for idx in range(days):
            f[idx] = sum_[idx] = 0
        for room, start, end in zip(d, s, t):
            f[start - 1] += room
            f[end] -= room
        # end for
        sum_[0] = f[0]
        for i in range(days):
            if i > 0:
                sum_[i] = sum_[i - 1] + f[i]
            if sum_[i] > r[i]:
                return False
                # end if
        return True

    def getApplicant(self, r, d, s, t):
        """ 二分 + 差分数组, 大致90%超时, 时间复杂度N * logN, 应该是最优解了, 但是目前没有AC, 翻译成C++后AC通过 """
        size = len(r)
        sum_ = [0] * (size + 1)
        f = [0] * (size + 1)
        if self.is_valid(r, d, s, t, size, f, sum_):
            return 0
        left, right = 0, len(d)
        cache = {}
        while left < right:
            mid = (left + right) // 2
            ok = self.is_valid(r, d[:mid], s[:mid], t[:mid], size, f, sum_)
            cache[mid] = ok
            if not ok and cache.get(mid - 1, False):
                return mid
            if ok and not cache.get(mid + 1, True):
                return mid + 1
            if ok:
                left = mid + 1
            else:
                right = mid
        return left

    def trans_c(self):
        """
        // 差分数组, c++ 实现
        #include <cstdio>
        #include <iostream>
        #include <cstring>
        #include <cstdlib>
        #include <algorithm>


        class Solution {
        public:
            /**
             * @param r: the number of classrooms available for rent
             * @param d: the number of classrooms you need to borrow
             * @param s: the start day you borrow the classroom
             * @param t: the end day you borrow the classroom
             * @return: which applicant to modify the order
             */

            int getApplicant(vector<int> &r, vector<int> &d, vector<int> &s, vector<int> &t) {
                // Write your code here.
                int r_size = r.size();
                int d_size = d.size();
                int *sum = new int[r_size + 2];
                int *f = new int[r_size + 2];
                int left = 0;
                int right = d_size;

                while (left < right) {
                    int mid = (left + right) / 2;
                    for (int i = 0; i < r_size; i++){
                        sum[i] = 0;
                        f[i] = 0;
                    }
                    int ok = 1;

                    for(int i = 0; i < mid; i++) {
                        f[s[i] - 1] += d[i];
                        f[t[i]] -= d[i];
                    }

                    sum[0] = f[0];
                    for(int i = 0; i < r_size; i++) {
                        if (i > 0) {
                            sum[i] = sum[i - 1] + f[i];
                        }
                        if(sum[i] > r[i]) {
                            ok = 0;
                            break;
                        }
                    }
                    cout<<mid<<"   "<<ok<<endl;
                    if(ok == 1 && mid == d_size) {
                        return 0;
                    }
                    if(ok) {
                        left = mid + 1;
                    }
                    else {
                        right = mid;
                    }
                }
                delete []sum;
                delete []f;
                return left;
            }
        };
        """
        pass
