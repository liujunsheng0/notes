#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
https://www.jianshu.com/p/cedbd94f4f45
http://www.matrix67.com/blog/archives/333


d(x,y) + d(y,z) >= d(x,z)  （从x变到z所需的步数不会超过x先变成y再变成z的步数）

want
d(child, want) + d(want, root) >= d(child, root)
假设d(want, root) = 1, d(child, want)最大为1, 可得d(child, root) <= 2, 删除了d(child, root) > 2的节点
"""
# TODO: bktree
