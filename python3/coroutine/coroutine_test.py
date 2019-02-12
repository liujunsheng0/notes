#!/usr/bin/python3
# -*- coding: utf-8 -*-

import threading
from datetime import datetime
import time

import asyncio


def now():
    return datetime.now().strftime('%H:%M:%S')


def hello(num: int):
    print("Hello", num, 'now =', now(), 'serve thread id =', threading.currentThread().ident)
    time.sleep(num)
    print("Bye..", num, 'now =', now())


def thread_test():
    tasks = [threading.Thread(target=hello, args=[i, ]) for i in range(3)]
    for t in tasks:
        t.start()
    for t in tasks:
        t.join()
    # result
    # Hello 0 now = 17:29:19 serve thread id = 13856
    # Hello 1 now = 17:29:19 serve thread id = 15188
    # Hello 2 now = 17:29:19 serve thread id = 15320
    # Bye.. 0 now = 17:29:19
    # Bye.. 1 now = 17:29:20
    # Bye.. 2 now = 17:29:21


def asyncio_test():
    # asyncio.coroutine 把一个generator标记为coroutine类型
    @asyncio.coroutine
    def hello(num: int):
        print("Hello", num, 'now =', now(), 'serve thread id =', threading.currentThread().ident)
        # 异步调用asyncio.sleep(num), 此处可以看做耗时的IO操作...
        # 在此期间, 主线程并未等待, 而是去执行EventLoop中其他可以执行的coroutine, 因此实现并发执行
        yield from asyncio.sleep(num)
        print("Bye..", num, 'now =', now())

    # 获取EventLoop
    loop = asyncio.get_event_loop()
    # 协程执行顺序, 貌似和tasks中的任务顺序有关, 可能是先进先执行队列吧....
    tasks = [hello(i) for i in range(1, 4)]
    # 执行coroutine
    task = asyncio.wait(tasks)
    loop.run_until_complete(task)
    loop.close()
    # 执行结果如下
    # Hello 1 now = 17:43:02 serve thread id = 14808
    # Hello 2 now = 17:43:02 serve thread id = 14808
    # Hello 3 now = 17:43:02 serve thread id = 14808
    # Bye.. 1 now = 17:43:03
    # Bye.. 2 now = 17:43:04
    # Bye.. 3 now = 17:43:05
    # 由打印的当前线程id可以看出, 三个coroutine是由同一个线程并发执行的.
    # 如果把asyncio.sleep(2)换成真正的IO操作, 则多个coroutine是由一个线程并发执行的, 可以认为是一个线程的并发...
    # 执行过程说明
    # 1. 当事件循环开始运行时, 它会在Task中寻找coroutine来执行调度, 因为事件循环注册了task(可以认为向事件循环中注册了三个协程,
    #    即[task1, task2, task3]), 因此task开始执行(假设task1先执行)
    # 2. task1执行至yield from asyncio.sleep(1)时, task1挂起, 将协程asyncio.sleep(1)加入到事件循环队列
    #    (协程执行过程中, 当碰到yield, yield from, await时, 协程挂起, 保存当前执行环境, 执行其他协程)
    #    (仅有一个yield 相当于让出执行权, 执行其他协程)
    # 3. 事件循环在队列中查找可被调度的协程, 执行其他协程,
    #    执行顺序可能如下:
    #    task2, task2挂起, asyncio.sleep(2)加入到事件循环队列
    #    task3, task3挂起, asyncio.sleep(3)加入到事件循环队列
    #    asyncio.sleep(1), asyncio.sleep(1)挂起, 等待计时结束
    #    asyncio.sleep(1), asyncio.sleep(2)挂起, 等待计时结束
    #    asyncio.sleep(1), asyncio.sleep(3)挂起, 等待计时结束
    # 4. asyncio.sleep(1), 计时结束, 执行task1, task1执行完毕, 执行其他协程
    #    asyncio.sleep(2), 计时结束, 执行task2, task2执行完毕, 执行其他协程
    #    asyncio.sleep(3), 计时结束, 执行task3, task3执行完毕, 执行其他协程


def async_test():
    async def hello(num: int):
        print("Hello", num, 'now =', now(), 'serve thread id =', threading.currentThread().ident)
        # 异步调用asyncio.sleep(1)
        await asyncio.sleep(num)
        # 如果使用time.sleep 则是顺序执行, 并不是以协程的形式执行
        # time.sleep(2)
        print("Bye..", num, 'now =', now())

    # 获取EventLoop
    loop = asyncio.get_event_loop()
    tasks = [hello(i) for i in range(3)]
    # 执行coroutine
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    # 结果
    # Hello 0 now = 17:44:11 serve thread id = 14796
    # Hello 1 now = 17:44:11 serve thread id = 14796
    # Hello 2 now = 17:44:11 serve thread id = 14796
    # Bye.. 0 now = 17:44:11
    # Bye.. 1 now = 17:44:12
    # Bye.. 2 now = 17:44:13


def gevent_test():
    import gevent
    from gevent import monkey
    monkey.patch_all()
    tasks = [gevent.spawn(hello, i) for i in range(3)]
    gevent.joinall(tasks)
    # 结果如下
    # Hello 0 now = 17:44:47 serve thread id = 46817808
    # Hello 1 now = 17:44:47 serve thread id = 46818112
    # Hello 2 now = 17:44:47 serve thread id = 46818264
    # Bye.. 0 now = 17:44:47
    # Bye.. 2 now = 17:44:48
    # Bye.. 1 now = 17:44:49


if __name__ == '__main__':
    # thread_test()
    # asyncio_test()
    # async_test()
    gevent_test()
    # 从结果来看, 多线程与协程的效果一样, 都达到了IO阻塞时切换的功能.
    # 不同的是, 多线程切换的是线程(线程间切换), 协程切换的是上下文(可以理解为执行的函数).
    # 而切换线程的开销是要大于切换上下文的开销, 因此当线程越多, 协程的效率就越比多线程的高。
