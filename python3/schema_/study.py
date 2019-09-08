#!/usr/bin/python3.7
# -*- coding: utf-8 -*-


"""
schema: 数据类型验证库
"""
import re

from schema import Schema, And, Or, Optional, Regex, Forbidden, Use

"""
Schema(self, schema, error=None, ignore_extra_keys=False, name=None)
    
    ignore_extra_keys: 不验证字典中多余的key
    error: 自定义错误信息

Schema.is_valid(data): 如果data是所指定的类型或函数返回True, 返回True, 否则返回False
Schema.validate(data): 如果data是所指定的类型或函数返回True, 则返回传入的数据, 否则抛出一个SchemaError的异常
"""


def _valid(s: Schema, data=None, tag: str=""):
    for i in (data or ('', '1', '11', 1, 10, [])):
        if tag:
            print(f'tag={tag}', end=' ')
        print('data=%-5s' % i, s.is_valid(i))


def schema_base_type():
    """ 传入基本数据类型 """
    _valid(Schema(int))


def schema_container():
    """ 传入容器类型, list set tuple """
    s = Schema([int, float, list, str])
    # 只需满足list/tuple/set中的其中一个条件后会返回当前的值, 不满足则抛出异常
    print(s.validate([1, 2, 3, 3.3, '', []]))  # [1, 2, 3, 3.3, '', []]
    print(s.is_valid([1, 2, 3, 3.3, '', []]))  # True
    print(s.is_valid([1, 2, 3, 3.3, '', ()]))  # False
    print(s.is_valid(1))                       # False, 传入为单个值时, 不是判断满足其中一个条件
    print(s.is_valid([]))                      # True


def schema_dict():
    """
    Schema类传入的字典, 称之为模式字典, validate方法传入的字典称之为数据字典
    Schema会判断模式字典和数据字典的key是否完全一样, 不一样的话直接抛出异常.
    如果一样, 拿数据字典的value去验证模式字典相应的value, 如果数据字典的全部value都可以验证通过的话才返回数据, 否则抛出异常
    """
    s = Schema({'name': str, 'age': int})
    for i in ({'name': 'foobar', 'age': 18},  # True
              {'name': 'foobar'}):            # False
        print('%-5s' % s.is_valid(i), i)

    # Optional 代码该key可有可无, 如果有, 则验证; 无, 则忽略
    s = Schema({'name': str, Optional('age'): int})
    for i in ({'name': 'foobar', 'age': 18},  # True
              {'name': 'foobar'}):            # True
        print('%-5s' % s.is_valid(i), i)

    # 禁止有某个key
    # dict中禁止有key等于name
    s = Schema({Forbidden('name'): str, 'age': int})
    for i in ({"age": 15},                 # {'age': 15}
              {"name": "jim", "age": 15},  # Forbidden key encountered: 'name' in {'name': 'laozhang', 'age': 15}
              1):                          # 1 should be instance of 'dict'
        try:
            print(s.validate(i))
        except Exception as e:
            print(e)


def schema_callable():
    """ 传入可调用的对象 """
    _valid(Schema(lambda x: x < 10))


def schema_with_validate():
    """ 传入带有validate方法的对象, And Or... """
    # 同时满足
    _valid(Schema(And(str, len)), tag='and')
    # 满足其中一个
    _valid(Schema(Or(int, list, float)), tag='or')


def schema_regex():
    # flags 忽悠大小写
    s = Regex('^foo', flags=re.I)
    for i in ('football', 'basketball', 'Football'):
        try:
            print(s.validate(i))
        except Exception as e:
            print(e)


def schema_use():
    # 类型转换
    s = Use(int)
    for i in ('1', '11', 1, 10, []):
        try:
            t = s.validate(i)
            print('%-5s' % i, type(t), t)
        except Exception as e:
            print('%-5s' % i, e)


if __name__ == '__main__':
    # schema_base_type()
    # schema_container()
    # schema_dict()
    # schema_callable()
    schema_with_validate()
    # schema_regex()
    # schema_use()
