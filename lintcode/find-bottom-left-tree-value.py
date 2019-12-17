#!/usr/bin/python3.6
# -*- coding: utf-8 -*-


"""
https://www.lintcode.com/problem/find-bottom-left-tree-value/description
给定一棵二叉树, 找到这棵树最中最后一行中最左边的值.
输人:{1,2,3,4,5,6,#,#,7}
输出:7
解释：
         1
        /  \
      2     3
    /  \    /
  4     5  6
   \
    7
"""


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None


class Solution:
    """
    @param root: a root of tree
    @return: return a integer
    """
    def findBottomLeftValue(self, root: TreeNode):
        return self.help(root, 0, root)[0]

    # 还可以用层次遍历
    def help(self, root: TreeNode, depth: int, parent: TreeNode):
        """
        :param root: root节点
        :param depth: 当前节点的高度
        :param parent: 父节点
        :return: 当前最坐的值和当前高度
        """
        if root is None:
            return parent.val, depth
        v1, d1 = self.help(root.left, depth + 1, root)
        v2, d2 = self.help(root.right, depth + 1, root)
        return (v1, d1) if d1 >= d2 else (v2, d2)


if __name__ == '__main__':
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    print(Solution().help(root, 0, root))
