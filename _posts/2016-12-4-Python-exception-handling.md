---
title: 总结：Python中的异常处理
categories: Coding
tags: Python
date: 2016-12-4
---

异常处理在任何一门编程语言里都是值得关注的一个话题，良好的异常处理可以让你的程序更加健壮，清晰的错误信息更能帮助你快速修复问题。在Python中，和不部分高级语言一样，使用了try/except/finally语句块来处理异常，如果你有其他编程语言的经验，实践起来并不难。

## 处理异常 try...excpet...finally

### 实例代码
```python
try:
  print 2/'0'
except ZeroDivisionError:
  print '除数不能为0'
except Exception:
  print '其他类型异常'

try:
  print 2/'0'
except (ZeroDivisionError,Exception):
  print '发生了一个异常'

try:
  print 2/'0'
except (ZeroDivisionError,Exception) as e:
  # unsupported operand type(s) for /: 'int' and 'str'
  print e
finally:
  print '不管是否发生异常都执行'
else:
  print '没有异常发生!'
```

### 总结如下
1. except语句不是必须的，finally语句也不是必须的，但是二者必须要有一个，否则就没有try的意义了。
2. except语句可以有多个，Python会按except语句的顺序依次匹配你指定的异常，如果异常已经处理就不会再进入后面的except语句。
3. except语句可以以元组形式同时指定多个异常，参见实例代码。

## 引发异常 raise

如果你需要自主抛出异常一个异常，可以使用raise关键字，等同于C#和Java中的throw语句，其语法规则如下。

```python
raise Exception("抛出一个异常")
```

raise 关键字后面需要指定你抛出的异常类型，一般来说抛出的异常越详细越好，Python在exceptions模块内建了很多的异常类型，通过使用dir函数来查看exceptions中的异常类型，如下：

```python
import exceptions

# ['ArithmeticError', 'AssertionError'.....]
print dir(exceptions)
```

## 自定义异常类型

Python中也可以自定义自己的特殊类型的异常，只需要要从Exception类继承(直接或间接)即可：
```python
class SomeCustomException(Exception):
  pass
```

## 经验案例

### 传递异常

捕捉到了异常，但是又想重新引发它(传递异常)，可以使用不带参数的raise语句即可：
```python
class MuffledCalculator:
  muffled = False
  def calc(self,expr):
    try:
      return eval(expr)
    except ZeroDivisionError:
      if self.muffled:
        print 'Division by zero is illegal'
      else:
        raise
```

### Exception 和 BaseException


### except Exception as e


### logging.exception()


### context manager (with 语句)

### sys.exc_info()

### raise "Exception string"


