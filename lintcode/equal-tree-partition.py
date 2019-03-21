#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
相等树划分 https://www.lintcode.com/problem/equal-tree-partition/description
给定一个有 n个节点的二叉树，请问可否在去掉恰好一条边的情况下，将原有的树分成两个节点值总和相等的两个树。
输入: {5,10,10,#,#,2,3}
输出: true
解释:
  原始的树:
     5
    / \
   10 10
     /  \
    2    3
  两棵子树:
     5       10
    /       /  \
   10      2    3
"""


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None


class Solution:
    """
    @param root: a TreeNode
    @return: return a boolean
    """
    def checkEqualTree(self, root):
        sum_ = self.get_sum(root)
        if sum_ & 1 > 0:
            return False
        return self.help(root, sum_, True)

    def get_sum(self, root):
        if not root:
            return 0
        return root.val + self.get_sum(root.left) + self.get_sum(root.right)

    def help(self, root, sum_, is_root):
        if not root:
            return False
        left_sum = self.get_sum(root.left)
        right_sum = self.get_sum(root.right)
        if not root.left and not root.right:
            if sum_ == 2 * root.val:
                return True
            return False
        else:
            if sum_ in (2 * left_sum, 2 * right_sum) or (not is_root and sum_ == 2 * (left_sum + root.val + right_sum)):
                return True
        return self.help(root.left, sum_, False) or self.help(root.right, sum_, False)

    def betterAnswer(self, root):
        d = {}
        sum_ = self.get_sum2(root, d)
        d[sum_] -= 1
        return sum_ & 1 == 0 and d.get(sum_ / 2, 0) > 0

    def get_sum2(self, root, d):
        if not root:
            return 0
        sum_ = root.val + self.get_sum2(root.left, d) + self.get_sum2(root.right, d)
        d[sum_] = d.get(sum_, 0) + 1
        return sum_

node = TreeNode(5)
node.left = TreeNode(10)
node.right = TreeNode(-10)
node.right.left = TreeNode(-3)
node.right.right = TreeNode(-2)

print(Solution().checkEqualTree(node))
print(Solution().betterAnswer(node))
