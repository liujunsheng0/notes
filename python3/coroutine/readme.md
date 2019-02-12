[github 链接](https://github.com/liujunsheng0/study_py3/tree/master/coroutine)   https://github.com/liujunsheng0/study_py3/tree/master/coroutine

# 阅读顺序

1. readme.md
2. coroutine_test.py
3. asyc_test.py
4. consumer_produce.py
5. aio_http

# [异步IO](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/00143208573480558080fa77514407cb23834c78c6c7309000)

**同步IO：**CPU的速度远远快于磁盘、网络等IO。在一个线程中，CPU执行代码的速度极快，然而，一旦遇到IO操作，如读写文件、发送网络数据时，就需要等待IO操作完成，才能继续进行下一步操作。

在IO操作的过程中，当前线程被挂起，而其他需要CPU执行的代码就无法被当前线程执行。

因为一个IO操作就阻塞了当前线程，导致其他代码无法执行，所以我们必须使用多线程或者多进程来并发执行代码，为多个用户服务。每个用户都会分配一个线程，如果遇到IO导致线程被挂起，其他用户的线程不受影响。

多线程和多进程的模型虽然解决了并发问题，但是系统不能无上限地增加线程。由于系统切换线程的开销也很大，所以，一旦线程数量过多，CPU的时间就花在线程切换上了，真正运行代码的时间就少了，结果导致性能严重下降。

由于我们要解决的问题是CPU高速执行能力和IO设备的龟速严重不匹配，多线程和多进程只是解决这一问题的一种方法。

另一种解决IO问题的方法是**异步IO**。当代码需要执行一个耗时的IO操作时，它只发出IO指令，并不等待IO结果，然后就去执行其他代码了。一段时间后，当IO返回结果时，再通知CPU进行处理。

可以想象，如果按普通顺序写出的代码实际上是没法完成异步IO的：

```python
do_some_code()
f = open(file, 'r')
r = f.read() # <== 线程停在此处等待IO操作结果
# IO操作完成后线程才能继续执行:
do_some_code(r)
```

------

**异步IO模型需要一个消息循环，在消息循环中，主线程不断地重复"读取消息-处理消息"这一过程**

```python
loop = get_event_loop()
while True:
    event = loop.get_event()
    process_event(event)
```

消息模型其实早在应用在桌面应用程序中了。一个GUI程序的主线程就负责不停地读取消息并处理消息。所有的键盘、鼠标等消息都被发送到GUI程序的消息队列中，然后由GUI程序的主线程处理。

由于GUI线程处理键盘、鼠标等消息的速度非常快，所以用户感觉不到延迟。某些时候，GUI线程在一个消息处理的过程中遇到问题导致一次消息处理时间过长，此时，用户会感觉到整个GUI程序停止响应了，敲键盘、点鼠标都没有反应。这种情况说明在消息模型中，处理一个消息必须非常迅速，否则，主线程将无法及时处理消息队列中的其他消息，导致程序看上去停止响应。

> **消息模型是如何解决同步IO必须等待IO操作这一问题的呢？**
>
> 当遇到IO操作时，代码只负责发出IO请求，不等待IO结果，然后直接结束本轮消息处理，进入下一轮消息处理过程。当IO操作完成后，将收到一条"IO完成"的消息，处理该消息时就可以直接获取IO操作结果。在"发出IO请求"到收到"IO完成"的这段时间里，同步IO模型下，主线程只能挂起，但异步IO模型下，主线程并没有休息，而是在消息循环中继续处理其他消息。这样，在异步IO模型下，一个线程就可以同时处理多个IO请求，并且没有切换线程的操作。对于大多数IO密集型的应用程序，使用异步IO将大大提升系统的多任务处理能力。



# [并发和并行](https://www.zhihu.com/question/33515481/answer/58849148)

你吃饭吃到一半，电话来了，你一直到吃完了以后才去接，这就说明你不支持并发也不支持并行；
你吃饭吃到一半，电话来了，你停了下来接了电话，接完后继续吃饭，这说明你支持并发；
你吃饭吃到一半，电话来了，你一边打电话一边吃饭，这说明你支持并行；

并发的关键是你有处理多个任务的能力，不一定要同时。并行的关键是你有同时处理多个任务的能力。
所以它们最关键的点就是：是否是 **同时**


# [协程](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001432090171191d05dae6e129940518d1d6cf6eeaaa969000)
函数，在所有语言中都是层级调用，比如A调用B，B在执行过程中又调用了C，C执行完毕返回，B执行完毕返回，最后是A执行完毕。子程序调用是通过栈实现的，一个线程就是执行一个子程序。

子程序调用总是一个入口，一次返回，调用顺序是明确的。而协程的调用和子程序不同。

**协程，又称微线程，纤程，英文名Coroutine。**

+ 协程的作用，是在执行函数A时，可以随时中断，去执行函数B，然后中断继续执行函数A（可以自由切换）。但这一过程并不是函数调用（没有调用语句），这一整个过程看似像多线程，然而协程只有一个线程执行。

  协程看上去也是子程序，但执行过程中，在子程序内部可中断，然后转而执行别的子程序，在适当的时候再返回来接着执行。注意，在一个子程序中中断，去执行其他子程序，不是函数调用，有点类似CPU的中断。

+ 协程的特点在于一个线程执行多个协程，那和多线程比，协程有何优势？
  1. 最大的优势就是协程极高的执行效率。因为子程序切换不是线程切换，而是由程序自身控制，因此，没有线程切换的开销，和多线程比，线程数量越多，协程的性能优势就越明显。
  2. 第二大优势就是不需要多线程的锁机制，**因为只有一个线程，也不存在同时写变量冲突**，在协程中控制共享资源不加锁，只需要判断状态就好了，所以执行效率比多线程高很多。

+ 协程适用场景

  **协程适合处理IO密集型程序的效率问题，但是处理CPU密集型不是它的长处，如要充分发挥CPU利用率可以结合多进程+协程**

+ 协程应用
  1. Python2
     + yield
     + [gevent](https://thief.one/2017/02/20/Python%E5%8D%8F%E7%A8%8B/)
  2. Python3
     - asynico + yield from（python3.4）
     - async + await（>= python3.5）
     - gevent

+ 生成器（generator）和协程（coroutine）的区别：

  1. generator总是生成值，一般是迭代的序列，coroutine关注的是消耗值，是数据的消费者
  2. coroutine不会与迭代操作关联，而generator与迭代操作相关联
  3. coroutine强调协同控制程序流，generator强调保存状态和产生数据
  4. 相似的是，它们都是不用return来实现重复调用的函数/对象，都用到了**yield(中断/恢复)**的方式来实现。（yield在函数中返回值时会保存函数的状态, 使下一次调用函数时会从上一次的状态继续执行）

利用yield写生产者消费者，更多实现方式详见[github](https://github.com/liujunsheng0/study_py3/blob/master/coroutine/consumer_produce.py)

```python
# 生成器
def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'

def produce(c):
    # 启动生成器
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()

c = consumer()
produce(c)
```

注意到`consumer`函数是一个`generator`，把一个`consumer`传入`produce`后：

1. 首先调用`c.send(None)`启动生成器；
2. 然后，一旦生产了东西，通过`c.send(n)`切换到`consumer`执行；
3. `consumer`通过`yield`拿到消息，处理，又通过`yield`把结果传回；
4. `produce`拿到`consumer`处理的结果，继续生产下一条消息；
5. `produce`决定不生产了，通过`c.close()`关闭`consumer`，整个过程结束。

整个流程无锁，由一个线程执行，`produce`和`consumer`协作完成任务，所以称为"协程"，而非线程的抢占式多任务。



# 名词介绍

+ event_loop 事件循环

  程序开启一个无限循环，程序员会把协程对象（可以认为是执行函数）注册到事件循环上。当满足事件发生的时候，调用相应的协程对象

+ coroutine 协程

  协程对象，指一个使用async关键字定义的函数，它的调用不会立即执行函数，而是会返回一个协程对象。协程对象需要注册到事件循环，由事件循环调用

+ task  任务

  一个协程对象就是一个原生可以挂起的函数，任务则是对协程进一步封装，其中包含任务的各种状态。

+ future

   代表将来执行或没有执行的任务的结果。它和task上没有本质的区别

+ asyncio

   是Python 3.4版本引入的标准库，直接**内置了对异步IO的支持**。

+ async/await

  python3.5 用于定义协程的关键字，async定义一个协程，await用于挂起阻塞的异步调用接口。



# [asyncio](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001432090954004980bd351f2cd4cc18c9e6c06d855c498000)

`asyncio`是Python 3.4版本引入的标准库，直接**内置了对异步IO的支持**。

`asyncio`的编程模型就是一个消息循环。从`asyncio`模块中获取`EventLoop`的引用，然后把需要执行的协程扔到`EventLoop`中执行，就实现了异步IO。

1. `asyncio`提供了完善的异步IO支持；
2. 异步操作需要在`coroutine`中通过`yield from`完成，即内部用`yield from`调用另一个coroutine实现异步操作；
3. 多个`coroutine`可以封装成一组Task然后并发执行

详见[github](https://github.com/liujunsheng0/study_py3/blob/master/coroutine/coroutine_test.py)



# async/await

用`asyncio`提供的`@asyncio.coroutine`可以把一个generator标记为coroutine类型，然后在coroutine内部用`yield from`调用另一个coroutine实现异步操作。

为了简化并更好地标识异步IO，从Python 3.5开始引入了新的语法`async`和`await`，可以让coroutine的代码更简洁易读。

请注意，`async`和`await`是针对coroutine的新语法，要使用新的语法，只需要做两步简单的替换：

1. 把`@asyncio.coroutine`替换为`async`；
2. 把`yield from`替换为`await`。

**async，await的使用**

+ 使用async可以定义协程对象

+ 使用await可以针对耗时的操作进行挂起，就像生成器里的yield一样，函数让出控制权。

  协程遇到await，事件循环将会挂起该协程，执行别的协程，直到其他的协程也挂起或者执行完毕，再进行下一个协程的执行，协程的目的也是让一些耗时的操作异步化。

+ **await后面跟的必须是一个Awaitable对象，或者实现了相应协议的对象，查看Awaitable抽象类的代码，表明了只要一个类实现了`__await__`方法，那么通过它构造出来的实例就是一个Awaitable，并且Coroutine类也继承了Awaitable。**

使用demo详见[github](https://github.com/liujunsheng0/study_py3/blob/master/coroutine/asyc_test.py)

# gevent

gevent是第三方库，通过greenlet实现协程。

+ 基本思想 　　

  当一个greenlet遇到IO操作时，比如访问网络，就自动切换到其他的greenlet，等到IO操作完成，再在适当的时候切换回来继续执行。由于IO操作非常耗时，经常使程序处于等待状态，有了gevent为我们自动切换协程，就保证总有greenlet在运行，而不是等待IO。

+ 使用demo详见[github](https://github.com/liujunsheng0/study_py3/tree/master/coroutine/aio_http)

# 不同方式实现hello world

代码详见[github](https://github.com/liujunsheng0/study_py3/blob/master/coroutine/coroutine_test.py)

```python
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

```



# 学习链接

[廖雪峰---异步IO](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/00143208573480558080fa77514407cb23834c78c6c7309000)

[协程](https://thief.one/2017/02/20/Python%E5%8D%8F%E7%A8%8B/)

[协程的学习与研究](https://thief.one/2018/06/21/1/)

[异步IO](https://www.jianshu.com/p/b5e347b3a17c)

[爬虫-同步，多线程，多进程，协程](https://zhuanlan.zhihu.com/p/25228075)

https://zhuanlan.zhihu.com/p/27258289