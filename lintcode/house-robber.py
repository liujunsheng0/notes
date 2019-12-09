#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""
https://www.lintcode.com/problem/house-robber/description
假设你是一个专业的窃贼, 准备沿着一条街打劫房屋. 每个房子都存放着特定金额的钱. 
你面临的唯一约束条件是: 相邻的房子装着相互联系的防盗系统, 且 当相邻的两个房子同一天被打劫时, 该系统会自动报警. 
给定一个非负整数列表, 表示每个房子中存放的钱,  算一算, 如果今晚去打劫, 在不触动报警装置的情况下, 你最多可以得到多少钱 . 
"""


class Solution:
    def houseRobber(self, a):
        """
        @param a: An array of non-negative integers
        @return: The maximum amount of money you can rob tonight
        """
        size = len(a)
        if size < 3:
            return max(a) if a else 0
        dp = [0] * size
        dp[0] = a[0]
        dp[1] = max(a[:2])
        for i in range(2, size):
            dp[i] = max(dp[i - 1], dp[i - 2] + a[i])
        return dp[-1]


"""
https://www.lintcode.com/problem/house-robber-ii/description
在上次打劫完一条街道之后, 窃贼又发现了一个新的可以打劫的地方, 但这次所有的房子围成了一个圈, 
这就意味着第一间房子和最后一间房子是挨着的. 每个房子都存放着特定金额的钱. 你面临的唯一约束条件是:相邻的房子装着相互联系的防盗系统, 
且当相邻的两个房子同一天被打劫时, 该系统会自动报警. 
给定一个非负整数列表, 表示每个房子中存放的钱,  算一算, 如果今晚去打劫, 在不触动报警装置的情况下, 你最多可以得到多少钱 . 
"""


class Solution:
    """
    @param nums: An array of non-negative integers.
    @return: The maximum amount of money you can rob tonight
    """
    def solution(self, a):
        size = len(a)
        if size < 3:
            return max(a) if a else 0
        dp = [0] * size
        dp[0] = a[0]
        dp[1] = max(a[:2])
        for i in range(2, size):
            dp[i] = max(dp[i - 1], dp[i - 2] + a[i])
        return dp[-1]

    def houseRobber2(self, nums):
        if len(nums) < 3:
            return max(nums) if nums else 0
        return max((self.solution(nums[:-1]), self.solution(nums[1:])))


"""
https://www.lintcode.com/problem/house-robber-iii/description
在上次打劫完一条街道之后和一圈房屋之后, 窃贼又发现了一个新的可以打劫的地方, 但这次所有的房子组成的区域比较奇怪, 
聪明的窃贼考察地形之后, 发现这次的地形是一颗二叉树. 与前两次偷窃相似的是每个房子都存放着特定金额的钱. 
你面临的唯一约束条件是:相邻的房子装着相互联系的防盗系统, 且当相邻的两个房子同一天被打劫时, 该系统会自动报警. 
算一算, 如果今晚去打劫, 你最多可以得到多少钱, 当然在不触动报警装置的情况下
PS: 数值均为正数
"""


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None


class Solution:

    def __init__(self):
        self.cache = {}

    def houseRobber3(self, root: TreeNode):
        """
        节点中的值均 > 0
        @param root: The root of binary tree.
        @return: The maximum amount of money you can rob tonight
        """
        if not root:
            return 0
        if root in self.cache:
            return self.cache[root]

        # 根节点 + 左右子树中的最大值
        v1 = root.val
        if root.left:
            # root + 左子节点的左右子节点
            v1 += self.houseRobber3(root.left.left)
            v1 += self.houseRobber3(root.left.right)
        if root.right:
            # root + 右子节点的左右子节点
            v1 += self.houseRobber3(root.right.left)
            v1 += self.houseRobber3(root.right.right)

        # 左子节点 + 右子节点
        v2 = self.houseRobber3(root.left) + self.houseRobber3(root.right)
        v = max(v1, v2)
        self.cache[root] = v
        return v

