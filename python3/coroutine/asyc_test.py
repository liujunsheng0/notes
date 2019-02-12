#!/usr/bin/python3
# -*- coding: utf-8 -*-

import asyncio
import time
from datetime import datetime
from functools import partial
import threading


"""
名词:
    event_loop 事件循环
        程序开启一个无限的循环, 将协程对象注册到事件循环上. 当满足事件发生条件时, 调用相应的协程对象
    coroutine 协程对象
        协程对象, 指一个使用async关键字定义的函数, 它的调用不会立即执行, 而是会返回一个协程对象.
        协程对象需要注册到事件循环, 由事件循环调用
    task 任务
        一个协程对象就是一个原生可以挂起的函数, 任务则是对协程进一步封装, 其中包含任务的各种状态. 
    future, asyncio.Future
        代表即将执行或没有执行任务的结果. 它和task上没有本质的区别
    asyncio
        Python 3.4版本引入的标准库, 直接内置了对异步IO的支持. 
    async/await
        Python3.5 用于定义协程的关键字, async定义一个协程, await用于挂起阻塞的异步调用接口
        通过await语法来挂起自身的协程, 并等待另一个协程完成直到返回结果
        使用await可以针对耗时的操作进行挂起, 就像生成器里的yield一样, 函数让出控制权. 协程遇到await, 事件循环将会挂起该协程,
        执行别的协程, 直到其他的协程也挂起或者执行完毕, 再进行下一个协程的执行, 协程的目的也是让一些耗时的操作异步化。

future对象的状态:
    Pending  创建task时的状态
    Running  执行task时的状态
    Done     完成task时的状态
    Cancelled

注意:
    如果协程中都是同步执行的, 和同步执行一样...
    目前大部分库都不支持异步, 所以使用时小心...
    await后面跟的必须是一个Awaitable对象, 或者实现了相应协议的对象,  查看Awaitable抽象类的代码, 表明了只要一个类实现了
    __await__方法, 那么通过它构造出来的实例就是一个Awaitable,  并且Coroutine类也继承了Awaitable
    await语法只能出现在通过async修饰的函数中

asyncio中重要的函数:
    asyncio.gather
        传参        可以传递多个协程或者Futures,函数会自动将协程包装成task,例如协程生成器
        返回值      包含Futures结果的list
        返回值顺序   按照原始顺序排列
        函数意义    注重收集结果,等待一堆Futures并按照顺序返回结果

    asyncio.wait
        传参        a list of futures
        返回值      返回两个Future集合 (done, pending)
        返回值顺序  无序
        函数意义    是一个协程等传给他的所有协程都运行完之后结束,并不直接返回结果

    asyncio.as_completed
        传参        a list of futures
        返回值      返回一个协程迭代器
        返回值顺序  按照完成顺序
        函数意义    返回的迭代器每次迭代只返回已经完成的Futures

"""


class AsyncStudy(object):
    def __init__(self):
        self.event_loop = asyncio.get_event_loop()

    def __del__(self):
        self.close()

    @property
    def now(self):
        return datetime.now().strftime('%H:%M:%S')

    async def do_something(self, n):
            print('start %s' % n, self.now)
            # 在 sleep的时候, 使用await让出控制权.
            # 即当遇到阻塞时, 使用await方法将协程的控制权让出, 以便event_loop调用其他的协程
            await asyncio.sleep(n)  # 可视为费时的IO操作
            print('end  %s' % n, self.now)
            return self.now

    def run(self, task):
        """
        :param task: 协程对象组成的list
        """
        if self.event_loop.is_closed():
            raise Exception('event loop is closed')
        if self.event_loop.is_running():
            raise Exception('event loop is running')
        if isinstance(task, list):
            # asyncio实现并发, 就需要多个协程来完成任务, 每当有任务阻塞的时候就await, 然后其他协程继续工作
            # 创建多个协程的列表, 然后将这些协程注册到事件循环中.
            task = asyncio.wait(task)
        # 协程对象不能直接运行, 在注册事件循环的时候, 其实是run_until_complete方法将协程包装成为了一个任务(task)对象
        # 所谓task对象是Future类的子类, 保存了协程运行后的状态, 用于未来获取协程的结果

        # run_until_complete 将协程对象注册到事件循环, 并启动事件循环, 当传入一个协程,其内部会自动封装成task
        return self.event_loop.run_until_complete(task)

    def close(self):
        if not self.event_loop.is_closed():
            print('close')
            self.event_loop.stop()
            self.event_loop.close()

    def create_corourine1(self):
        """可通过async 定义一个协程对象"""
        # coroutines 中的对象不是函数, 而是协程对象, 并不能像函数一样, 立即执行
        # 需要把协程加入到事件循环(loop), 由后者在适当的时候调用协程
        coroutines = [self.do_something(i) for i in range(0, 4)]
        self.run(coroutines)

    def create_coroutine2(self):
        """ 创建协程对象的方法以及其返回值 """
        task = self.do_something(1)
        asyncio.gather(task)  # 创建协程对象, 那么await的返回值就是协程运行的结果
        asyncio.wait([self.do_something(1), self.do_something(2)])
        # for task in asyncio.as_completed(tasks):
        #     result = await task
        #     print('Task ret: {}'.format(result))

    def create_tasks(self):
        """ 协程对象 -> task """
        # 协程对象不能直接运行, 在注册事件循环的时候, 其实是run_until_complete方法将协程包装成为了一个任务(task)对象.
        # 所谓task对象是Future类的子类. 保存了协程运行后的状态, 用于获取协程的返回结果
        # 以下两种方式都可以用来创建task
        # task = asyncio.ensure_future(self.do_something(1))
        task = self.event_loop.create_task(self.do_something(1))
        # 同一个协程如果执行完成了, 不会在执行...
        self.run([task, task])

    def callback(self):
        """
        绑定回调, 在task执行完毕的时候可以获取执行的结果, 回调的最后一个参数是future对象,
        通过该对象可以获取协程返回值. 如果回调需要多个参数
        """
        task = self.event_loop.create_task(self.do_something(1))

        def callback(a, future: asyncio.Future):
            print('callback a =', a, 'return =', future.result())
        task.add_done_callback(partial(callback, 1))
        self.run(task)

    def await_use(self):
        """
        使用async可以定义协程对象, 使用await可以针对耗时的操作进行挂起. 就像生成器里的yield一样, 函数让出控制权.
        协程遇到await, 事件循环将会挂起该协程, 执行别的协程(如asyncio.sleep), 直到其他的协程也挂起或者执行完毕,
        再进行下一个协程的执行
        耗时的操作一般是一些IO操作, 例如网络请求, 文件读取等.
        在do_something中使用asyncio.sleep函数来模拟IO操作, 协程的目的也是让这些IO操作异步化
        """
        corourine = self.do_something(1)
        print(type(corourine), corourine)

    async def _coroutine_nest(self):
        """
        协程嵌套, 说白了就是将一堆协程放一起执行, 哪个IO阻塞了就执行另一个
        使用async可以定义协程, 协程用于耗时的io操作, 可以封装更多的io操作过程, 这样就实现了嵌套的协程,
        即一个协程中await了另外一个协程,如此连接起来。
        """
        tasks = [asyncio.ensure_future(self.do_something(i)) for i in range(1, 4)]
        dones, pendings = await asyncio.wait(tasks)
        for task in dones:
            print('Task ret: ', task.result())

    def coroutine_nest_main(self):
        self.run(self._coroutine_nest())

    def threads(self, is_async=True):
        """ 一个线程处理 另一个线程添加任务 """
        def start_event(loop):
            asyncio.set_event_loop(loop)
            loop.run_forever()

        async def do_something(n):
            print('local start %s' % n, self.now)
            time.sleep(n)
            print('local end  %s' % n, self.now)
            return self.now

        new_loop = asyncio.new_event_loop()
        t1 = threading.Thread(target=start_event, args=(new_loop, ))
        t1.daemon = True
        t1.start()
        if is_async:
            func = self.do_something  # 异步sleep, max(1, 3) = 3s
        else:
            func = do_something   # 大概执行 2 + 3 = 5s, 因为time.sleep 是同步执行的.
        for i in [2, 3]:
            asyncio.run_coroutine_threadsafe(func(i), new_loop)
        t1.join()

    def cancel(self):
        tasks = [asyncio.ensure_future(self.do_something(i)) for i in range(0, 4)]
        try:
            self.event_loop.run_until_complete(asyncio.wait(tasks))
        # ctrl + c 中断程序
        except KeyboardInterrupt as e:
            print(e)
            # for task in tasks:
            for task in asyncio.Task.all_tasks():
                # 挨个任务取消, 如果用协程嵌套, 取消最外层的任务即可
                print(task.cancel())

    def async_generate(self):
        """
        异步生成器..有点小厉害...
        协程对象中不能yield那是3.6之前的情况
        """
        async def async_generate():
            print('async_generate start')
            for i in range(10):
                r = yield i
                print('r =', r)

        g = async_generate()
        print(type(g))

        async def main():
            # 启动生成器...
            print(await g.asend(None))
            print(await g.asend(1))
        self.run(main())

    def run_sync_func(self):
        """
        如果想要在asyncio中使用阻塞的函数调用, 但是不阻塞事件循环的当前线程, 应该怎么操作?
        https://juejin.im/entry/5aabb949f265da23a04951df
        函数(例如io读写, requests网络请求)阻塞了客户代码与asycio事件循环的唯一线程, 因此在执行调用时.
        整个应用程序都会冻结. 这个问题的解决方法是使用事件循环对象的 run_in_executor方法.
        asyncio的事件循环在背后维护着一个ThreadPoolExecutor对象, 我们可以调用run_in_executor方法, 把可调用对象发给它执行
        (简单来说用的是多线程...)
        在asyncio中调用阻塞函数时, 需要使用asyncio维护的线程池来另开线程运行阻塞函数, 防止阻塞事件循环所在的线程.
        """
        from concurrent import futures
        from time import sleep
        executor = futures.ThreadPoolExecutor(max_workers=5)

        def sleep_(t):
            print('sleep start ', t, self.now, threading.get_ident())
            sleep(t)
            print('sleep end   ', t, self.now)
            return t

        async def blocked_sleep(loop_, t):
            await loop_.run_in_executor(executor, sleep_, t)
            return t

        async def main():
            task = [blocked_sleep(self.event_loop, i) for i in range(1, 6)]
            return await asyncio.gather(*task)

        results = self.run(main())
        print('results =', results)


if __name__ == '__main__':
    obj = AsyncStudy()
    # obj.create_corourine1()
    # obj.create_tasks()
    # obj.callback()
    # obj.await_use()
    # obj.coroutine_nest_main()
    # obj.threads()
    # obj.threads(False)
    # obj.cancel()
    # obj.async_generate()
    obj.run_sync_func()
