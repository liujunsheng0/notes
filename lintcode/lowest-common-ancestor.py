#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
最近公共祖先 https://www.lintcode.com/problem/lowest-common-ancestor-of-a-binary-tree/description
给定一棵二叉树，找到两个节点的最近公共父节点(LCA)。最近公共祖先是两个节点的公共的祖先节点。
注意：假设给出的两个节点都在树中存在
对于下面这棵二叉树
  4
 / \
3   7
   / \
  5   6
LCA(3, 5) = 4, LCA(5, 6) = 7, LCA(6, 7) = 7
"""


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None


class Solution1:
    """
    @param: root: The root of the binary tree.
    @param: A: A TreeNode in a Binary.
    @param: B: A TreeNode in a Binary.
    @return: Return the least common ancestor(LCA) of the two nodes.
    """

    def lowestCommonAncestor(self, root, A, B):
        if root is None:
            return None
        if root is A or root is B:
            return root
        left = self.lowestCommonAncestor(root.left, A, B)
        right = self.lowestCommonAncestor(root.right, A, B)
        # A在左右两侧, 则root为重合点
        if left and right:
            return root
        # 只在左侧
        if left:
            return left
        # 只在右侧
        if right:
            return right
        return None


a = TreeNode(1)
b = TreeNode(2)
c = TreeNode(3)
d = TreeNode(4)
a.left, a.right = b, c
b.left = d

# print(Solution1().lowestCommonAncestor(a, d, b).val)


"""
最近公共祖先 II  https://www.lintcode.com/problem/lowest-common-ancestor-ii/description
给一棵二叉树和二叉树中的两个节点，找到这两个节点的最近公共祖先LCA。
两个节点的最近公共祖先，是指两个节点的所有父亲节点中（包括这两个节点），离这两个节点最近的公共的节点。
每个节点除了左右儿子指针以外，还包含一个父亲指针parent，指向自己的父亲。

例1：
输入：
       4
      / \
     3  7
        / \
       5  6
3,5
输出：4
说明：LCA（3,5）= 4

例2：
输入：
       4
      / \
     3  7
        / \
       5  6
和5,6
输出：7
说明：LCA（5,6）= 7
"""


class ParentTreeNode:
    def __init__(self, val):
        self.val = val
        self.parent, self.left, self.right = None, None, None


class Solution2:
    """
    @param: root: The root of the tree
    @param: A: node in the tree
    @param: B: node in the tree
    @return: The lowest common ancestor of A and B
    """
    def get_len(self, node: ParentTreeNode):
        size = 0
        while node:
            node = node.parent
            size += 1
        return size

    def lowestCommonAncestorII(self, root, A, B):
        """ 树变链表 -> 重合点 """
        len_a, len_b = self.get_len(A), self.get_len(B)
        if len_a > len_b:
            A, B = B, A
            len_a, len_b = len_b, len_a
        while len_b > len_a:
            B = B.parent
            len_b -= 1
        while len_a > 0:
            if A is B:
                return A
            A, B = A.parent, B.parent
            len_a -= 1
        # end while
        return root


"""
最近公共祖先 III
给一棵二叉树和二叉树中的两个节点，找到这两个节点的最近公共祖先LCA。
两个节点的最近公共祖先，是指两个节点的所有父亲节点中（包括这两个节点），离这两个节点最近的公共的节点。
返回 null 如果两个节点在这棵树上不存在最近公共祖先的话。

  4
 / \
3   7
   / \
  5   6
LCA(3, 5) = 4
LCA(5, 6) = 7
LCA(6, 7) = 7
LCA(5, 8) = null
注意事项 <这两个节点未必都在这棵树上出现>
"""


class Solution3:
    """
    @param: root: The root of the binary tree.
    @param: A: A TreeNode
    @param: B: A TreeNode
    @return: Return the LCA of the two nodes.
    """
    def lowestCommonAncestor3(self, root, A, B):
        ans = self.lowestCommonAncestor(root, A, B)
        l = self.help(ans)
        return ans if A in l and B in l else None

    def lowestCommonAncestor(self, root, A, B):
        if root is None:
            return None
        if root is A or root is B:
            return root
        left = self.lowestCommonAncestor(root.left, A, B)
        right = self.lowestCommonAncestor(root.right, A, B)
        if left and right:
            return root
        if left:
            return left
        if right:
            return right
        return None

    def help(self, root):
        return [root] + self.help(root.left) + self.help(root.right) if root else []

ans = Solution3().lowestCommonAncestor3(a, b, 11)
print(ans.val if ans else None)
