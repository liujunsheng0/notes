#!/usr/bin/python3
# -*- coding: utf-8 -*-


from time import sleep
from threading import Thread

"""
测试threading中daemon的作用, 默认为False
在主线程中创建子线程, 当主线程结束时根据子线程daemon属性值的不同可能会发生下面的两种情况之一:
    1. 子线程的daemon属性为False
      主线程结束时会检测该子线程是否结束, 如果该子线程还在运行, 则主线程会等待它完成后再退出；
    2. 子线程的daemon属性为True
      主线程运行结束时不对这个子线程进行检查而直接退出, 同时所有daemon值为True的子线程将随主线程一起结束, 而不论是否运行完成
简单来说:
    Daemon设置为子线程是否随主线程一起结束, 默认为False. 如果要随主线程一起结束需要设置为True.
PS: 属性daemon的值默认为False, 如果需要修改, 必须在调用start()方法启动线程之前进行设置
"""


def sleep_func(t):
    sleep(t)
    print("t =", t)


def test(daemon1=False, daemon2=False, is_join=False):
    t1 = Thread(target=sleep_func, args=(2, ), daemon=daemon1)
    t2 = Thread(target=sleep_func, args=(4, ), daemon=daemon2)
    t1.start()
    t2.start()
    if is_join:
        t1.join()
        t2.join()
    print("finish", t1.daemon, t2.daemon, is_join)


if __name__ == "__main__":
    # test(is_join=True)
    # test(True, False, is_join=True)
    # test(False, True, is_join=True)
    # test(True, True, is_join=True)
    # 以上四个答案均为
    # t = 2
    # t = 4
    # finish ...

    # test(is_join=False)
    # finish False False False
    # t = 2
    # t = 4

    # test(True, False, is_join=False)
    # finish True False False
    # t = 2
    # t = 4

    # test(False, True, is_join=False)
    # finish False True False
    # t = 2

    test(True, True, is_join=False)
    # finish True True False
