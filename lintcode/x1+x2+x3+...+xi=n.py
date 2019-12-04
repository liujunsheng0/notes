#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""
多元一次不定方程解的个数

problem1: s将30条鱼放入10个桶中, 每个桶至少一条鱼, 总共有多少种方法?
本质:
    x1 + x2 + x3 + x4 + ... + xi = n, xi > 0, n > i
    本题:  x1 + x2 + x3 + x4 + ... + x9 + x10 = 30, x1~x10　> 0

解答: 隔板法, 每条鱼可以视为数值1, 插入板子后将1相加
            n条鱼排一列,　板子能放的位置是 = n - 1
            要i个数, 需要插入 i - 1个板子
            所求即为板子的位置, so答案为排列组合, C(n - 1, i - 1), 板子顺序没关系

     扩展1: 当xi >= 0时
        x1 + x2 + ... + xi = n的非负整数解个数与 y1 + y2 + ... + yi = n + i (yi = xi+1, i=[1,r]) 的正整数解个数是相同的
        所以答案为 C(n + i - 1, i - 1)
     扩展2: x1 >= -2, x2... > 0
        x1 + x2 + ... + xi = n的整数解个数与 y1 = x1 + 3, y1 + x2 + ... + xi = n + 3的正整数解的个数
        所以答案为C(n + 3 - 1, i - 1)

problem2: 将30条鱼放入10个桶中, 每个桶可以放0-10条, 总共有多少种方法?
本质:
    x1 + x2 + x3 + x4 + ... + xi = n, 0 <= xi <= 10
    本题:  x1 + x2 + x3 + x4 + ... + x9 + x10 = 30, 0 <= x1~x10 <= 10

"""


class Problem2(object):
    @classmethod
    def solution1(cls, box, fish, max_fish_num: int = 10):
        """ 递归 """
        if fish < 0 or box < 0 or (box < 1 and fish > 0):
            return 0
        if box == 0 and fish == 0:
            return 1
        if box == 1:
            return int(fish <= max_fish_num)
        ans = 0
        for i in range(0, max_fish_num + 1):
            ans += cls.solution1(box - 1, fish - i, max_fish_num=max_fish_num)
        return ans

    @classmethod
    def solution2(cls, box, fish, max_fish_num: int = 10):
        """ 动态规划 """
        if fish < 0 or box < 0 or (box < 1 and fish > 0):
            return 0
        if box == 0 and fish == 0:
            return 1
        if box == 1:
            return int(fish <= max_fish_num)

        # row = fish, col = box
        box += 1  # 盒子和球的个数都为0的时候
        dp = [[0] * box for _ in range(fish + 1)]
        dp[0] = [1] * box
        for i in range(1, fish + 1):  # row 鱼的数量
            for j in range(1, box):   # col 桶的数量
                tmp = 0
                for m in range(0, max_fish_num + 1):
                    if i - m < 0:
                        break
                    # 少的那个桶放0~max_fish_num个鱼
                    tmp += dp[i - m][j - 1]
                # end for
                dp[i][j] = tmp
            # end for
        # end for

        return dp[-1][-1]

    @staticmethod
    def help(m, n):
        ans = 1
        for i in range(m, m - n, -1):
            ans *= i
        for i in range(1, n + 1):
            ans /= i
        return ans


if __name__ == '__main__':
    for a, b in [[5, 15], [4, 18], [5, 30]]:
        print(a, b, "=>", Problem2.solution1(a, b), Problem2.solution2(a, b))