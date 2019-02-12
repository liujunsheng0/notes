#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
异步初体验....
"""

from datetime import datetime
import asyncio
from threading import Thread

import aiohttp  # 异步http请求库


def now():
    return datetime.now().strftime('%H:%M:%S')


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(resp.status)
            return await resp.text()


async def do_some_work(x):
    print('Waiting ', x, now())
    try:
        ret = await fetch(url='http://127.0.0.1:5000/{}'.format(x))
        print(ret)
    except Exception as e:
        try:
            print(e)
            print(await fetch(url='http://127.0.0.1:5000/error'))
        except Exception as e:
            print('error', e)
    else:
        print('Done {}'.format(x), now())


def main():
    new_loop = asyncio.get_event_loop()
    t = Thread(target=start_loop, args=(new_loop,))
    t.setDaemon(True)
    t.start()
    # 大约max(range(10)) = 9 完成, 如果是同步执行的话, 大约sum(range(9)) = 45s完成
    for i in range(10):
        asyncio.run_coroutine_threadsafe(do_some_work(i), new_loop)
    t.join()


if __name__ == '__main__':
    main()
