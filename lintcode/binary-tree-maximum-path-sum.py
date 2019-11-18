#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""
描述: https://www.lintcode.com/problem/binary-tree-maximum-path-sum/description
给出一棵二叉树, 寻找一条路径使其路径和最大, 路径可以在任一节点中开始和结束(路径和为两个节点之间所在路径上的节点权值之和)
ps: 注意负数!!!

"""


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None


class Solution:
    """
    @param root: The root of binary tree.
    @return: An integer
    """

    def __init__(self):
        self.ans = None
        self.max_val = None  # 节点中的最大值

    def maxPathSum(self, root: TreeNode):
        if root is None:
            return 0
        self.ans = self.max_val = root.val
        self._maxPathSum(root)
        if self.max_val < 0:
            return self.max_val
        return self.ans

    def _maxPathSum(self, root: TreeNode):
        if root is None:
            return 0
        self.max_val = max(self.max_val, root.val)
        sum1 = self._maxPathSum(root.left)
        sum2 = self._maxPathSum(root.right)
        ans = max(self.ans,
                  root.val,
                  sum1,
                  sum2,
                  root.val + sum1,
                  root.val + sum2,
                  root.val + sum1 + sum2)
        if ans > self.ans:
            self.ans = ans
        return max(0, root.val + sum1, root.val + sum2)
