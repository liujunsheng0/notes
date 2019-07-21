#!/usr/bin/python3.7
# -*- coding: utf-8 -*-

import threading
from datetime import datetime
import time

import asyncio


def now():
    return datetime.now().strftime('%H:%M:%S')


def thread_test():
    def hello(num: int):
        print("Hello {} now: {} thread id: {}".format(num, now(), threading.get_ident()))
        time.sleep(num)
        print("Bye.. {} now: {}".format(num, now()))

    tasks = [threading.Thread(target=hello, args=[i, ]) for i in range(1, 4)]
    for t in tasks:
        t.start()
    for t in tasks:
        t.join()
    # result
    # Hello 1 now = 17:29:19 serve thread id = x
    # Hello 2 now = 17:29:19 serve thread id = y
    # Hello 3 now = 17:29:19 serve thread id = z
    # Bye.. 1 now = 17:29:20
    # Bye.. 2 now = 17:29:21
    # Bye.. 3 now = 17:29:22


def asyncio_test():
    # asyncio.coroutine 把一个generator标记为coroutine类型
    @asyncio.coroutine
    def hello(num: int):
        print("Hello {} now: {} thread id: {}".format(num, now(), threading.get_ident()))
        # 异步调用asyncio.sleep(num), 此处可以看做耗时的IO操作...
        # 在此期间, 主线程并未等待, 而是去执行EventLoop中其他可以执行的coroutine, 因此实现并发执行
        yield from asyncio.sleep(num)
        print("Bye.. {} now: {}".format(num, now()))

    # 获取EventLoop
    loop = asyncio.get_event_loop()
    # 协程执行顺序, 貌似和tasks中的任务顺序有关, 可能是先进先执行队列吧....
    # 三个协程包装成一个任务
    task = asyncio.wait([hello(i) for i in range(1, 4)])
    # 执行coroutine
    print(loop.run_until_complete(task))
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
    #    task1 执行到asyncio.sleep(1), asyncio.sleep(1)挂起, 等待计时结束, 加入执行队列, 执行循环队列中的下一个任务
    #    task2 执行到asyncio.sleep(2), asyncio.sleep(2)挂起, 等待计时结束, 加入执行队列, 执行循环队列中的下一个任务
    #    task3 执行到asyncio.sleep(3), asyncio.sleep(3)挂起, 等待计时结束, 加入执行队列, 执行循环队列中的下一个任务
    #    asyncio.sleep(1), 计时结束, 执行task1, task1执行完毕, 执行其他协程
    #    asyncio.sleep(2), 计时结束, 执行task2, task2执行完毕, 执行其他协程
    #    asyncio.sleep(3), 计时结束, 执行task3, task3执行完毕, 执行其他协程


def async_test():
    async def hello(num: int):
        print("Hello {} now: {} thread id: {}".format(num, now(), threading.get_ident()))
        await asyncio.sleep(num)
        print("Bye.. {} now: {}".format(num, now()))
    # end hello

    # 获取EventLoop
    loop = asyncio.get_event_loop()
    tasks = [hello(i) for i in range(1, 4)]
    # 执行coroutine
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    # 结果
    # Hello 3 now: 19:35:13 thread id: 140223218222848
    # Hello 2 now: 19:35:13 thread id: 140223218222848
    # Hello 1 now: 19:35:13 thread id: 140223218222848
    # Bye.. 1 now: 19:35:14
    # Bye.. 2 now: 19:35:15
    # Bye.. 3 now: 19:35:16


def gevent_test():
    import gevent
    from gevent import monkey
    monkey.patch_all()

    def hello(num: int):
        print("Hello {} now: {} thread id: {}".format(num, now(), threading.get_ident()))
        time.sleep(num)
        print("Bye.. {} now: {}".format(num, now()))

    tasks = [gevent.spawn(hello, i) for i in range(3)]
    gevent.joinall(tasks)
    # 结果如下
    # Hello 0 now = 17:44:47 serve thread id = 46817808
    # Hello 1 now = 17:44:47 serve thread id = 46818112
    # Hello 2 now = 17:44:47 serve thread id = 46818264
    # Bye.. 0 now = 17:44:47
    # Bye.. 2 now = 17:44:48
    # Bye.. 1 now = 17:44:49


def create_task_test():
    async def say_after(delay, what):
        await asyncio.sleep(delay)
        print(what)

    async def main1():
        start = datetime.now().timestamp()
        await say_after(1, 'hello')
        await say_after(2, 'world')
        print("main1 cost {}".format(datetime.now().timestamp() - start))

    async def main2():
        # # 任务 被用来设置日程以便 并发 执行协程
        task1 = asyncio.ensure_future(say_after(1, 'hello'))
        task2 = asyncio.ensure_future(say_after(2, 'world'))
        start = datetime.now().timestamp()
        await task1
        await task2
        # 用来并发运行作为 asyncio 任务 的多个协程
        print("main2 cost {}".format(datetime.now().timestamp() - start))

    async def main3():
        # 任务 被用来设置日程以便 并发 执行协程
        # 此函数 在 Python 3.7 中被加入, 在 Python 3.7 之前, 可以改用低层级的 asyncio.ensure_future() 函数
        task1 = asyncio.create_task(say_after(1, 'hello'))
        task2 = asyncio.create_task(say_after(2, 'world'))
        start = datetime.now().timestamp()

        # Wait until both tasks are completed (should take around 2 seconds.)
        await task1
        await task2
        # 用来并发运行作为 asyncio 任务 的多个协程
        print("main3 cost {}".format(datetime.now().timestamp() - start))

    task = asyncio.wait([main1(), main2(), main3()])
    asyncio.run(task)


def gather_test():
    """
    awaitable asyncio.gather(*aws, loop=None, return_exceptions=False)
    并发 运行 aws 序列中的 可等待对象.
    如果 aws 中的某个可等待对象为协程, 它将自动作为一个任务加入日程.
    如果所有可等待对象都成功完成, 结果将是一个由所有返回值聚合而成的列表.结果值的顺序与 aws中可等待对象的顺序一致.
    如果 return_exceptions=False, 所引发的首个异常会立即传播给等待gather()的任务.aws序列中的其他可等待对象不会被取消并将继续运行.
    如果 return_exceptions=True, 异常会和成功的结果一样处理, 并聚合至结果列表.
    如果 gather() 被取消, 所有被提交 (尚未完成) 的可等待对象也会 被取消.
    如果 aws 序列中的任一 Task 或 Future 对象 被取消, 它将被当作引发了 CancelledError 一样处理,
    在此情况下 gather()调用不会被取消.这是为了防止一个已提交的 Task/Future 被取消导致其他 Tasks/Future 也被取消.
    """
    async def factorial(name, number):
        f = 1
        for i in range(2, number + 1):
            print(f"Task {name}: Compute factorial({i})... now={now()}")
            await asyncio.sleep(1)
            f *= i
        print(f"Task {name}: factorial({number}) = {f} now={now()}")

    async def main():
        # Schedule three calls *concurrently*:
        fs = asyncio.gather(factorial("A", 2), factorial("B", 3), factorial("C", 4))
        print(fs, type(fs))
        result = await fs
        print(result)
    asyncio.run(main())


def wait_for_test():
    """
    coroutine asyncio.wait_for(aw, timeout, *, loop=None)
    等待 aw 可等待对象 完成, 指定 timeout 秒数后超时.
    如果 aw 是一个协程, 它将自动作为任务加入日程.
    timeout 可以为 None, 也可以为 float 或 int 型数值表示的等待秒数.如果 timeout 为 None, 则等待直到完成.
    如果发生超时, 任务将取消并引发 asyncio.TimeoutError.
    要避免任务 取消, 可以加上 shield().
    函数将等待直到目标对象确实被取消, 所以总等待时间可能超过 timeout 指定的秒数.
    如果等待被取消, 则 aw 指定的对象也会被取消.
    """
    async def sleep():
        await asyncio.sleep(3600)
        print('hello!')

    async def main():
        # Wait for at most 1 second
        try:
            await asyncio.wait_for(sleep(), timeout=1)
        except asyncio.TimeoutError:
            print('timeout!')

    asyncio.run(main())


def wait_test():
    """
    coroutine asyncio.wait(aws, *, loop=None, timeout=None, return_when=ALL_COMPLETED)
    
    与 wait_for() 不同, wait() 在超时发生时不会取消可等待对象.
    
    并发运行 aws 指定的 可等待对象 并阻塞线程直到满足 return_when 指定的条件.
    如果 aws 中的某个可等待对象为协程, 它将自动作为任务加入日程.直接向 wait() 传入协程对象已弃用, 因为这会导致令人迷惑的行为.
    :return Task/Future 集合: (done, pending).
    
    用法:
        done, pending = await asyncio.wait(aws),
        loop 参数已弃用, 计划在 Python 3.10 中移除.
        如指定 timeout (float 或 int 类型) 则它将被用于控制返回之前等待的最长秒数.
        请注意此函数不会引发 asyncio.TimeoutError.当超时发生时, 未完成的 Future 或 Task 将在指定秒数后被返回.
        return_when 指定此函数应在何时返回.它必须为以下常数之一:
            FIRST_COMPLETED  函数将在任意可等待对象结束或取消时返回
            FIRST_EXCEPTION  函数将在任意可等待对象因引发异常而结束时返回, 当没有引发任何异常时它就相当于 ALL_COMPLETED
            ALL_COMPLETED    函数将在所有可等待对象结束或取消时返回

    """
    async def sleep(t):
        await asyncio.sleep(t)
        print(f"sleep {t} finish")

    async def main():
        task1 = asyncio.create_task(sleep(2))
        task2 = asyncio.create_task(sleep(3))
        # wait中的参数必须是 asyncio.Task
        done, pending = await asyncio.wait({task1, task2}, timeout=1)
        print(pending)
        await asyncio.wait(pending)

    asyncio.run(main())

def my_test():
    async def sleep(name, t):
        await asyncio.sleep(t)
        print(f"{name} sleep {t} finish")

    async def main():
        # 以下几种方式都是将协程/任务添加到循环
        asyncio.gather(*[sleep("gather", i) for i in range(3)])
        asyncio.wait(asyncio.gather(*[sleep("wait", i) for i in range(3)]))
        for i in range(3):
            asyncio.create_task(sleep("create task", i))
            asyncio.ensure_future(sleep("ensure future", i))

        await asyncio.sleep(10)

    asyncio.run(main())


if __name__ == '__main__':
    # thread_test()
    # asyncio_test()
    # async_test()
    # gevent_test()
    # create_task_test()
    # gather_test()
    # wait_for_test()
    # wait_test()
    my_test()
    # 从结果来看, 多线程与协程的效果一样, 都达到了IO阻塞时切换的功能.
    # 不同的是, 多线程切换的是线程(线程间切换), 协程切换的是上下文(可以理解为执行的函数).
    # 而切换线程的开销是要大于切换上下文的开销, 因此当线程越多, 协程的效率就越比多线程的高.
