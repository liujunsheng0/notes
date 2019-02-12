#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
描述: https://www.lintcode.com/problem/best-time-to-buy-and-sell-stock/description
假设有一个数组，它的第i个元素是一支给定的股票在第i天的价格。如果你最多只允许完成一次交易(例如,一次买卖股票),设计一个算法来找出最大利润。

输入：[3,2,3,1,2]
输出：1
解释：1买2卖，最大利润为1
"""


class Solution1:
    """
    @param prices: Given an integer array
    @return: Maximum profit
    """

    def maxProfit(self, prices):
        # write your code here
        size = len(prices)
        if size < 2:
            return 0
        ans, max_v, min_v = 0, prices[0], prices[0]
        for v in prices[1:]:
            if v > max_v:
                max_v = v
                ans = max(ans, max_v - min_v)
            elif v < min_v:
                min_v = v
                max_v = 0
                # end if
        # end for
        return ans


"""
https://www.lintcode.com/problem/best-time-to-buy-and-sell-stock-ii/description
假设有一个数组，它的第i个元素是一个给定的股票在第i天的价格。设计一个算法来找到最大的利润。
你可以完成尽可能多的交易(多次买卖股票)。然而,你不能同时参与多个交易(你必须在再次购买前出售股票)。

输入：[2,1,2,0,1]
输出：2
解释：1买2卖 0买1卖

输入：[1,2,8,10]
输出：9
解释：1买10卖

"""


class Solution2:
    """
    @param prices: Given an integer array
    @return: Maximum profit
    https://www.cnblogs.com/theskulls/p/5284143.html
    """

    def maxProfit(self, prices):
        ans = 0
        for i in range(len(prices) - 1):
            if prices[i] < prices[i + 1]:
                ans += (prices[i + 1] - prices[i])
        return ans


"""
描述 https://www.lintcode.com/problem/best-time-to-buy-and-sell-stock-iii/description
假设你有一个数组，它的第i个元素是一支给定的股票在第i天的价格。设计一个算法来找到最大的利润。你最多可以完成两笔交易。
不可以同时参与多笔交易，必须在再次购买前出售掉之前的股票

样例
输入：[4,4,6,1,1,4,2,5]
输出：6
解释：1买4卖  2买5卖
"""


class Solution3:
    """
    param prices: Given an integer array
    return: Maximum profit
    """

    def help(self, prices):
        size = len(prices)
        if size < 2:
            return 0
        ans, max_v, min_v = 0, prices[0], prices[0]
        for v in prices[1:]:
            if v > max_v:
                max_v = v
                ans = max(ans, max_v - min_v)
            elif v < min_v:
                min_v = v
                max_v = 0
                # end if
        # end for
        return ans

    def maxProfit(self, prices):
        """ O(n^2) 超时"""
        ans = 0
        for i in range(len(prices)):
            ans1 = self.help(prices[:i])
            ans2 = self.help(prices[i:])
            ans = max(ans, ans1 + ans2)
        # end for
        return ans
    # https://cloud.tencent.com/developer/article/1019199

print(Solution3().maxProfit([1, 2, 4, 2, 5, 7, 2, 4, 9, 0]))
