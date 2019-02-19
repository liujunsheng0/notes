#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
对称二叉树 判断 二叉树 是否是对称二叉树 https://www.lintcode.com/problem/symmetric-binary-tree/description
"""


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None


class Solution:
    """
    @param root: the root of binary tree.
    @return: true if it is a mirror of itself, or false.
    """
    def isSymmetric(self, root):
        if not root:
            return True
        return self.compare(root.left, root.right)

    def compare(self, n1, n2):
        if (n1 is None and n2 is not None) or (n1 is not None and n2 is None):
            return False
        if n1 is None and n2 is None:
            return True
        if n1.val != n2.val:
            return False
        # 因为对称, 左侧节点的左孩子 == 右侧节点的右孩子, 左侧节点的右孩子 == 右侧节点的左孩子
        return self.compare(n1.left, n2.right) and self.compare(n1.right, n2.left)
