---
title: Turn off logging in python selenium
tags: [python,selenium]
date: 2016-09-24 22:14:44
categories: tips
---
Python selenium will print a lot of debug info on selenium driver, which will mess up important information for your testing.

![](./images/selenium-debug-logging.png)

To turn it off, please add bellow code before test case.

```python
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)
```
**Note:** above code should be put before webdriver initialization.
