---
title: 说说Python中的单元测试
categories: [Tech]
tags: [Python,unittest,pytest]
date: 2018-04-08
---

单元测试是每种编程语言必学的课题，是保护开发者的强力护盾，每个程序员都在时间允许的情况下尽可能多的写单元测试，今天我们不讨论其必要性，只抛砖引玉聊一聊Python中单元测试的恩怨情仇。本文仅代表个人看法，仅供参考。

## 标准库中难以忍受的unittest

很多时候我们总是认为标准库里的带的总是精挑细选的，如果不经过仔细打磨怎么可能入选为一等公民？然后我要告诉你，Python标准库里的单元测试框架真不是最好的，随着你对Python的熟悉你甚至会讨厌这个unittest，为什么呢？

因为Python一直崇尚简单，优雅，高效地完成事情，当你写完一个函数需要测试一下时，使用标准库你需要做这些事情：

- 新建单元测试脚本
- 导入单元测试依赖
- **继承单元测试类**
- 实现单元测试方法

具体的实例代码如下：

```python
import unittest

class IntegerArithmeticTestCase(unittest.TestCase):
    def testAdd(self):  # test method names begin with 'test'
        self.assertEqual((1 + 2), 3)
        self.assertEqual(0 + 1, 1)

if __name__ == '__main__':
    unittest.main()
```

看上去还行，不是很难。但是渐渐地你会吐槽：

- 为啥我要新建一个文件来写测试？
- 为啥我要继承一个类来写测试？
- 为啥我要用unittest的Assertion来做断言？
- 为啥unitunit的命名规则跟最佳实践不一样（`mixedCase` vs `lower_case`）？

要回答以上问题，答案只有一个：[历史原因](https://www.quora.com/Will-Pythons-unittest-module-become-pythonic-anytime-soon)。

很久很久以前，Python从Java借鉴了单元测试框架，包括命名规则和实现方式，一直沿用至今。不得不说这个框架没啥毛病，该有的功能的都有，想做的事都可以做，但是用起来总是没有爽的感觉。

但是为啥伟大的社区力量为啥不把这个框架改的爽一点呢？没办法，为了兼容和世界和平，你要知道Python这个庞然大物能健康地活着，后面有无数的类库和方法在支撑，而这些类库和方法都被单元测试保护着，如果修改了单元测试框架导致case挂了，你就成了千古罪人。

## 见识简洁的单元测试

Python中很多大牛其实都有严重的强迫症，追求简洁和优雅的代码。必然的，他们会抛弃标准库中的unittest，使用或者发明自己心仪的单元测试框架。

### pytest

正如其名，这是一个无数人推荐并在使用的Python单元测试框架，pytest 使用起来非常简单，只要你的方法名是以 `test_` 开头就可以，你可以和需要测试的方法放在一起，亦或是新建一个文件来专门存放单元测试，都可以。


```python
def your_func():
  pass

def test_your_func():
  assert result
```
这样的设计，就让你写单元测试成了顺手拈来的事，假如你写完了一个方法，想看看是否work，在旁边直接写上一个`test_` 开头的方法，稍微准备一下数据就可以验证这个方法好不好用，岂不妙哉？

## 让单元测试和IDE无缝集成

## 闲话和总结