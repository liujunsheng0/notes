#!/usr/bin/python3.6
# -*- coding: utf-8 -*-


"""
给定一个整型数组, 数组元素随机无序的, 要求打印出所有元素右边第一个大于该元素的值, 如果不存在, 输出None

如数组A=[1,5,3,6,4,8,9,10]          输出[5, 6, 6, 8, 8, 9, 10, None]

如数组A=[8, 2, 5, 4, 3, 9, 7, 2, 5] 输出[9, 5, 9, 9, 9, None, None, 5, None]

要求: 时间复杂度为O(n)
"""


def solution1(nums: list) -> list:
    # O(n ^ 2)
    ans = []
    for idx, i in enumerate(nums[:-1]):
        v = None
        for j in nums[idx + 1:]:
            if j > i:
                v = j
                break
        ans.append(v)
    ans.append(None)
    return ans


def solution2(nums: list) -> list:
    # O(n), 单调栈 - 递减
    size = len(nums)
    ans = [None] * size
    # 栈里面存放索引
    stack = [0]
    idx = 1
    while idx < size:
        while stack and idx < size and nums[idx] < nums[stack[-1]]:  # 单调递减
            stack.append(idx)
            idx += 1
        # end while
        while stack and idx < size and nums[idx] > nums[stack[-1]]:  # 弹出元素直至单调递减
            ans[stack[-1]] = nums[idx]
            stack.pop()
        # end while
        stack.append(idx)
        idx += 1
    # end while
    return ans

if __name__ == '__main__':
    import random
    a = [random.randint(0, 100) for _ in range(30)]
    r1 = solution1(a)
    r2 = solution2(a)
    print(r1 == r2)
    print(a)
    print(r1)
    print(r2)
