---
title: 也说说Python中的闭包 - Closure
categories: Coding
tags: Python
date: 2016-10-23
---

Python中的闭包不是一个一说就能明白的概念，但是随着你往学习的深入，无论如何你还是需要去了解这么一个东西。

## 闭包的概念

我们从概念上尝试去理解一些闭包。

> 在一些语言中，在函数中可以（嵌套）定义另一个函数时，如果内部的函数引用了外部的函数的变量，则可能产生闭包。闭包可以用来在一个函数与一组“私有”变量之间创建关联关系。在给定函数被多次调用的过程中，这些私有变量能够保持其持久性。
> —— [维基百科](https://zh.wikipedia.org/wiki/%E9%97%AD%E5%8C%85_(%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%A7%91%E5%AD%A6))

用比较容易懂的人话说，就是当某个**函数**被当成对象返回时，**夹带了外部变量**，就形成了一个闭包。看例子。

```python
def make_printer(msg):
    def printer():
        print msg  # 夹带私货
    return printer  # 返回的是函数，带私货的函数

printer = make_printer('Foo!')
printer()
```

## 如何理解闭包

为什么需要闭包？我们怎么理解闭包存在的意义呢？

我个人认为，闭包存在的意义就是它夹带的那些私货，如果它不夹带私货，它和普通的函数没有任何区别。其实闭包和面向接口编程的概念很像，可以把闭包理解成轻量级的接口封装。

```python
def tag(name):
    def add_tag(content):
        return "<{0}>{1}</{0}>".format(name, content)
    return add_tag

content = 'Hello'

add_tag = tag('a')
print add_tag(content)
# <a>Hello</a>

add_tag = tag('b')
print add_tag(content)
# <b>Hello</b>
```

在这个例子里，我们只是想要一个给content加tag的功能，但是具体的tag是什么样子的要根据实际需求来定，对外部的接口已经确定，就是`add_tag(for_content)`，如果按照传统的方式实现，我们可能会把先把`add_tag`写成接口，指定参数和返回类型。然后分别去实现a和b的`add_tag`功能。

但是在闭包的概念中，`add_tag`就是一个函数，它需要两个参数tag和content，只不过tag这个参数是打包带走的。所以一开始就可以告诉我怎么打包，然后带走就行。

在我们生活和工作中，闭包的概念也很常见。比如说手机就是一个闭包，你只关心能不能打电话，而不会去纠结它是怎么实现的，用到了哪些模块。再比如去餐馆吃饭，你只要付钱点菜就可以享受到服务，你并不知道那桌饭菜用了多少地沟油。这些都可以看成闭包，返回来的是一些功能或者服务，但是这些功能使用了外部变量。

## 怎么使用闭包

在Python中最常使用闭包的地方之一就是装饰器Decorator，假如你需要写一个带参数的装饰器，那么必然会生成闭包。为什么？因为Python的装饰器是一个固定语法接口。

```python
def foo():
    pass

def decorate(func):
    return func

foo = decorate(foo)

foo()

```


## 参考链接

- https://www.the5fire.com/closure-in-python.html
- https://zh.wikipedia.org/wiki/%E9%97%AD%E5%8C%85_(%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%A7%91%E5%AD%A6)
- http://stackoverflow.com/questions/4020419/why-arent-python-nested-functions-called-closures



