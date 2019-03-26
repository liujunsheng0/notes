#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
回文链表 https://www.lintcode.com/problem/palindrome-linked-list/description
设计一种方式检查一个链表是否为回文链表

输入: 1->2->1  输出: true
输入: 2->2->1  输出: false
挑战: O(n)的时间和O(1)的额外空间。
"""


class ListNode(object):
    def __init__(self, val, next_=None):
        self.val = val
        self.next = next_


class Solution:
    """
    @param head: A ListNode.
    @return: A boolean.
    """
    def findMid(self, node):
        """ 快慢指针找中心点 """
        fast, low = node.next, node
        while fast is not None and fast.next is not None:
            fast = fast.next.next
            low = low.next
        return low

    def reverse(self, head):
        """ 转置链表 """
        cur = None
        while head:
            tmp = head.next
            head.next = cur
            cur = head
            head = tmp
        return cur

    def isPalindrome(self, head):
        if head is None or head.next is None:
            return True
        mid = self.findMid(head)
        reverse = mid.next
        mid.next = None
        reverse = self.reverse(reverse)
        while head and reverse:
            if head.val != reverse.val:
                return False
            head = head.next
            reverse = reverse.next
        return True

a = ListNode(1)
a.next = ListNode(2)
a.next.next = ListNode(1)
# a.next.next.next = ListNode(1)
print(Solution().isPalindrome(a))
