#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import pytest

"""
pytest 使用文件 conftest.py 集中管理固件
在复杂的项目中, 可以在不同的目录层级定义 conftest.py, 其作用域为其所在的目录和子目录
不要自己显式调用 conftest.py, pytest 会自动调用, 可以把 conftest 当做插件来理解

使用 pytestconfig, 可以很方便的读取命令行参数和配置文件. 在conftest.py中使用函数 pytest_addoption (特定的 hook function)

markers用来标记测试, 以便于选择性的执行测试用例. pytest 提供了一些内建的 marker：
    # 跳过测试
    @pytest.mark.skip(reason=None)

    # 满足某个条件时跳过该测试
    @pytest.mark.skipif(condition)

    # 预期该测试是失败的
    @pytest.mark.xfail(condition, reason=None, run=True, raises=None, strict=False)

    # 参数化测试函数. 给测试用例添加参数, 供运行时填充到测试中
    # 如果 parametrize 的参数名称与 fixture 名冲突, 则会覆盖掉 fixture
    @pytest.mark.parametrize(argnames, argvalues)

    # 让测试尽早地被执行
    @pytest.mark.tryfirst

    # 让测试尽量晚执行
    @pytest.mark.trylast
    
    自定义marker
    @pytest.mark.old_test
    def test_one():
        assert False
"""


def pytest_addoption(parser):
    """ 添加命令行选项 """
    parser.addoption("--host", action="store", default="127.0.0.1", help="host of db")
    parser.addoption("--port", action="store", default="8888",      help="port of db")


# fixture 函数可以通过接受 request 对象来反向获取请求中的测试函数, 类或模块上下文
@pytest.fixture(scope="session")
def config(request):
    return request.config


def test_option(config):
    """
    $ pytest -s conftest.py
    """
    print("host: %s" % config.getoption("host"))
    print("port: %s" % config.getoption("port"))


def pytest_configure(config):
    """
    @pytest.mark.mytag 自定义标签
    避免此warning: Unknown pytest.mark.finish - is this a typo?  You can register custom marks to avoid this warning -
    for details, see https://docs.pytest.org/en/latest/mark.html

    """
    config.addinivalue_line("markers", "finish: mark test to run only on named environment")
    config.addinivalue_line("markers", "commit: mark test to run only on named environment")
    config.addinivalue_line("markers", "unfinish: mark test to run only on named environment")
