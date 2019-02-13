#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
https://www.lintcode.com/problem/sum-root-to-leaf-numbers/description?_from=cat
描述
给定仅包含来自0-9的数字的二叉树，每个根到叶路径可以表示数字。举个例子：root-to-leaf路径1-> 2-> 3，它代表数字123，
找到所有根到叶的数的总和
<叶节点是没有子节点的节点>

Example:
Input: [1,2,3]
    1
   / \
  2   3
Output: 25
Explanation:
The root-to-leaf path 1->2 represents the number 12.
The root-to-leaf path 1->3 represents the number 13.
Therefore, sum = 12 + 13 = 25.
Example 2:

Input: [4,9,0,5,1]
    4
   / \
  9   0
 / \
5   1
Output: 1026
Explanation:
The root-to-leaf path 4->9->5 represents the number 495.
The root-to-leaf path 4->9->1 represents the number 491.
The root-to-leaf path 4->0 represents the number 40.
Therefore, sum = 495 + 491 + 40 = 1026.
"""


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None


class Solution:
    def __init__(self):
        self.sum = 0

    """
    @param root: the root of the tree
    @return: the total sum of all root-to-leaf numbers
    """
    def sumNumbers(self, root):
        self.sum = 0
        self.help(root, 0)
        return self.sum

    def help(self, root, nums):
        if not root:
            return
        nums = nums * 10 + root.val
        if not root.left and not root.right:
            self.sum += nums
        else:
            self.help(root.left, nums)
            self.help(root.right, nums)

root = TreeNode(1)
root.left = TreeNode(2)
# root.right = TreeNode(3)
print(Solution().sumNumbers(root))
