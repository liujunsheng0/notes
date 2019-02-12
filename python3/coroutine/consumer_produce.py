#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
"""
利用协程改写生产者,消费者模式
yield在函数中返回值时会保存函数的状态, 使下一次调用函数时会从上一次的状态继续执行
"""

import random
import asyncio
from datetime import datetime
import time


def now():
    return datetime.now().strftime('%H:%M:%S')


def generate():
    """ 利用生成器实现 生产者-消费者 """
    def consumer():
        r = ''
        while True:
            produce_num = yield r
            if produce_num is None:
                yield "consumer finish"  # 让函数遇到 yield 表达式时暂停执行, 执行其他协程
                return
            r = "consume %s" % produce_num
            print(r)

    def produce(gen):
        gen.send(None)  # 启动生成器
        for i in [1, 2, 3, None]:
            n = None
            if i is not None:
                n = random.randint(1, 10)
                time.sleep(1)
                print("produce %s" % n)
            r = gen.send(n)
            print("produce receive: %s" % r)
        print("produce finish")
        gen.close()
    print('generate, start =', now())
    g = consumer()
    produce(g)
    print('generate, end =', now())


def coroutine():
    """ 协程 实现生产者 消费者,  """
    async def produce():
        n = random.randint(1, 10)
        # 如果只有一个协程执行时, 相当于同步的time.sleep(1)
        await asyncio.sleep(1)
        print("produce = %s" % n)
        return n

    async def consumer(n: int=5):
        while n > 0:
            n -= 1
            v = await produce()
            if v is None:
                break
            print("consumer = %s" % v)

        return "finish"

    async def main():
        return await consumer()
    loop = asyncio.get_event_loop()
    print('coroutine, start =', now())
    # task = asyncio.wait([main(), main(), main()])
    task = main()
    loop.run_until_complete(task)
    print('coroutine, end =', now())


if __name__ == '__main__':
    # generate()
    coroutine()
