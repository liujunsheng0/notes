#!/usr/bin/python3.7
# -*- coding: utf-8 -*-


"""
用于配置文件解析
"""

from configparser import ConfigParser


def main():
    cfg = ConfigParser()
    # 读取配置文件, 如果配置文件不存在则创建
    cfg.read('config.ini', encoding="utf-8")
    for i in cfg.sections():
        for j in cfg.options(i):
            print(f"section = {'%-5s' % i} option = {'%-8s' % j}  exist={cfg.has_option(i, j)} value = {cfg.get(i, j)}")
    # end for

    print()
    for i in ('redis', '11', "env"):
        print(f"cfg.has_section({'%-5s' % i}) = {cfg.has_section(i)}")

    print()
    for i in cfg.sections():
        print(cfg.items(i))


if __name__ == '__main__':
    main()
