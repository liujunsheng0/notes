#!/usr/bin/python3.6
# -*- coding: utf-8 -*-


"""
https://www.lintcode.com/problem/binary-tree-paths/description
给一棵二叉树, 找出从根节点到叶子节点的所有路径.
输入：{1,2,3,#,5}
输出：["1->2->5","1->3"]
解释：
   1
 /   \
2     3
 \
  5
样例 2:

输入：{1,2}
输出：["1->2"]
解释：
   1
 /
2
"""


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None


class Solution:
    def __init__(self):
        self.ans = []
    """
    @param root: the root of the binary tree
    @return: all root-to-leaf paths
    """
    def binaryTreePaths(self, root: TreeNode):
        self.ans = []
        self.help(root, [])
        return self.ans

    def help(self, root, paths):
        if root is None:
            return
        paths += [root.val]
        if root.left is None and root.right is None:
            return self.ans.append("->".join([str(i) for i in paths]))
        self.help(root.left, list(paths))
        self.help(root.right, list(paths))


if __name__ == '__main__':
    n1 = TreeNode(1)
    n2 = TreeNode(2)
    n3 = TreeNode(3)
    n5 = TreeNode(5)
    n1.left, n1.right = n2, n3
    n2.right = n5
    print(Solution().binaryTreePaths(n1))
