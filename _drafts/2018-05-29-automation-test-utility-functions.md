---
title: 分享几个自动化测试中常用的功能函数
categories: [Tech]
tags: [python,automation,testing,tips]
date: 2018-05-29
---

## 前言

在自动化测试中会有很多意料之中意料之外的情况需要处理，你可以对特定的case写特定的逻辑，不过一些万金油式的功能函数还是能解决很多问题的。本文权当抛砖引玉，有兴趣的读者欢迎留言指教。

完整的代码示范请移步GitHub： https://github.com/tobyqin/python_automation_utils

## wait_for

### 函数实现

```python
def wait_for(method, timeout=DEFAULT_TIMEOUT, poll_time=DEFAULT_POLL_TIME):
    """
    Wait for a method with timeout, return its result or raise error.
    The expecting result should NOT be False or equal to False.
    """

    end_time = time.time() + timeout
    exc_info = ()

    while True:
        try:
            value = method()
            if value:
                return value

        except Exception as exc:
            args_as_str = [str(x) for x in exc.args]
            exc_info = (type(exc).__name__, ','.join(args_as_str))

        time.sleep(poll_time)
        if time.time() > end_time:
            break

    message = "Timeout to wait for '{}()' in {} seconds.".format(
        method.__name__, timeout)

    if exc_info:
        message += " [{}]: {}".format(exc_info[0], exc_info[1])

    raise Exception(message)
```

### 调用示范

```python
# 例一：等待页面
def page_ready():
    ...

wait_for(page_ready)
then_do_something()

# 例二：等待长操作
def calculation():
    # cost long time
    return something

result = wait_for(calculation,timeout=100,poll_time=10)
```

### 函数说明

###  已知问题

## 声明

- 本文所用编程语言均为Python，欢迎读者翻译成其他编程语言。
- 读者可以无偿将文中内容引用到任何项目中，但作者（我）以不承担由于这些内容造成的损失。
- 欢迎转载分享并注明出处，讨厌抄袭或者纯粹靠爬虫骗流量的平台。