---
title: 使用timeit测试Python函数的性能
categories: [Tech]
tags: [Python]
date: 2020-03-04
layout: post
---
`timeit`是Python标准库内置的小工具，可以快速测试小段代码的性能。

<!-- more -->

## 认识timeit

timeit 函数：

```python
timeit.timeit(stmt, setup,timer, number)
```

参数说明：

- **stmt**: statement的缩写，你要测试的代码或者语句，纯文本，默认值是 "pass"
- **setup**: 在运行`stmt`前的配置语句，纯文本，默认值也是 "pass"
- **timer**: 计时器，一般忽略这个参数
- **number**: `stmt`执行的次数，默认是1000000，一百万

repeat 函数：

```python
timeit.repeat(stmt, setup, timer, repeat, number)
```

是timeit的repeat版，可以指定重复timeit的次数，默认是3次，然后返回一个数组。

举一个简单的例子来说明用法：

```python
import timeit

print(timeit.timeit('output = 10*5')) 
# 0.014560436829924583

print(timeit.repeat('output = 10*5')) 
# [0.01492984383367002, 0.01342877489514649, 0.013638464966788888]
```

嗯，看上去没毛病，实际上谁也不会去测没有意义的加减乘除，我们需要测试自己的代码。

## 测试多行代码

测试多行代码可以用分号来连接语句。

```python
print(timeit.timeit(stmt='a=10;b=10;sum=a+b'))
```

也可以用三引号来写stmt。

```python
import timeit
import_module = "import random"
testcode = ''' 
def test(): 
    return random.randint(10, 100)
'''
print(timeit.repeat(stmt=testcode, setup=import_module))
```

但是其实都挺扯的，自己的代码会那么简单？我们是模块化编程。

## 测试模块中的函数

如果你要测试的函数都在一个模块里，可以这样写timeit。

```python
import timeit
import random
import arrow

# 本地函数
def stupid1():
    return random.randint(1, 10)

# 依赖其他函数
def stupid2():
    return stupid1()

# 依赖其他包或者模块
def stupid3():
    return arrow.now()

print(timeit.timeit('stupid1()', setup='from __main__ import stupid1'))
print(timeit.timeit('stupid2()', setup='from __main__ import stupid2'))
print(timeit.timeit('stupid3()', setup='from __main__ import stupid3', number=100))
```

写成上面这样的其实还是单行的模式。

## 借用default_timer

timeit自带的default_timer可以借来用一下。

```python
import timeit
import random
 
def test(): 
    return random.randint(10, 100)
 
starttime = timeit.default_timer()
print("The start time is :",starttime)
test()
print("The time difference is :", timeit.default_timer() - starttime)
```

## 命令行的用法

timeit还支持命令行的调用方式，不过我觉得敲参数太累了，没必要去尝试。

```
C:\pythontest>python -m timeit -s 'text="hello world"'
20000000 loops, best of 5: 13.1 nsec per loop
```

## 分享一个案例

2月29那天，我想今年是闰年啊，计算闰年有几种算法啊？孔乙己说有3种：

```python
def is_leap_year_0(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def is_leap_year_1(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def is_leap_year_2(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    return False
```

这三种方法那种最好啊？这个不能一概而论吧，因为要看你的参数是什么，比如1991年不是闰年，方法0和方法1直接就返回了，但方法2还需要走到最后一个if才知道不是闰年。再比如2020年，方法2直接就返回了，但是方法0和1需要走到最里层的if才得到结果。所以我们需要取样测试才公平，比如从1900年到2900年，每个函数都跑10000遍。

timeit就不太方便了，它接受的参数哪能那么复杂，我们需要包装一下。

```python
def perf_test(method):
    years = range(1900, 2900)
    if method == 0:
        for y in years:
            is_leap_year_0(y)

    if method == 1:
        for y in years:
            is_leap_year_1(y)

    if method == 2:
        for y in years:
            is_leap_year_2(y)

print(timeit('perf_test(0)', setup='from __main__ import perf_test', number=10000))
print(timeit('perf_test(1)', setup='from __main__ import perf_test', number=10000))
print(timeit('perf_test(2)', setup='from __main__ import perf_test', number=10000))
```

你们猜猜看哪个方法结果最好？你一定想不到。

```
1.6432780250906944
1.7527272370643914
0.0023122059646993876
```

## 其他的思路

`timeit`其实还是太弱了，随便测测还凑合，如果真要检查性能问题还是需要用更专业的手段。比如：

- [PyCharm Profiler](https://www.jetbrains.com/help/pycharm/profiler.html) （Pro版功能）
- [cProfile](https://docs.python.org/3/library/profile.html#module-cProfile)
- [pycallgraph](http://pycallgraph.slowchop.com/)
- [memory_profiler](https://pypi.org/project/memory-profiler/)

有机会我们下次再说。

