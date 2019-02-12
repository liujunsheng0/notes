#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
使用相对导入看起来像是浏览文件系统, 但是不能到定义包的目录之外. 也就是说, 使用点的这种模式从不是包的目录中导入将会引发错误.

对于一个很大的模块, 可能只想组件在需要时被加载, 所以可用 延迟导入
延迟加载的真实例子, 见标准库 multiprocessing/__init__.py 的源码.

执行 python -m import_.import
"""

# 延迟倒入demo
from .pkg import (a, b)

# 从同层目录中的__init__.py中导入对象f
from . import f

# 相对导入
# from .._flask import docs

# 绝对导入, 在编辑器中能直接运行, 是因为工作路径为上一级目录, 所以能导入同级目录下的文件
# from _flask import docs

if __name__ == '__main__':
    print(f)
    print(a())
    print(b())
