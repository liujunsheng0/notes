#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
完全二叉树 https://www.lintcode.com/problem/complete-binary-tree/description
判断一个二叉树是否是完全二叉树
"""


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None


class Solution:
    """
    @param root: the root of binary tree.
    @return: true if it is a complete binary tree, or false.
    """
    def isComplete(self, root):
        if not root:
            return True
        q = [root]
        times = 0
        while q:
            tmp = []
            for node in q:
                tmp.extend([node.left, node.right])
            ok = False
            for i in tmp:
                if ok and i is not None:
                    return False
                if not ok and i is None:
                    ok = True
                    times += 1
            # end for
            if times > 2:
                return False
            q = [i for i in tmp if i is not None]
        # end for
        return True

