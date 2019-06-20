#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import pytest

"""
https://learning-pytest.readthedocs.io/zh/latest/doc/test-function/skip.html
http://kuanghy.github.io/2018/05/08/pytest

pytest 使用 . 表示测试通过
       使用 F 表示测试失败,  FAIL
       使用 s 表示测试被跳过, skip
       使用 x 表示预见的失败, XFAIL

pytest 查找测试策略: 
    1) 会递归查找当前目录下以test_开头或/_test结尾的文件
    2) 测试类以Test开头，并且不能带有 init 方法
    2) 测试函数以test_开头
    
标记测试函数:
    显示指定函数名 pytest test.py::test_func
    模糊搜索      pytest -k func1 test.py, 只运行测试案例名称中包含func1的
    使用pytest.mark在函数上进行标记, 详见TestMark, 使用命令'pytest -m 标记的信息 test.py', 只会执行指定标记的测试方法

pytest参数
    -v            用于显示每个测试函数的执行结果
    -q            只显示整体测试结果
    -k "pattern"  只执行测试案例名中包含指定字符串的测试案例, 模糊匹配
    -s            用于显示测试函数中print()函数输出
    -m "mark"     只运行指定标记的测试函数, 详见TestMark
    -x            首次失败后停止执行
    
    --maxfail=2       两次失败之后停止执行
    --resultlog path  生成HTML格式报告
    --setup-show      更细的跟踪固件执行
"""


class TestAssert(object):
    """
    使用断言编写测试案例
    $ pytest -k assert base.py
    """
    def test_assert1(self):
        assert (1, 2, 3) == (1, 2, 3), "assert 失败时显示的异常信息"

    def test_assert2(self):
        assert 1 == 2, "值不相等"


class TestException(object):
    """
    捕获异常, 测试是否如期抛出预期的异常
    $ pytest -k raise base.py
    """
    def test_raises(self):
        with pytest.raises(ValueError) as e:
            int('a')
        assert "invalid" in e.value.args[0]


class TestMark(object):
    """ 
    给函数打标记, 标记是自己指定的, 可以命名为finish, unfinish, commit...
    一个函数可以打多个标记, 多个函数也可以打相同的标记

    运行测试时使用 -m 选项可以加上逻辑, 如：
        $ pytest -m "finish and commit"
        $ pytest -m "finish and not merged"
    测试命令: 
        $ pytest -v -m "finish and commit" base.py
        $ pytest -v -m "finish or unfinish" base.py
        $ pytest -v -m finish base.py
        $ pytest -v -m unfinish base.py
    
    """

    @pytest.mark.commit
    @pytest.mark.finish
    def test_1(self):
        pass

    @pytest.mark.finish
    def test_2(self):
        pass

    @pytest.mark.unfinish
    def test_3(self):
        pass


class TestSkip(object):
    """ 
    pytest.mark.skip可以跳过测试
    pytest.mark.skipif, 当条件为true时忽略测试函数

    执行命令： $ pytest -v -k skip base.py
    """

    @pytest.mark.skip(reason="test")
    def test_skip1(self):
        assert 1 == 2

    @pytest.mark.skipif(1 == 1, reason="test")
    def test_skip2(self):
        """ 为测试函数指定被忽略的条件, 如果条件为True则忽略测试函数, 如果条件为False则执行 """
        assert 1 == 2

    @pytest.mark.skipif(1 > 1, reason="test")
    def test_skip3(self):
        assert 1 == 2


class TestXfail(object):
    """ 可预见的失败
        如果条件为True, 说明测试肯定失败, 标记为x但是不会标记为失败 
        如果条件为False, 和正常测试案例一样
        执行命令: $ pytest -v -k xfail base.py
    """

    @pytest.mark.xfail(1 == 2, reason='not supported until v0.2.0')
    def test_xfail1(self):
        assert 1 != 1

    @pytest.mark.xfail(1 < 2, reason='not supported until v0.2.0')
    def test_xfail2(self):
        assert 1 != 1


class TestParam(object):
    """
    参数化测试, 当对一个测试函数进行测试时, 通常会给函数传递多组参数. 比如测试账号登陆, 我们需要模拟各种千奇百怪的账号密码.
    即每组参数都 独立 执行一次测试. 使用的工具就是 'pytest.mark.parametrize(argnames, argvalues)'
    
    $ pytest -v -k md5 base.py 
    """
    # 多个参数, 相当于多个测试案例,
    @pytest.mark.parametrize('user, passwd', [('jack', 'abcdefgh'), ('tom', 'a123456a')])
    def test_passwd_md5(self, user, passwd):
        db = {
            'jack': 'e8dc4081b13434b45189a720b77b6818',
            'tom': '1702a132e769a623c1adb78353fc9503'
        }

        import hashlib
        assert hashlib.md5(passwd.encode()).hexdigest() == db[user]


if __name__ == '__main__':
    TestException().test_raises()
