# 装饰器

## 定义

一般而言，如果需要给某些函数添加额外的功能，如统计运行时间，则需要修改函数的源代码，逐一修改太麻烦了，**装饰器就是专门的解决方案**！

装饰器的定义主要从**两个不同层面**进行说明的。

在Python里面有两层定义：

1. 从设计模式的层面上 - 代码重用

   装饰器是一个很著名的设计模式，经常被用于有切面需求的场景，较为经典的应用有插入日志、增加计时逻辑来检测性能、加入事务处理等。装饰器是解决这类问题的绝佳设计，**有了装饰器，我们就可以抽离出大量函数中与函数功能本身无关的雷同代码并继续重用**。概括的讲，装饰器的作用就是为已经存在的对象添加额外的功能。

2. 从Python的语法层面上（其实第二种本质上也是第一种，只不过在语法上进行了规范化）

   简言之，python装饰器就是用于拓展原来函数功能的一种函数，这个函数的特殊之处在于它的返回值也是一个函数，使用python装饰器的好处就是在不用更改原函数的代码前提下给函数增加新的功能。 如此一来，我们要想拓展原来函数功能，就不需要再在函数里面修改源代码了。

## 作用

1. 抽离雷同代码，加以重用
2. 为函数添加额外的功能

## 使用场景

装饰器可能在我们平时的编码中比较少去自己定义，更多的是我们使用别人的已经编写好的装饰器，比如我们我们经常使用的@staticmethod，@classmethod，@property等等，都是别人写好了，我们自己不需要自己再实现了，在编码中，我们在下面的一些情况会经常遇见装饰器。

+ 缓存装饰器
+ 权限验证装饰器
+ 计时装饰器
+ 日志装饰器
+ 路由装饰器
+ 异常处理装饰器
+ 错误重试装饰器



## 模板

为了能够明确装饰器的实现原理，这里给出一个关于装饰器的”一般模板“，但是，装饰器作为一种设计模式，本身没有固定的设计模板，语法也相对较为灵活，没有说一定要怎么写才正确。

模板如下：

```python
def decorator(function):
    """
    第一层函数为装饰器名称
    function：参数，即需要装饰的函数
    return：返回值wrapper，为了保持与原函数参数一致
    """
    def wrapper(*arg, **kwargs):
        """
        内层函数，这个函数实现“添加额外功能”的任务
        *arg,**kwargs：参数保持与需要装饰的函数参数一致，这里用*arg和**kwargs代替
        """
        #这里就是额外功能代码
        function(*arg,**kwargs)   #执行原函数
        #这里就是额外功能代码
    return wrapper
```

## 分类

+ 函数装饰函数

+ 函数装饰类

+ 类装饰函数

+ 类装饰类



## 缺点

+ 被函数装饰器所装饰的对象（函数、类）已经不再是它本身了，虽然从形式上看没有变化，本质上是函数装饰器的内部wrapper
+ 被类装饰器所装饰的对象（函数、类）也不再是它本身了，虽然从形式上看没有变化，本质上是类装饰器的一个对象。



参考链接

[Python高级编程——装饰器Decorator超详细讲解（上篇）](https://mp.weixin.qq.com/s/5gFl2BQSzTNbGR4fZQn1Xg)

[Python高级编程——装饰器Decorator超详细讲解(中篇)](https://mp.weixin.qq.com/s/HVZymCKnU5bJrQ3BRiH8rw)

[Python高级编程——装饰器Decorator超详细讲解(下篇之python闭包详解)](https://mp.weixin.qq.com/s/dziy9MUMN_nGbPyQvuZJ9Q)
