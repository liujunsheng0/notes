#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
二叉搜索树中第K小的元素 https://leetcode-cn.com/classic/problems/kth-smallest-element-in-a-bst/description/
给定一个二叉搜索树，编写一个函数 kthSmallest 来查找其中第 k 个最小的元素。
说明：
你可以假设 k 总是有效的，1 ≤ k ≤ 二叉搜索树元素个数。

示例 1:

输入: root = [3,1,4,null,2], k = 1
   3
  / \
 1   4
  \
   2
输出: 1
示例 2:

输入: root = [5,3,6,2,4,null,null,1], k = 3
       5
      / \
     3   6
    / \
   2   4
  /
 1
输出: 3
"""


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def kthSmallest(self, root: TreeNode, k: int) -> int:
        if k < 1:
            return None
        self.k = k
        return self.help(root)

    def help(self, root):
        if root:
            ret = self.help(root.left)
            if ret is not None:
                return ret
            if self.k == 1:
                return root.val
            self.k -= 1
            ret = self.help(root.right)
            if ret is not None:
                return ret
        return None
