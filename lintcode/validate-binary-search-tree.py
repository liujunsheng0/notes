#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
https://www.lintcode.com/problem/validate-binary-search-tree/description
给定一个二叉树，判断它是否是合法的二叉查找树(BST) -> ******* 中序遍历是升序 *****
一棵BST定义为：
    节点的左子树中的值要严格小于该节点的值。
    节点的右子树中的值要严格大于该节点的值。
    左右子树也必须是二叉查找树。
    一个节点的树也是二叉查找树。
"""

"""
Definition of TreeNode:
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None
"""


class Solution:
    """
    @param root: The root of binary tree.
    @return: True if the binary tree is BST, or false
    """
    def isValidBST(self, root):
        self.ans = True
        self.last_val = float('-inf')
        self.help(root)
        return self.ans

    def help(self, root):
        """ 中序遍历二叉查找树时, 升序 """
        if root:
            self.help(root.left)
            if root.val <= self.last_val:
                self.ans = False
                return
            self.last_val = root.val
            self.help(root.right)

