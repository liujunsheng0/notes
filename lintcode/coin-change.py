#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""
描述: https://www.lintcode.com/problem/coin-change/description
给出不同面额的硬币以及一个总金额. 写一个方法来计算给出的总金额可以换取的最少的硬币数量. 如果已有硬币的任意组合均无法与总金额面额相等, 那么返回 -1.
你可以假设每种硬币均有无数个
"""


class Solution1:
    """
    @param coins: a list of integer
    @param amount: a total amount of money amount
    @return: the fewest number of coins that you need to make up
    """

    def coinChange(self, coins, amount):
        if amount < 1:
            return 0 if amount == 0 else -1

        dp = [amount + 1] * (amount + 1)
        dp[0] = 0
        for i in range(1, amount + 1):
            for c in coins:
                if i - c >= 0 and dp[i - c] != amount + 1:
                    dp[i] = min(dp[i - c] + 1, dp[i])
                if dp[i] == 1:
                    break
        return dp[-1] if dp[-1] != amount + 1 else -1


print(Solution1().coinChange([1, 2, 5], 11))

"""
给出不同面额的硬币以及一个总金额, 写一个方法来计算给出的总金额可以换取的最少的硬币数量.
要求
    1.硬币的价值总和是所有组合中最小的, 并且大于等于总金额
    2.基于1的条件下, 要求硬币个数尽可能少,
"""


class Solution2:
    """
    @param coins: a list of integer
    @param amount: a total amount of money amount
    @return: the fewest number of coins that you need to make up
    """

    def coinChange(self, coins, amount):
        if amount < 1:
            return 0 if amount == 0 else -1

        # member = (最小硬币个数, 前一次位置, 本次货币)
        dp = [None] * (amount + 1)
        dp[0] = [0, 0]
        i = 1
        while dp[-1] is None or i < amount + 1:
            if i > amount:
                dp.append(None)
            for c in coins:
                if c == i:
                    dp[i] = (1, 0, c)
                    break
                elif i - c >= 0 and dp[i - c] is not None:
                    if dp[i] is None or dp[i - c][0] + 1 < dp[i][0]:
                        dp[i] = (dp[i - c][0] + 1, i - c, c)
            # end for
            i += 1
        # end while
        i = dp[-1][1]
        ans = [dp[-1][2]]
        while i > 0:
            ans.append(dp[i][2])
            i = dp[i][1]
        # end for
        return ans


print(Solution2().coinChange([30, 40, 70], 111))
