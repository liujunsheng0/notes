#!/usr/bin/python3.7
# -*- coding: utf-8 -*-

import threading
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures import as_completed
import time

"""
https://python-parallel-programmning-cookbook.readthedocs.io/zh_CN/latest/chapter4/02_Using_the_concurrent.futures_Python_modules.html
concurrent.futures 模块由以下部分组成：
concurrent.futures.Executor 这是一个虚拟基类, 提供了异步执行的方法
submit(function, argument)  调度函数(可调用的对象), 将argument作为参数传入 
map(function, argument)     将 argument 作为参数执行函数, 以异步的方式
shutdown(Wait=True)         发出让执行者释放所有资源的信号.
concurrent.futures.Future   其中包括函数的异步执行. Future对象是submit任务（即带有参数的functions）到executor的实例
"""


def _evaluate(x, sleep):
    i = 0
    # 这里只是为了消耗时间
    for i in range(0, 10000000):
        i = i + 1
    res = i * x
    if sleep:
        time.sleep(x / 3)
    return res


def submit():
    number_list = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    for sleep in (0, 1):
        # 顺序执行
        start_time = time.time()
        for item in number_list:
            print(_evaluate(item, sleep), end=', ')
        print(f"\nsleep:{sleep} Sequential execution in {time.time() - start_time} seconds")

        # 线程池执行, max_workers 参数表示最多有多少个worker并行执行任务
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(_evaluate, item, sleep) for item in number_list]
            for future in as_completed(futures):
                print(future.result(), end=', ')
        print(f"\nsleep:{sleep} Thread pool execution in {time.time() - start_time} seconds")

        # 进程池
        start_time = time.time()
        with ProcessPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(_evaluate, item, sleep) for item in number_list]
            for future in as_completed(futures):
                print(future.result(), end=', ')
        print(f"\nsleep:{sleep} Process pool execution in {time.time() - start_time} seconds")


def map_():
    executor = ThreadPoolExecutor(max_workers=2)
    for future in executor.map(time.sleep, range(10)):
        print(future, threading.active_count())
    executor.shutdown()


if __name__ == "__main__":
    # submit()
    map_()
