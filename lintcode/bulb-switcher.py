"""
描述  https://www.lintcode.com/problem/bulb-switcher/description
起初这 n 个灯泡都是关闭状态。首先你把所有灯泡都打开。然后，每隔一个灯泡关闭下一个灯泡。在第三回合，每隔两个灯泡转换下一个
灯泡的状态（如果原先是关闭状态就打开，反之则关闭）。对于第 i回合，每隔i - 1 个灯泡，转换下一个灯泡的状态。
对于第 n 回合，只需要转换最后一个灯泡的状态。在 n 回合之后，还有多少灯泡亮着。

样例:

给出 n = 5.
起初，五个灯泡的状态是       [off, off, off, off, off].
第一回合之后，五个灯泡状态是 [on,  on,  on,  on,  on].   12345
第二回合之后，五个灯泡状态是 [on,  off, on,  off, on].   24
第三回合之后，五个灯泡状态是 [on,  off, off, off, on].   3
第四回合之后, 五个灯泡状态是 [on,  off, off, on,  on].   4
第五回合之后, 五个灯泡状态是 [on,  off, off, on,  off].  5
所以你应该返回 2, 因为只有两个灯泡是开着的。
"""


class Solution:
    """
    @param n: a Integer
    @return: how many bulbs are on after n rounds
    """
    def bulbSwitch(self, n):
        # http://www.cnblogs.com/grandyang/p/5100098.html
        pass
