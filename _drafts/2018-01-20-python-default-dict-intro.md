---
title: 认识 Python 中的 defaultdict
categories: [Tech]
tags: [python,defaultdict]
date: 2018-01-20
---

今天看到一篇讲defaultdict的PPT，同时第一次见到`__missing__()`这个方法，好奇之下，仔细阅读了这篇PPT。看完之后随手做笔记，分享给有需要的人。准确地说，这篇文章不是纯粹的翻译，因为原文本身只是一份PPT。文章的大多数文字内容，都是本人的阅读心得。

### 默认值可以很方便

众所周知，在Python中如果访问字典中不存在的键，会引发KeyError异常（JavaScript中如果对象中不存在某个属性，则返回undefined）。但是有时候，字典中的每个键都存在默认值是非常方便的。例如下面的例子：

```
strings = ('puppy', 'kitten', 'puppy', 'puppy',
           'weasel', 'puppy', 'kitten', 'puppy')
counts = {}

for kw in strings:
    counts[kw] += 1
```

该例子统计strings中某个单词出现的次数，并在counts字典中作记录。单词每出现一次，在counts相对应的键所存的值数字加1。但是事实上，运行这段代码会抛出KeyError异常，出现的时机是每个单词第一次统计的时候，因为Python的dict中不存在默认值的说法，可以在Python命令行中验证：

```
>>> counts = dict()
>>> counts
{}
>>> counts['puppy'] += 1
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'puppy'
```

### 使用判断语句检查

既然如此，首先可能想到的方法是在单词第一次统计的时候，在counts中相应的键存下默认值1。这需要在处理的时候添加一个判断语句：

```
strings = ('puppy', 'kitten', 'puppy', 'puppy',
           'weasel', 'puppy', 'kitten', 'puppy')
counts = {}

for kw in strings:
    if kw not in counts:
        counts[kw] = 1
    else:
        counts[kw] += 1

# counts:
# {'puppy': 5, 'weasel': 1, 'kitten': 2}
```

### 使用`dict.setdefault()`方法

也可以通过`dict.setdefault()`方法来设置默认值：

```
strings = ('puppy', 'kitten', 'puppy', 'puppy',
           'weasel', 'puppy', 'kitten', 'puppy')
counts = {}

for kw in strings:
    counts.setdefault(kw, 0)
    counts[kw] += 1 # 原PPT中这里有一个笔误
```

`dict.setdefault()`方法接收两个参数，第一个参数是健的名称，第二个参数是默认值。假如字典中不存在给定的键，则返回参数中提供的默认值；反之，则返回字典中保存的值。利用`dict.setdefault()`方法的返回值可以重写for循环中的代码，使其更加简洁：

```
strings = ('puppy', 'kitten', 'puppy', 'puppy',
           'weasel', 'puppy', 'kitten', 'puppy')
counts = {}

for kw in strings:
    counts[kw] = counts.setdefault(kw, 0) + 1
```

### 使用`collections.defaultdict`类

以上的方法虽然在一定程度上解决了dict中不存在默认值的问题，但是这时候我们会想，有没有一种字典它本身提供了默认值的功能呢？答案是肯定的，那就是`collections.defaultdict`。

defaultdict类就好像是一个dict，但是它是使用一个类型来初始化的：

```
>>> from collections import defaultdict
>>> dd = defaultdict(list)
>>> dd
defaultdict(<type 'list'>, {})
```

defaultdict类的初始化函数接受一个类型作为参数，当所访问的键不存在的时候，可以实例化一个值作为默认值：

```
>>> dd['foo']
[]
>>> dd
defaultdict(<type 'list'>, {'foo': []})
>>> dd['bar'].append('quux')
>>> dd
defaultdict(<type 'list'>, {'foo': [], 'bar': ['quux']})
```

需要注意的是，这种形式的默认值只有在通过`dict[key]`或者`dict.__getitem__(key)`访问的时候才有效，这其中的原因在下文会介绍。

```
>>> from collections import defaultdict
>>> dd = defaultdict(list)
>>> 'something' in dd
False
>>> dd.pop('something')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'pop(): dictionary is empty'
>>> dd.get('something')
>>> dd['something']
[]
```

defaultdict类除了接受类型名称作为初始化函数的参数之外，还可以使用任何不带参数的可调用函数，到时该函数的返回结果作为默认值，这样使得默认值的取值更加灵活。下面用一个例子来说明，如何用自定义的不带参数的函数zero()作为defaultdict类的初始化函数的参数：

```
>>> from collections import defaultdict
>>> def zero():
...     return 0
...
>>> dd = defaultdict(zero)
>>> dd
defaultdict(<function zero at 0xb7ed2684>, {})
>>> dd['foo']
0
>>> dd
defaultdict(<function zero at 0xb7ed2684>, {'foo': 0})
```

利用`collections.defaultdict`来解决最初的单词统计问题，代码如下：

```
from collections import defaultdict

strings = ('puppy', 'kitten', 'puppy', 'puppy',
           'weasel', 'puppy', 'kitten', 'puppy')
counts = defaultdict(lambda: 0)  # 使用lambda来定义简单的函数

for s in strings:
    counts[s] += 1
```

### defaultdict类是如何实现的

通过上面的内容，想必大家已经了解了defaultdict类的用法，那么在defaultdict类中又是如何来实现默认值的功能呢？这其中的关键是使用了看`__missing__()`这个方法：

```
>>> from collections import defaultdict
>>> print defaultdict.__missing__.__doc__
__missing__(key) # Called by __getitem__ for missing key; pseudo-code:
  if self.default_factory is None: raise KeyError(key)
  self[key] = value = self.default_factory()
  return value
```

通过查看`__missing__()`方法的docstring，可以看出当使用`__getitem__()`方法访问一个不存在的键时(dict[key]这种形式实际上是`__getitem__()`方法的简化形式)，会调用`__missing__()`方法获取默认值，并将该键添加到字典中去。

关于`__missing__()`方法的具体介绍可以参考Python官方文档中的"[Mapping Types — dict](http://docs.python.org/library/stdtypes.html#dict)"一节。

文档中介绍，从2.5版本开始，如果派生自dict的子类定义了`__missing__()`方法，当访问不存在的键时，dict[key]会调用`__missing__()`方法取得默认值。

从中可以看出，虽然dict支持`__missing__()`方法，但是在dict本身是不存在这个方法的，而是需要在派生的子类中自行实现这个方法。可以简单的验证这一点：

```
>>> print dict.__missing__.__doc__
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: type object 'dict' has no attribute '__missing__'
```

同时，我们可以进一步的做实验，定义一个子类Missing并实现`__missing__()`方法:

```
>>> class Missing(dict):
...     def __missing__(self, key):
...         return 'missing'
...
>>> d = Missing()
>>> d
{}
>>> d['foo']
'missing'
>>> d
{}
```

返回结果反映了`__missing__()`方法确实发挥了作用。在此基础上，我们稍许修改`__missing__()`方法,使得该子类同defautldict类一样为不存在的键设置一个默认值：

```
>>> class Defaulting(dict):
...     def __missing__(self, key):
...         self[key] = 'default'
...         return 'default'
...
>>> d = Defaulting()
>>> d
{}
>>> d['foo']
'default'
>>> d
{'foo': 'default'}
```

### 在旧版本的Python中实现类defaultdict的功能

defaultdict类是从2.5版本之后才添加的，在一些旧版本中并不支持它，因此为旧版本实现一个兼容的defaultdict类是必要的。这其实很简单，虽然性能可能未必如2.5版本中自带的defautldict类好，但在功能上是一样的。

首先，`__getitem__()`方法需要在访问键失败时，调用`__missing__()`方法：

```
class defaultdict(dict):
    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)
```

其次，需要实现`__missing__()`方法用来设置默认值：

```
class defaultdict(dict):
    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        self[key] = value = self.default_factory()
        return value
```

然后，defaultdict类的初始化函数`__init__()`需要接受类型或者可调用函数参数:

```
class defaultdict(dict):
    def __init__(self, default_factory=None, *a, **kw):
        dict.__init__(self, *a, **kw)
        self.default_factory = default_factory

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        self[key] = value = self.default_factory()
        return value
```

最后，综合以上内容，通过以下方式完成兼容新旧Python版本的代码：

```
try:
    from collections import defaultdict
except ImportError:
    class defaultdict(dict):
      def __init__(self, default_factory=None, *a, **kw):
          dict.__init__(self, *a, **kw)
          self.default_factory = default_factory

      def __getitem__(self, key):
          try:
              return dict.__getitem__(self, key)
          except KeyError:
              return self.__missing__(key)

      def __missing__(self, key):
          self[key] = value = self.default_factory()
          return value
```



在Python里面有一个模块collections，解释是数据类型容器模块。这里面有一个collections.defaultdict()经常被用到。主要说说这个东西。

 

综述：

这里的*defaultdict(function_factory)*构建的是一个类似*dictionary*的对象，其中*keys*的值，自行确定赋值，但是*values*的类型，是*function_factory*的类实例，而且具有默认值。比如*default(int)*则创建一个类似*dictionary*对象，里面任何的*values*都是*int*的实例，而且就算是一个不存在的*key*, *d[key]* 也有一个默认值，这个默认值是*int()*的默认值0.

 

[`defaultdict`](mk:@MSITStore:C:%5CPython32%5CDoc%5CPython323.chm::/library/#collections.defaultdict) 
dict subclass that calls a factory function to supply missing values。

这是一个简短的解释

defaultdict属于内建函数dict的一个子类，调用工厂函数提供缺失的值。

 

比较晕，什么是工厂函数：

来自python 核心编程的解释

 

Python 2.2 统一了类型和类， 所有的内建类型现在也都是类， 在这基础之上， 原来的 
所谓内建转换函数象int(), type(), list() 等等， 现在都成了工厂函数。 也就是说虽然他 
们看上去有点象函数， 实质上他们是类。当你调用它们时， 实际上是生成了该类型的一个实 
例， 就象工厂生产货物一样。 
下面这些大家熟悉的工厂函数在老的Python 版里被称为内建函数： 
int(), long(), float(), complex() 
str(), unicode(), basestring() 
list(), tuple() 
type() 
以前没有工厂函数的其他类型，现在也都有了工厂函数。除此之外，那些支持新风格的类 
的全新的数据类型，也添加了相应的工厂函数。下面列出了这些工厂函数： 
dict() 
bool() 
set(), frozenset() 
object() 
classmethod() 
staticmethod() 
super() 
property() 
file()

 

再看看它的使用：

[![复制代码](http://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
import collections
s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]

d = collections.defaultdict(list)
for k, v in s:
    d[k].append(v)

list(d.items())
```

[![复制代码](http://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

 

这里就开始有点明白了，原来defaultdict可以接受一个内建函数list作为参数。其实呢，list()本身是内建函数，但是再经过更新后，python里面所有东西都是对象，所以list改编成了类，引入list的时候产生一个类的实例。

 

还是不太明白，再看defaultdict的help解释

- *class *`collections.``defaultdict`([*default_factory*[, *...*]])

  Returns a new dictionary-like object. [`defaultdict`](mk:@MSITStore:C:%5CPython32%5CDoc%5CPython323.chm::/library/#collections.defaultdict) is a subclass of the built-in [`dict`](mk:@MSITStore:C:%5CPython32%5CDoc%5CPython323.chm::/library/stdtypes.html#dict) class. It overrides one method and adds one writable instance variable. The remaining functionality is the same as for the [`dict`](mk:@MSITStore:C:%5CPython32%5CDoc%5CPython323.chm::/library/stdtypes.html#dict) class and is not documented here.

首先说了，collections.defaultdict会返回一个类似dictionary的对象，注意是类似的对象，不是完全一样的对象。这个defaultdict和dict类，几乎是一样的，除了它重载了一个方法和增加了一个可写的实例变量。（可写的实例变量，我还是没明白）

 

The first argument provides the initial value for the [`default_factory`](mk:@MSITStore:C:%5CPython32%5CDoc%5CPython323.chm::/library/#collections.defaultdict.default_factory) attribute; it defaults to `None`. All remaining arguments are treated the same as if they were passed to the [`dict`](mk:@MSITStore:C:%5CPython32%5CDoc%5CPython323.chm::/library/stdtypes.html#dict) constructor, including keyword arguments.

[`defaultdict`](mk:@MSITStore:C:%5CPython32%5CDoc%5CPython323.chm::/library/#collections.defaultdict) objects support the following method in addition to the standard [`dict`](mk:@MSITStore:C:%5CPython32%5CDoc%5CPython323.chm::/library/stdtypes.html#dict) operations:

- `__missing__`(*key*)

  If the [`default_factory`](mk:@MSITStore:C:%5CPython32%5CDoc%5CPython323.chm::/library/#collections.defaultdict.default_factory) attribute is `None`, this raises a [`KeyError`](mk:@MSITStore:C:%5CPython32%5CDoc%5CPython323.chm::/library/exceptions.html#KeyError) exception with the *key* as argument.If [`default_factory`](mk:@MSITStore:C:%5CPython32%5CDoc%5CPython323.chm::/library/#collections.defaultdict.default_factory) is not `None`, it is called without arguments to provide a default value for the given *key*, this value is inserted in the dictionary for the *key*, and returned.

  主要关注这个话，如果default_factory不是None, 这个default_factory将以一个无参数的形式被调用，提供一个默认值给___missing__方法的key。 这个默认值将作为key插入到数据字典里，然后返回。

  十分晕。有扯出了个__missing__方法，这个__missing__方法是collections.defaultdict()的内建方法。

If calling [`default_factory`](mk:@MSITStore:C:%5CPython32%5CDoc%5CPython323.chm::/library/#collections.defaultdict.default_factory) raises an exception this exception is propagated unchanged.

This method is called by the [`__getitem__()`](mk:@MSITStore:C:%5CPython32%5CDoc%5CPython323.chm::/reference/datamodel.html#object.__getitem__) method of the [`dict`](mk:@MSITStore:C:%5CPython32%5CDoc%5CPython323.chm::/library/stdtypes.html#dict) class when the requested key is not found; whatever it returns or raises is then returned or raised by [`__getitem__()`](mk:@MSITStore:C:%5CPython32%5CDoc%5CPython323.chm::/reference/datamodel.html#object.__getitem__).

Note that [`__missing__()`](mk:@MSITStore:C:%5CPython32%5CDoc%5CPython323.chm::/library/#collections.defaultdict.__missing__) is *not* called for any operations besides [`__getitem__()`](mk:@MSITStore:C:%5CPython32%5CDoc%5CPython323.chm::/reference/datamodel.html#object.__getitem__). This means that `get()` will, like normal dictionaries, return `None` as a default rather than using [`default_factory`](mk:@MSITStore:C:%5CPython32%5CDoc%5CPython323.chm::/library/#collections.defaultdict.default_factory).

[`defaultdict`](mk:@MSITStore:C:%5CPython32%5CDoc%5CPython323.chm::/library/#collections.defaultdict) objects support the following instance variable:

- `default_factory`

  This attribute is used by the [`__missing__()`](mk:@MSITStore:C:%5CPython32%5CDoc%5CPython323.chm::/library/#collections.defaultdict.__missing__) method; it is initialized from the first argument to the constructor, if present, or to `None`, if absent.



看样子这个文档是难以看懂了。直接看示例：


```
import collections
s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]

# defaultdict
d = collections.defaultdict(list)
for k, v in s:
    d[k].append(v)

# Use dict and setdefault    
g = {}
for k, v in s:
    g.setdefault(k, []).append(v)
    


# Use dict
e = {}
for k, v in s:
    e[k] = v


##list(d.items())
##list(g.items())
##list(e.items())
```


看看结果


```
list(d.items())
[('blue', [2, 4]), ('red', [1]), ('yellow', [1, 3])]
>>> list(g.items())
[('blue', [2, 4]), ('red', [1]), ('yellow', [1, 3])]
>>> list(e.items())
[('blue', 4), ('red', 1), ('yellow', 3)]
>>> d
defaultdict(<class 'list'>, {'blue': [2, 4], 'red': [1], 'yellow': [1, 3]})
>>> g
{'blue': [2, 4], 'red': [1], 'yellow': [1, 3]}
>>> e
{'blue': 4, 'red': 1, 'yellow': 3}
>>> d.items()
dict_items([('blue', [2, 4]), ('red', [1]), ('yellow', [1, 3])])
>>> d["blue"]
[2, 4]
>>> d.keys()
dict_keys(['blue', 'red', 'yellow'])
>>> d.default_factory
<class 'list'>
>>> d.values()
dict_values([[2, 4], [1], [1, 3]])
```


可以看出

collections.defaultdict(list)使用起来效果和运用dict.setdefault()比较相似

python help上也这么说了

When each key is encountered for the first time, it is not already in the mapping; so an entry is automatically created using the `default_factory` function which returns an empty [`list`](mk:@MSITStore:C:%5CPython32%5CDoc%5CPython323.chm::/library/functions.html#list). The `list.append()` operation then attaches the value to the new list. When keys are encountered again, the look-up proceeds normally (returning the list for that key) and the `list.append()` operation adds another value to the list. This technique is simpler and faster than an equivalent technique using [`dict.setdefault()`](mk:@MSITStore:C:%5CPython32%5CDoc%5CPython323.chm::/library/stdtypes.html#dict.setdefault):

 

说这种方法会和dict.setdefault()等价，但是要更快。

有必要看看dict.setdefault()

- `setdefault`(*key*[, *default*])

  If *key* is in the dictionary, return its value. If not, insert *key* with a value of *default* and return *default*. *default* defaults to `None`.

如果这个key已经在dictionary里面存着，返回value.如果key不存在，插入key和一个default value,返回Default. 默认的defaults是None.

 

但是这里要注意的是defaultdict是和dict.setdefault等价，和下面那个直接赋值是有区别的。从结果里面就可以看到，直接赋值会覆盖。

 

从最后的d.values还有d[“blue”]来看，后面的使用其实是和dict的用法一样的，唯一不同的就是初始化的问题。defaultdict可以利用工厂函数，给初始keyi带来一个默认值。

这个默认值也许是空的list[]  defaultdict(list), 也许是0, defaultdict(int).

 

再看看下面的这个例子。

defaultdict(int) 这里的d其实是生成了一个默认为0的带key的数据字典。你可以想象成 d[key] = int default （int工厂函数的默认值为0）

 

d[k]所以可以直接读取 d[“m”] += 1 就是d[“m”] 就是默认值 0+1 = 1

后面的道理就一样了。



```
>>> s = 'mississippi'
>>> d = defaultdict(int)
>>> for k in s:
...     d[k] += 1
...
>>> list(d.items())
[('i', 4), ('p', 2), ('s', 4), ('m', 1)]
```




https://docs.python.org/2/library/collections.html#collections.defaultdict