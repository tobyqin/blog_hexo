---
title: 一款优秀的代码高亮库 - rainbow.js
categories: [tech]
tags: [javascript, code-highlight]
date: 2017-07-17
---

RainbowJS 项目地址： https://github.com/ccampbell/rainbow

## 缘起

代码高亮的js库也不少，最知名的莫过于 [highlightjs](https://highlightjs.org/)，支持你听过的没听过的各种编程语言，兼容你用过没用过的各种浏览器，有着多姿多彩的配色方案。然而，唯有一点我还是选择放弃了它，因为它不能很方便的自定义高亮语言。

现在我的需求是是这样的，有一个测试结果的页面，里面会显示一个测试案例的数据，以及控制台输出 stdout， 我需要高亮控制台输出的一些信息，比较 INFO 级别是默认色，WARN 级别是橙色，ERROR 级别是红色。

```
...
2017-07-14 11:53:55,668 INFO   : Go to my account page
2017-07-14 11:53:58,071 DEBUG  : Now check: MyAccountPage
2017-07-14 11:53:59,804 WARNING: Page loaded time > 2000 ms
2017-07-14 11:54:01,535 ERROR  : Test failed!!!
...
```

像这样的自定义需求highlightjs就不是那么灵活，估计你需要把这整个库的代码拉下来，读懂它的开发和编译流程，才能勉强实现这样的需求。

## 初试 RainbowJS

RainbowJS 虽然简单而且支持的编程语言也不多（压缩后大小只有不到3kb），但是恰恰能满足自定义高亮的需求。入门只需要三步即可：

### 导入主题配色文件

官方的github 仓库里提供了 20 多种配色，常见的都可以找得到。

```html
<link href="/rainbow/css/theme.css" rel="stylesheet" type="text/css">
```

### 使用 `<pre><code>` 包住你的代码

在 `code` 标签里你可以使用`data-language` 指定代码语言。

```html
<pre><code data-language="python">def openFile(path):
    file = open(path, "r")
    content = file.read()
    file.close()
    return content</code></pre>
```

### 开始高亮你的代码

如果整个过程是同步的，那么你只需要在页面最后导入RainbowJS和你你需要的高亮语言库，就可以自动高亮代码块。

```html
<script src="/js/rainbow.js"></script>
<script src="/js/language/generic.js"></script>
<script src="/js/language/python.js"></script>
```

如果你的代码块是异步生成的，你可以选择提前引入相关语言的js文件，然后调用`Rainbow.color()`方法来给代码着色。

```Js
// load rainbow js and language support
...
// call your function to generate dyanmc code blocks
...
// finally, highligh your code blocks
Rainbow.color();
// optionally, you can pass in a callback function in color()
// for example:
Rainbow.color(function() {
    console.log('The new blocks are now highlighted!');
});
```



## 高亮自定义语言

