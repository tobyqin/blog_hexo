---
title: 设置 Python Selenium 中的Log显示信息
tags: [python,selenium,logging,tips]
date: 2016-09-24 22:14:44
categories: Tech
---
Python Selenium默认会往控制台和Log文件里写入大量的DEBUG信息，比如下面这张图。这样的相信在测试过程中有一定帮助，但大部分情况下都是没有营养的，而且会把你自己打印的Log信息淹没在汪洋大海中。

![](images/selenium-debug-logging.png)

如果想要停止显示或者关闭Selenium中的Log，你可以通过以下代码更改其默认LOGGER的级别。

```python
import logging
from selenium.webdriver.remote.remote_connection import LOGGER

LOGGER.setLevel(logging.WARNING)
```
**注意：**以上代码一定要在初始化`WebDriver`前进行。