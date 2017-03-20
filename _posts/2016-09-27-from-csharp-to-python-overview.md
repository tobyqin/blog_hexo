---
title: 从C#到Python - 语言特性和概览
tags: [C#,python]
date: 2016-09-27 09:35:13
categories: Tech
---

因为工作的原因，目前主力编程语言从C#转移到Python，所以在此记录这两种语言的一些异同点和自己的感悟收获。本系列文章数量不限，随想随写。

## 语言特性和特点

###  `C#`

C#是微软公司主推的编程语言，在Windows平台的首选开发语言，需要.net framework的支持，非微软平台支持目前并不完善。主要特点是语法简单，IDE强悍(VS是我用过最强悍和人性化的IDE，没有之一)，C#是强类型高级编程语言。

### `Python`

是开源的动态解释型语言，由Guido van Rossum于1989年发明。它天生具有跨平台的能力，默认集成在MacOS和Linux系统中。Windows平台需要单独安装。主要特点是语法简洁，第三方类库丰富强大，数据处理能力异常优秀。

### 漫谈瞎扯

我使用C#编程的时间大概有5年左右，对于它的各种特性还算比较了解。接触Python大概只有三个多月，不过三观已经被刷新。限于我个人水平，本文对C#和Python特别深入的东西不会特别介绍，仅从我个人的角度来帮助C#的程序猿认识Python。

很明显我感觉C#是**简单**，但Python是**简洁**。两个不完全一样的概念，简洁之中蕴含了简单，但是简洁也意味着信息的省略和丢失。举一些具体的例子

#### 标识语句块

C#用花括号，和大多数编程语言一样。

```csharp
using System;

namespace csharp_example
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            Console.WriteLine("Hello C#!");
        }
    }
}
```

而Python用的是缩进。

```python
def say_hello(name=None):
    if name is None:
        name = 'python!'

    print "hello", name

if __name__ == '__main__':
    say_hello()

```

#### 命名规则 

C#对文件系统的命名空间是System.IO。

```csharp
using System.IO;
```
Python只有io，只有两个字母，还是小写的！

```python
import os
```

#### 迭代语句 

C#中for迭代是这样的，已经很简洁了。

```csharp
var list = new List<int>() { 1,, 3, 4, 5, 5, 5, 6 };
foreach (var item in list)
{
    Console.WriteLine(item);
}
```

Python是这样的，真的不能再简洁了。

```python
list = [1, 2, 3, 4, 4, 5, 5, 6]
for i in list:
    print i
```

#### 其他

还有不少细节的地方在你接触Python之后也一定深有体会。
- 比如为了不切换大小写，Python推荐使用全小写的命名规范（类命名除外）
- Python要求省略句尾的分号
- Python不推荐在逻辑判断后使用括号，比如 `if i > 0:` 而不是 `if (i > 0):`

这样的例子枚不胜举，如果语意可读性上来说，我比较喜欢C#的做法，因为使用驼峰命名规则，基本上一个语句就是一小段英文。而且从命名规范上来说，C#推荐使用完整的英文单词来命名变量和类名。

Python就不见得了，很多类库和命名都是极度简洁的，比如`pytz`, `wrapt`, `isalnum()`。最令人发指的是居然连中间的下划线也省了，比如`altsep`, `execl`, `getcwdu`, `spawnle`，尼玛，这些是什么鬼，这一点也不考虑其他人的感受，很多时候你只能yy或者查文档，这就是简洁的代价。

不过话说回来，正因为Python这也省布料，所以使用Python实现与C#，JAVA相同功能，至少可以少20%的代码量。夸张的说法甚至60%到80%，我保留意见，但不得不承认是极有可能的。

最后从动态语言和非动态语言的角度简单说一下，动态语言的特点就是程序在运行时才能确定类型和行为，动态语言也叫鸭子类型`ducking typing`，源自于来自James Whitcomb Riley这句有名的话。

> If it looks like a duck, swims like a duck, and quacks like a duck, then it probably is a duck.
>
> 如果它看起来像一只鸭子，游起来也像鸭子，而且还会像鸭子一样叫，那么它极有可能就是一只鸭子。

在动态语言里变量只是一个标记，具体的行为可以在程序运行时才确定，比如两个变量相加，Python可以这样写：

```python
def add(a, b):
    return a + b
```

你不需要**也不能**指定这个a, b的类型，当程序在运行时，他们的相加行为会根据传入的具体类型确定。

```python
>>> add(1, 2)
3

>>> add([1,2,3], [4,5,6])
[1, 2, 3, 4, 5, 6]

>>> add('hi ', 'toby')
'hi toby'

>>> add('hi', 1)
Traceback (most recent call last):
  File "<pyshell#7>", line 1, in <module>
    add('hi', 1)
  File "<pyshell#2>", line 2, in add
    return a+b
TypeError: cannot concatenate 'str' and 'int' objects
>>> 
```

反观C#，Visual Studio会对你的语法进行检查，没有泛型之前，你只能这样写。

```csharp
public int AddInt(int a, int b)
{
  return a + b;
}

public string AddString(string a, string b)
{
  return a + b;
}
```

有泛型和dynamic类型之后，情况好一些。

```csharp
public T Add<T>(T a, T b)
{
    dynamic x = a;
    dynamic y = b;            
    return x + y;
}
```
然而这种和C#本身格格不入的编码方式并不流行，而且IDE支持也不好。或许你能从这个小例子明白动态语言的厉害之处。

### 小结

写了那么多，希望你对Python有一个比较直观的印象。

两种语言各有特点，不能说谁好谁坏。具体用哪个一般只有一个原因，工作环境和项目需求。但就学习而言，如果已经熟悉C#，转而学习Python还是比较简单和容易接受的，因为做的的减法。但是如果之前是Python而后转到C#，就不是那么好受了，因为做的是加法。

Python的作者有处女情节，所以处处都要追求优雅，简单，完美。想适应这种情节真的需要刷三观，费半条命。

而且写Python的人一般都短命，因为喜欢Python的人都喜欢这句话。

`Life is short, I use Python. （人生苦短，我用Python）`

> 本文源码地址：https://github.com/tobyqin/csharp_vs_python