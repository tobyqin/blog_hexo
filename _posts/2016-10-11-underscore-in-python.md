---
title: Python中的下划线和双下划线
date: 2016-10-11 22:26:46
tags: [python,python underscore,tips]
categories: Tech
---
### 开门见山

下划线在Python中有特殊的意义，简单来说，可以总结成两点。

1. 单下划线一般用于声明私有成员。
2. 双下划线一般被用于Python内置的特殊方法或者属性。

更多细节的讨论，可以看StackOverflow上的这个主题 http://stackoverflow.com/questions/1301346/the-meaning-of-a-single-and-a-double-underscore-before-an-object-name-in-python。

### 思维导图

下面是思维导图的总结

![](images/underscore-in-Python.png)

### 附录： 如何调用魔法方法

一些魔法方法直接和内建函数对应，这种情况下，如何调用它们是显而易见的。然而，另外的情况下，调用魔法方法的途径并不是那么明显。这个附录旨在展示那些不那么明显的调用魔法方法的语法。

| 魔法方法                              | 什么时候被调用                            | 解释                 |
| --------------------------------- | ---------------------------------- | ------------------ |
| `__new__(cls [,...])`             | `instance = MyClass(arg1, arg2)`   | `__new__`在实例创建时调用  |
| `__init__(self [,...])`           | `instance = MyClass(arg1,arg2)`    | `__init__`在实例创建时调用 |
| `__cmp__(self)`                   | `self == other`, `self > other` 等  | 进行比较时调用            |
| `__pos__(self)`                   | `self`                             | 一元加法符号             |
| `__neg__(self)`                   | `-self`                            | 一元减法符号             |
| `__invert__(self)`                | `~self`                            | 按位取反               |
| `__index__(self)`                 | `x[self]`                          | 当对象用于索引时           |
| `__nonzero__(self)`               | `bool(self)`                       | 对象的布尔值             |
| `__getattr__(self, name)`         | `self.name` #name不存在               | 访问不存在的属性           |
| `__setattr__(self, name)`         | `self.name = val`                  | 给属性赋值              |
| `__delattr__(self, name)`         | `del self.name  `                  | 删除属性               |
| `__getattribute__(self,name)`     | `self.name`                        | 访问任意属性             |
| `__getitem__(self, key)`          | `self[key]`                        | 使用索引访问某个元素         |
| `__setitem__(self, key)`          | `self[key] = val`                  | 使用索引给某个元素赋值        |
| `__delitem__(self, key)`          | `del self[key]`                    | 使用索引删除某个对象         |
| `__iter__(self)`                  | `for x in self`                    | 迭代                 |
| `__contains__(self, value)`       | `value in self, value not in self` | 使用in进行成员测试         |
| `__call__(self [,...])`           | `self(args)`                       | “调用”一个实例           |
| `__enter__(self)`                 | `with self as x:`                  | with声明的上下文管理器      |
| `__exit__(self, exc, val, trace)` | `with self as x:`                  | with声明的上下文管理器      |
| `__getstate__(self)`              | `pickle.dump(pkl_file, self)`      | Pickling           |
| `__setstate__(self)`              | `data = pickle.load(pkl_file)`     | Pickling           |

如果你还想了解关于魔方方法的更多细节，那么你一定不能错过：

-	魔法方法指南 http://pyzh.readthedocs.io/en/latest/python-magic-methods-guide.html
-	Magic method guide: http://www.rafekettler.com/magicmethods.html

