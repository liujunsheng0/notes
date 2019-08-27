#!/usr/bin/python3.7
# -*- coding: utf-8 -*-

from abc import abstractmethod, ABC


# 抽象类不能实例化
class Animal(ABC):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    # 抽象方法, 子类必须实现
    @abstractmethod
    def say(self):
        """
        抽象类会在实现的抽象方法和抽象特性上强制实施规则, 但它不会对参数和返回值进行一致性检查,
        所以, 抽象类不会检查子类是否使用了与抽象方法相同的参数和返回值, 但是最好和抽象方法保持一致的输入和输出类型.
        """
        pass


class Dog(Animal):
    def __init__(self, name=''):
        super().__init__(name)

    def say(self):
        return "汪汪汪"


class Cat(Animal):
    def __init__(self, name):
        super().__init__(name)

    def say(self):
        return "喵喵喵"


def _isinstance():
    dog = Dog('小D')
    cat = Cat('小C')
    print(isinstance(dog, Dog), isinstance(cat, Cat))         # True
    print(isinstance(dog, Animal), isinstance(cat, Animal))   # True
    print(dog.name, dog.say())
    print(cat.name, cat.say())


def _register():
    """
    抽象基类支持对已经存在的类进行注册, 使其属于该基类, 使用register()进行注册.
    向抽象基类注册某个类时, 对于注册类的实例, 涉及抽象基类的类型检查操作(isinstance,issubclass)将返回True.
    向抽象类注册某个类时, 不会检查该类是否实现了抽象方法/特性. 这种注册只影响类型检查, 它不会向注册的类进行额外的错误检查.
    """
    a = 1
    print(isinstance(a, Animal))
    Animal.register(int)
    print(isinstance(a, Animal))


if __name__ == '__main__':
    # Animal()
    _isinstance()
    _register()
