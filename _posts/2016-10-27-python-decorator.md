---
title: 详解Python的装饰器
categories: Coding
tags: Python
date: 2016-10-27
---

Python中的装饰器是你进入Python大门的一道坎，不管你跨不跨过去它都在那里。

## 为什么需要装饰器

我们假设你的程序实现了`say_hello()`和`say_goodbye()`两个函数。

```python
def say_hello():
    print "hello!"
    
def say_goodbye():
    print "hello!"  # bug here

if __name__ == '__main__':
    say_hello()
    say_goodbye()
```

但是在实际调用中，我们发现程序出错了，上面的代码打印了两个hello。经过调试你发现是`say_goodbye()`里出错了。你的老板要求在调用每个方法前都要打印一下进入当前函数的时间，比如这样：

```
[DEBUG] 2016-10-27 11:11:11 - Enter say_hello()
Hello!
[DEBUG] 2016-10-27 11:11:11 - Enter say_goodbye()
Goodbye!
```

好，小A是个毕业生，他是这样实现的。

```python
def say_hello():
    print "[DEBUG]: enter say_hello()"
    print "hello!"

def say_goodbye():
    print "[DEBUG]: enter say_goodbye()"
    print "hello!"

if __name__ == '__main__':
    say_hello()
    say_goodbye()
```

很low吧？ 小B工作有一段时间了，他是这样写的。

```python
def debug():
    import inspect
    caller_name = inspect.stack()[1][3]
    print "[DEBUG]: enter {}()".format(caller_name)   

def say_hello():
    debug()
    print "hello!"

def say_goodbye():
    debug()
    print "goodbye!"

if __name__ == '__main__':
    say_hello()
    say_goodbye()
```

是不是好一点？那当然，但是一个业务函数里凭空多出一个`debug()`函数，是不是很难受？那么装饰器这时候应该登场了。

> 装饰器本质上是一个Python函数，它可以让其他函数在不需要做任何代码变动的前提下增加额外功能，装饰器的返回值也是一个函数对象。它经常用于有切面需求的场景，比如：插入日志、性能测试、事务处理、缓存、权限校验等场景。装饰器是解决这类问题的绝佳设计，有了装饰器，我们就可以抽离出大量与函数功能本身无关的雷同代码并继续重用。

概括的讲，装饰器的作用就是**为已经存在的对象添加额外的功能**。

## 怎么写一个装饰器

在早些时候 (Python Version <= 2.4),为一个函数添加额外功能的写法是这样的。

```python
def debug(func):
    def wrapper():
        print "[DEBUG]: enter {}()".format(func.__name__)
        print 'Prepare and say...',
        return func()
    return wrapper

def say_hello():
    print "hello!"

say_hello = debug(say_hello)  # 添加功能并保持原函数名不变
```

上面的debug函数其实已经是一个装饰器了，它对原函数做了包装并返回了另外一个函数，额外添加了一下功能。因为这样写实在不太优雅，在新版本的Python中支持了@语法糖，下面代码等同于早期的写法。

```python
def debug(func):
    def wrapper():
        print "[DEBUG]: enter {}()".format(func.__name__)
        print 'Prepare and say...',
        return func()
    return wrapper

@debug
def say_hello():
    print "hello!"
```

这是最简单的装饰器，但是有一个问题，如果被装饰的函数需要参数，那么这个装饰器就坏了。因为返回的已经装饰过的函数并不能接受参数，你可以指定装饰器函数就接收和原函数一样的参数，比如：

```python
def debug(func):
    def wrapper(something):  # 指定一毛一样的参数
        print "[DEBUG]: enter {}()".format(func.__name__)
        print 'Prepare and say...',
        return func(something)
    return wrapper  # 返回包装过函数

@debug
def say(something):
    print "hello {}!".format(something)
```

这样你就解决了一个问题，但又多了N个问题。因为目标函数有千千万，你只管你自己的函数，别人的函数参数是什么样子，鬼知道？还好Python提供了可变参数`*args`和关键字参数`**kwargs`，有了这两个参数，装饰器就可以用于任意目标函数了。

```python
def debug(func):
    def wrapper(*args, **kwargs):  # 指定宇宙无敌参数
        print "[DEBUG]: enter {}()".format(func.__name__)
        print 'Prepare and say...',
        return func(*args, **kwargs)
    return wrapper  # 返回包装过函数

@debug
def say(something):
    print "hello {}!".format(something)
```

至此，你已完全掌握初级的装饰器写法。

## 高级一点的装饰器



## 装饰器里的那些坑



## 如何优化你的装饰器



## 小结


> 本文源码 https://github.com/tobyqin/python_decorator
