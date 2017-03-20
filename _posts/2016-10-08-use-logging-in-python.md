---
title: Python中的logging模块
date: 2016-10-08 20:57:43
tags: [python,logging]
categories: Tech
---
最近修改了项目里的logging相关功能，用到了python标准库里的logging模块，在此做一些记录。主要是从官方文档和stackoverflow上查询到的一些内容。

- [官方文档](https://docs.python.org/2.7/library/logging.html)
- [技术博客](http://blog.csdn.net/balderfan/article/details/7644807)

## 基本用法
下面的代码展示了logging最基本的用法。

```python
# -*- coding: utf-8 -*-

import logging
import sys

# 获取logger实例，如果参数为空则返回root logger
logger = logging.getLogger("AppName")

# 指定logger输出格式
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')

# 文件日志
file_handler = logging.FileHandler("test.log")
file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter  # 也可以直接给formatter赋值

# 为logger添加的日志处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 指定日志的最低输出级别，默认为WARN级别
logger.setLevel(logging.INFO)

# 输出不同级别的log
logger.debug('this is debug info')
logger.info('this is information')
logger.warn('this is warning message')
logger.error('this is error message')
logger.fatal('this is fatal message, it is same as logger.critical')
logger.critical('this is critical message')

# 2016-10-08 21:59:19,493 INFO    : this is information
# 2016-10-08 21:59:19,493 WARNING : this is warning message
# 2016-10-08 21:59:19,493 ERROR   : this is error message
# 2016-10-08 21:59:19,493 CRITICAL: this is fatal message, it is same as logger.critical
# 2016-10-08 21:59:19,493 CRITICAL: this is critical message

# 移除一些日志处理器
logger.removeHandler(file_handler)
```

除了这些基本用法，还有一些常见的小技巧可以分享一下。

### 格式化输出日志
```python
# 格式化输出
service_name = "Booking"
logger.error('%s service is down!' % service_name)  # 使用python自带的字符串格式化，不推荐
logger.error('%s service is down!', service_name)  # 使用logger的格式化，推荐
logger.error('%s service is %s!', service_name, 'down')  # 多参数格式化
logger.error('{} service is {}'.format(service_name, 'down')) # 使用format函数，推荐

# 2016-10-08 21:59:19,493 ERROR   : Booking service is down!
```

### 记录异常信息

当你使用logging模块记录异常信息时，不需要传入该异常对象，只要你直接调用`logger.error()` 或者 `logger.exception()`就可以将当前异常记录下来。

```python
# 记录异常信息
try:
    1 / 0
except:
    # 等同于error级别，但是会额外记录当前抛出的异常堆栈信息
    logger.exception('this is an exception message')

# 2016-10-08 21:59:19,493 ERROR   : this is an exception message
# Traceback (most recent call last):
#   File "D:/Git/py_labs/demo/use_logging.py", line 45, in <module>
#     1 / 0
# ZeroDivisionError: integer division or modulo by zero
```

### logging配置要点

#### GetLogger()
这是最基本的入口，该方法参数可以为空，默认的logger名称是root，如果在同一个程序中一直都使用同名的logger，其实会拿到同一个实例，使用这个技巧就可以跨模块调用同样的logger来记录日志。

另外你也可以通过日志名称来区分同一程序的不同模块，比如这个例子。

```python
logger = logging.getLogger("App.UI")
logger = logging.getLogger("App.Service")
```

#### Formatter
Formatter对象定义了log信息的结构和内容，构造时需要带两个参数：
- 一个是格式化的模板`fmt`，默认会包含最基本的`level`和 `message`信息
- 一个是格式化的时间样式`datefmt`，默认为 `2003-07-08 16:49:45,896 (%Y-%m-%d %H:%M:%S)`

`fmt`中允许使用的变量可以参考下表。
- **%(name)s**       Logger的名字
- **%(levelno)s**    数字形式的日志级别
- **%(levelname)s**  文本形式的日志级别
- **%(pathname)s**    调用日志输出函数的模块的完整路径名，可能没有
- **%(filename)s**       调用日志输出函数的模块的文件名
- **%(module)s**      调用日志输出函数的模块名|
- **%(funcName)s**   调用日志输出函数的函数名|
- **%(lineno)d**           调用日志输出函数的语句所在的代码行
- **%(created)f**         当前时间，用UNIX标准的表示时间的浮点数表示|
- **%(relativeCreated)d**  输出日志信息时的，自Logger创建以来的毫秒数|
- **%(asctime)s**     字符串形式的当前时间。默认格式是“2003-07-08 16:49:45,896”。逗号后面的是毫秒
- **%(thread)d**         线程ID。可能没有
- **%(threadName)s**     线程名。可能没有
- **%(process)d**        进程ID。可能没有
- **%(message)s**        用户输出的消息

#### SetLevel
Logging有如下级别: DEBUG，INFO，WARNING，ERROR，CRITICAL
默认级别是WARNING，logging模块只会输出指定level以上的log。这样的好处, 就是在项目开发时debug用的log，在产品release阶段不用一一注释，只需要调整logger的级别就可以了，很方便。

#### Handler
最常用的是StreamHandler和FileHandler, Handler用于向不同的输出端打log。
Logging包含很多handler, 可能用到的有下面几种
- **StreamHandler** instances send error messages to streams (file-like objects).
- **FileHandler** instances send error messages to disk files.
- **RotatingFileHandler** instances send error messages to disk files, with support for maximum log file sizes and log file rotation.
- **TimedRotatingFileHandler** instances send error messages to disk files, rotating the log file at certain timed intervals.
- **SocketHandler** instances send error messages to TCP/IP sockets.
- **DatagramHandler** instances send error messages to UDP sockets.
- **SMTPHandler** instances send error messages to a designated email address.

#### Configuration
logging的配置大致有下面几种方式。
1. 通过代码进行完整配置，参考开头的例子，主要是通过getLogger方法实现。
2. 通过代码进行简单配置，下面有例子，主要是通过basicConfig方法实现。
3. 通过配置文件，下面有例子，主要是通过 `logging.config.fileConfig(filepath)`

##### logging.basicConfig

basicConfig提供了非常便捷的方式让你配置logging模块并马上开始使用，可以参考下面的例子。具体可以配置的项目请查阅[官方文档](https://docs.python.org/2/library/logging.html#logging.basicConfig)。

```python
import logging
logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.debug('This message should appear on the console')

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.warning('is when this event was logged.')
```
备注： 其实你甚至可以什么都不配置直接使用默认值在控制台中打log，用这样的方式替换print方法对日后项目维护会有很大帮助。

##### 通过文件配置logging

如果你希望通过配置文件来管理logging，可以参考这个[官方文档](https://docs.python.org/2/library/logging.config.html)。在log4net或者log4j中这是很常见的方式。
```ini
# logging.conf
[loggers]
keys=root

[logger_root]
level=DEBUG
handlers=consoleHandler
#,timedRotateFileHandler,errorTimedRotateFileHandler

#################################################
[handlers]
keys=consoleHandler,timedRotateFileHandler,errorTimedRotateFileHandler

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout,)

[handler_timedRotateFileHandler]
class=handlers.TimedRotatingFileHandler
level=DEBUG
formatter=simpleFormatter
args=('debug.log', 'H')

[handler_errorTimedRotateFileHandler]
class=handlers.TimedRotatingFileHandler
level=WARN
formatter=simpleFormatter
args=('error.log', 'H')

#################################################
[formatters]
keys=simpleFormatter, multiLineFormatter

[formatter_simpleFormatter]
format= %(levelname)s %(threadName)s %(asctime)s:   %(message)s
datefmt=%H:%M:%S

[formatter_multiLineFormatter]
format= ------------------------- %(levelname)s -------------------------
 Time:      %(asctime)s
 Thread:    %(threadName)s
 File:      %(filename)s(line %(lineno)d)
 Message:
 %(message)s

datefmt=%Y-%m-%d %H:%M:%S
```
假设以上的配置文件放在和模块相同的目录，代码中的调用如下。
```python
import os
filepath = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(filepath)
return logging.getLogger()
```

### 日志重复输出的坑

你有可能会看到你打的日志会重复显示多次，可能的原因有很多，但总结下来无非就一个，日志中多个重复的handler。

#### 第一坑 

```python
import logging

logging.basicConfig(level=logging.DEBUG)

fmt = '%(levelname)s:%(message)s'
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(fmt))
logging.getLogger().addHandler(console_handler)

logging.info('hello!')

# INFO:root:hello!
# INFO:hello!
```

上面这个例子出现了重复日志，因为在第3行调用`basicConfig()`方法时系统会默认创建一个handler，如果你再添加一个控制台handler时就会出现重复日志。

#### 第二坑

```python
import logging

def get_logger():
    fmt = '%(levelname)s:%(message)s'
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(fmt))
    logger = logging.getLogger('App')
    logger.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    return logger

def call_me():
    logger = get_logger()
    logger.info('hi')

call_me()
call_me()

# INFO:hi
# INFO:hi
# INFO:hi
```

在这个例子里`hi`居然打印了三次，如果再调用一次`call_me()`呢？我告诉你会打印6次。why? 因为你每次调用`get_logger()`方法时都会给它加一个新的handler，你是自作自受。正常的做法应该是全局只配置logger一次。

#### 第三坑

```python
import logging

def get_logger():
    fmt = '%(levelname)s: %(message)s'
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(fmt))
    logger = logging.getLogger('App')
    logger.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    return logger

def foo():
    logging.basicConfig(format='[%(name)s]: %(message)s')
    logging.warn('some module use root logger')

def main():
    logger = get_logger()
    logger.info('App start.')
    foo()
    logger.info('App shutdown.')

main()

# INFO: App start.
# [root]: some module use root logger
# INFO: App shutdown.
# [App]: App shutdown.
```

为嘛最后的`App shutdown`打印了两次？所以在Stackoverflow上很多人都问，我应该怎么样把root logger关掉，root logger太坑爹坑妈了。只要你在程序中使用过root logger，那么默认你打印的所有日志都算它一份。上面的例子没有什么很好的办法，我建议你招到那个没有经过大脑就使用root logger的人，乱棍打死他或者开除他。

如果你真的想禁用root logger，有两个不是办法的办法：

```python
logging.getLogger().handlers = []  # 删除所有的handler
logging.getLogger().setLevel(logging.CRITICAL)  # 将它的级别设置到最高
```

### 小结

Python中的日志模块作为标准库的一部分，功能还是比较完善的。个人觉得上手简单，另外也支持比如过滤，文件锁等高级功能，能满足大多数项目需求。

不过切记，小心坑。





