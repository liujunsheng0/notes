#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
给定一棵二叉树，统计唯一值子树的数目. https://www.lintcode.com/problem/count-univalue-subtrees/description
唯一值子树意味着子树的所有节点都具有相同的值.

给定二叉树 = {5,1,5,5,5,#,5}, 返回 4.
      5
     / \
    1   5      三个叶子节点 + 5-5(根节点的又孩子)
   / \   \
  5   5   5
"""


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None


class Solution:
    def __init__(self):
        self.ans = 0
    """
    @param root: the given tree
    @return: the number of uni-value subtrees.
    """
    def countUnivalSubtrees(self, root):
        self.ans = 0
        self.help(root)

    def help(self, root):
        if not root:
            return True
        ok = True
        if root.left:
            ok = self.help(root.left) and (root.val == root.left.val)
        if root.right:
            ok = self.help(root.right) and (root.val == root.right.val)
        if ok:
            self.ans += 1
        return ok
