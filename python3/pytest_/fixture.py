#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import time

import pytest

"""
fixtue(固件)是一些函数, pytest会在执行测试函数之前(或之后)加载运行它们. 可以利用固件做任何事情, 其中最常见的可能就是数据库的初始连接和最后关闭操作
pytest 使用 pytest.fixture() 定义固件, fixture 可以作为其他测试函数的参数被使用

固件的作用域, 在定义固件时, 通过 scope 参数声明作用域, 可选项有
    function 函数级  每个测试函数都会执行一次固件(默认)
    class    类级别  每个测试类执行一次, 所有方法都可以使用
    module   模块级  每个模块执行一次, 模块内函数和方法都可使用
    session  会话级  一次测试只执行一次. 所有被找到的函数和方法都可用

固件自动执行, 在定义时指定 autouse=True
固件的名称默认为定义时的函数名, 可以通过 name 设置固件名

可以使用 yield 关键词将固件分为两部分: 
    yield 之前的代码属于预处理, 会在 测试 前执行;
    yield 之后的代码属于后处理, 会在 测试完成 后执行
"""


class TestFixtrue(object):
    """
    pytest 使用 yield 关键词将固件分为两部分,
        yield 之前的代码属于预处理, 会在 测试 前执行;
        yield 之后的代码属于后处理, 会在 测试完成 后执行
    $ pytest -sv -k search fixture.py
    """
    @pytest.fixture(scope='class')
    def db1(self):
        print('\nConnection1 successful')
        yield
        print('\nConnection1 closed')

    @pytest.fixture()
    def db2(self):
        print('\nConnection2 successful')
        yield
        print('\nConnection2 closed')

    def search_user(self, user_id):
        d = {'001': 'xiaoming'}
        return d.get(user_id)

    def test_search1(self, db1, db2):
        """ db为固件, pytest会自动赋值 """
        assert self.search_user('001') == 'xiaoming'

    def test_search2(self, db1, db2):
        assert self.search_user('002') is None


class TestFixtureAutoRun(object):
    """
    固件的自动执行
    $  pytest -sv -k run fixture.py
    """
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    @pytest.fixture(scope='session', autouse=True)
    def timer_session_scope(self):
        start = time.time()
        print('\nstart: {}'.format(time.strftime(self.DATE_FORMAT, time.localtime(start))))
        yield
        finished = time.time()
        print('finished: {}'.format(time.strftime(self.DATE_FORMAT, time.localtime(finished))))
        print('Total time cost: {:.3f}s'.format(finished - start))

    @pytest.fixture(autouse=True)
    def timer_function_scope(self):
        start = time.time()
        yield
        print(' Time cost: {:.3f}s'.format(time.time() - start))

    # 注意下面的两个测试函数并都没有显式使用固件
    def test_run1(self):
        time.sleep(1)

    def test_run2(self):
        time.sleep(2)


class TestFixtureParams(object):
    """
    固件参数化需要使用 pytest 内置的固件 request, 并通过 request.param 获取参数
    $  pytest -sv -k params fixture.py
    """
    @pytest.fixture(params=[('redis', '6379'), ('elasticsearch', '9200')], scope="class")
    def param(self, request):
        return request.param

    @pytest.fixture(autouse=True)
    def db(self, param):
        print('\nSucceed to connect %s:%s' % param)
        yield
        print('\nSucceed to close %s:%s' % param)

    def test_params(self):
        pass


class TestFixtureBuiltin(object):
    """
    内置固件
    tmpdir: 用于临时文件和目录管理, 默认会在测试结束时删除, tmpdir只有function 作用域, 只能在函数内使用
    tmpdir_factory: 可以在所有作用域使用, 包括 function, class, module, session

    """
    def test_tmpdir(self, tmpdir):
        a_dir = tmpdir.mkdir('mytmpdir')
        a_file = a_dir.join('tmpfile.txt')
        print(a_dir)
        a_file.write('hello, pytest!')
        assert a_file.read() == 'hello, pytest!'

    # 自定义固件
    @pytest.fixture(scope='module')
    def my_tmpdir_factory(self, tmpdir_factory):
        a_dir = tmpdir_factory.mktemp('mytmpdir')
        a_file = a_dir.join('tmpfile.txt')
        a_file.write('hello, pytest!')
        return a_file

    """
    monkeypath 用于运行时动态修改类或模块, 内置接口如下
        设置属性    setattr(target, name, value, raising=True)
        删除属性    delattr(target, name, raising=True)
        字典添加元素 setitem(dic, name, value)
        字典删除元素 delitem(dic, name, raising=True)
        设置环境变量 setenv(name, value, prepend=None)
        删除环境变量 delenv(name, raising=True)
        添加系统路径 syspath_prepend(path)
        切换目录    chdir(path)
        
        raising 用于通知 pytest 在元素不存在时是否抛出异常
        prepend 如果设置, 环境变量将变为 value+prepend+<old value> 
    """
