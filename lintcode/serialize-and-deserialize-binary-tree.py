#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
描述
设计一个算法，并编写代码来序列化和反序列化二叉树。将树写入一个文件被称为“序列化”，读取文件后重建同样的二叉树被称为“反序列化”。
如何反序列化或序列化二叉树是没有限制的，你只需要确保可以将二叉树序列化为一个字符串，并且可以将字符串反序列化为原来的树结构。
对二进制树进行反序列化或序列化的方式没有限制，LintCode将您的serialize输出作为deserialize的输入，它不会检查序列化的结果。

样例
给出一个测试数据样例， 二叉树{3,9,20,#,#,15,7}，表示如下的树结构：

  3
 / \
9  20
  /  \
 15   7
我们的数据是进行BFS遍历得到的。当你测试结果wrong answer时，你可以作为输入调试你的代码。

你可以采用其他的方法进行序列化和反序列化。
"""


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None

import json


class Solution:
    """
    @param root: An object of TreeNode, denote the root of the binary tree.
    This method will be invoked first, you should design your own algorithm
    to serialize a binary tree which denote by a root node to a string which
    can be easily deserialized by your own "deserialize" method later.
    """
    def serialize(self, root):
        """ 层次遍历 """
        if not root:
            return '[]'
        q = [root]
        ans = []
        while q:
            ans.append([i.val if i else '#' for i in q])
            tmp = []
            for i in q:
                tmp.extend([i.left, i.right] if i else [None, None])
            # end for
            q = tmp if any(tmp) else []
        # end while
        return json.dumps(ans)
    """
    @param data: A string serialized by your serialize method.
    This method will be invoked second, the argument data is what exactly
    you serialized at method "serialize", that means the data is not given by
    system, it's given by your own serialize method. So the format of data is
    designed by yourself, and deserialize it here as you serialize it in
    "serialize" method.
    """
    def deserialize(self, data):
        q = json.loads(data)
        if not q:
            return None
        root = TreeNode(q[0][0])
        roots = [root]
        for nodes in q[1:]:
            tmp = []
            size = len(nodes)
            for idx, head in enumerate(roots):
                if head and 2 * idx < size and nodes[2 * idx] != '#':
                    node = TreeNode(nodes[2 * idx])
                    head.left = node
                    tmp.append(node)
                else:
                    tmp.append(None)
                # end if
                if head and (2 * idx + 1) < size and nodes[2 * idx + 1] != '#':
                    node = TreeNode(nodes[2 * idx + 1])
                    head.right = node
                    tmp.append(node)
                else:
                    tmp.append(None)
                # end if
            # end for
            roots = tmp
        # end for
        return root



root = TreeNode(1)
root.right = TreeNode(3)
root.left = TreeNode(2)
root.left.left = TreeNode(4)
print(Solution().deserialize(Solution().serialize(root)).left.left.val)