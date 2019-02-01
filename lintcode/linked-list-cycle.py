#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
给定一个链表，判断它是否有环。 https://www.lintcode.com/problem/linked-list-cycle/description

样例
给出 -21->10->4->5, tail connects to node index 1，返回 true
"""

"""
Definition of ListNode
class ListNode(object):
    def __init__(self, val, next=None):
        self.val = val
        self.next = next
"""

class Solution:
    """
    @param head: The first node of linked list.
    @return: True if it has a cycle, or false
    """
    def hasCycle(self, head):
        """快慢指针"""
        if not head or not head.next:
            return False
        slow = fast = head
        while slow and fast:
            if not fast.next or not fast.next.next:
                return False
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        # end while
        return False
