#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
"""http://cachetools.readthedocs.io/en/latest/"""

import functools
import operator
import cachetools
import time
import threading

# LFUCache(Least Frequently Used (LFU) cache implementation) 使用频率最少
# LRUCache(Least Recently Used (LRU) cache implementation)   最近未使用
# RRCache(Random Replacement (RR) cache implementation)      随机
# TTLCAche(LRU Cache implementation with per-item time-to-live (TTL) value)


@functools.lru_cache(maxsize=3)
def lru_cache(num: int):
    """最近未使用的缓存会被替换掉"""
    print("cal num =", num)
    return num * num


def test_lru_cache():
    [lru_cache(i) for i in [1, 1, 2, 3, 4, 1]]
    print(lru_cache.cache_info(), lru_cache.cache_clear())
    [lru_cache(i) for i in [1, 1, 2, 3, 4, 1]]


def ttl_cache():
    """直接使用, 带时间的cache"""
    ttl = 1  # second
    cache = cachetools.TTLCache(maxsize=3, ttl=ttl)
    cache.update([('a', 1), ('b', 2)])
    cache.update(c=3, d=4)
    cache['e'] = 5
    print("get c", cache.get('c'), cache.items())
    time.sleep(ttl)
    print("after sleep, get c", cache.get('c'), cache.items())


@cachetools.cached(cache=cachetools.TTLCache(maxsize=1, ttl=1), lock=threading.RLock())
def ttl_cache_decorator(num: int):
    """ 装饰器, 带时间的cache """
    print("cal num^2", num)
    return num ^ 2


def test_ttl_cache_decorator():
    [ttl_cache_decorator(i) for i in (1, 1, 3, 1)]
    print("get 1", ttl_cache_decorator(1))
    time.sleep(1)
    print("after sleep, get 1", ttl_cache_decorator(1))


def test_cache_class_decorator():
    """ 类方法装饰器 """
    class CachedTest(object):
        def __init__(self, cachesize):
            self.cache = cachetools.LRUCache(maxsize=cachesize)

        @cachetools.cachedmethod(operator.attrgetter('cache'))
        def get(self, num):
            print("get", num)
            return num ^ 2

    cache = CachedTest(3)
    print([cache.get(i) for i in (1, 1, 2)])


if __name__ == '__main__':
    # test_lru_cache()
    # ttl_cache()
    test_ttl_cache_decorator()
    # test_cache_class_decorator()
