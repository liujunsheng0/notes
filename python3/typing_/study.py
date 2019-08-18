#!/usr/bin/python3.7
# -*- coding: utf-8 -*-

"""
https://docs.python.org/zh-cn/3/library/typing.html
静态类型检查
"""
import typing

vector_float = typing.List[float]
dict_str_str = typing.Dict[str, str]
address = typing.Tuple[str, int]
user_id = typing.NewType('usr_id', int)  # 闭包实现

# 期望特定的回调函数可以将类型标注为 Callable[[Arg1Type, Arg2Type], ReturnType]
return_none_func = typing.Callable[[int, Exception], None]
# 通过用文字省略号替换类型提示中的参数列表
return_int_func = typing.Callable[..., int]

# Any是一种特殊的类型, 静态类型检查器将所有类型视为与Any兼容,反之亦然, Any也与所有类型相兼容
any_type = typing.Any
union = typing.Union[int, float, str]
# typing.Optional[int] 等价于 typing.Union(int, None)

def func(a: vector_float, b:dict_str_str, c:address):
    # 可以对 usr_id 类型的变量执行所有的 int 支持的操作, 但结果将始终为 int 类型
    var_user_id = user_id(1) + user_id(2)
    for k, v in locals().items():
        print(f"{k}, {type(v)}, {v}")

    print("\n=====global=====")
    for k, v in globals().items():
        print(f"{k}, {type(v)}, {v}")


if __name__ == '__main__':
    # 提示类型变量错误
    func(['a'], {1:1}, (1, 1))
