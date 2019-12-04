#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""
参考: https://zhuanlan.zhihu.com/p/34133067
"""
from typing import Dict, Any


class Node(object):
    """ 双向链表节点 """

    def __init__(self, key, value, prev=None, next_=None):
        self.key = key
        self.value = value
        self.prev: Node = prev  # 前面的节点
        self.next: Node = next_  # 后面的节点


class LruCache(object):
    """ 
    dict + 双向链表实现LRU, get/set的时间复杂度为O(1)
    
    from cachetools import LRUCache 中使用的是orderDict
    """

    def __init__(self, max_size=10):
        self.cache: Dict[Any, Node] = {}
        self.max_cache_size = max_size

        self.head = Node(None, None)
        self.tail = Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key, default=None):
        if key in self.cache:
            node = self.cache.get(key)
            self._move_to_head(node)
            return node.value
        return default

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            return self._move_to_head(node)

        if len(self.cache) >= self.max_cache_size:
            self._remove_tail()

        node = Node(key, value)
        self._add_node(node)

    def _add_node(self, node: Node):
        """ 新增节点到队首 """
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

        self.cache[node.key] = node

    def _move_to_head(self, node: Node):
        """ 更新节点到队首 """
        prev = node.prev
        next_ = node.next
        prev.next = next_
        next_.prev = prev
        self._add_node(node)

    def _remove_tail(self):
        if len(self.cache) < 1:
            return

        prev = self.tail.prev
        if prev.key in self.cache:
            self.cache.pop(prev.key)

        node = prev.prev
        node.next = self.tail
        self.tail.prev = node

        prev.prev = prev.next = None
        del prev

    def print_nodes(self):
        head = self.head.next
        while head is not self.tail:
            print(head.key, end="->")
            head = head.next
        print("End")


if __name__ == '__main__':
    lru = LruCache(3)
    appeared = set()
    for i in [1, 2, 1, 3, 4, 3]:
        if i not in appeared:
            appeared.add(i)
            lru.put(i, i)
        else:
            lru.get(i)
        lru.print_nodes()

