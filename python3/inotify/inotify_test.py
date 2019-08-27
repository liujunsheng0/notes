#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from threading import Thread
from time import sleep

import pyinotify

"""
note:    https://github.com/liujunsheng0/notes/blob/master/linux/Linux%20Programming%20Interface/test/part19/19.cpp
实验环境: Linux
目的:    使用inotify机制实现tail -f的功能
"""


class ProcessTransientFile(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
        line = fd.readline()
        if line:
            print(event, 'modify:', line, end='')


filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test.txt')
fw = open(filename, 'w', buffering=1)


def write():
    for i in range(10):
        sleep(1)
        fw.write(f"{i}\n")


Thread(target=write).start()

with open(filename, 'r') as fd:
    st_results = os.stat(filename)
    st_size = st_results[6]
    fd.seek(st_size)
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm)
    wm.watch_transient_file(filename, pyinotify.IN_MODIFY, ProcessTransientFile)
    notifier.loop()

fw.close()
