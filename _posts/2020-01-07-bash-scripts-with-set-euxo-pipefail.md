---
title: Bash 脚本中的 set -euxo pipefail
categories: [Tech]
tags: [bash,shell]
date: 2020-01-07
---

有些开发人员会用Bash来实现很复杂的功能，就像使用别的高级语言一样。他可能觉得自己很牛逼但其他人早就想锤爆他了，Bash的可读性和可维护性远远低于任何高级语言。更要命的是，Bash并没有方便的调试工具和防错机制，出了问题你要排查半天。

<!-- more -->

在Ruby或者Python等高级语言里，你很容易知道错误是哪行什么类型的错误，还有IDE的Debugger加持。而Bash只能看源码，通过打印log等非常低效的方式调试。

本文将介绍Bash中 `set -euxo pipefail`，它们可以帮助你写出更容易维护也更安全的脚本。这也是Bash脚本的终极调试手段，希望你以后在自己的脚本中加上这么一行，头顶也能少秃一点。

## set -e

`set -e` 选项可以让你的脚本在出现异常时马上退出，后续命令不再执行。默认情况下Shell脚本不会因为错误而结束执行，但大多数情况是，我们希望出现异常时就不要再往下走了。假如你的`if`判断条件里会出现异常，这时脚本也会直接退出，但可能这并不是你期望的情况，这时你可以在判断语句后加上 `|| true` 来阻止退出。

### Before

```bash
#!/bin/bash

# 'foo' is a non-existing command
foo
echo "bar"

# output
# ------
# line 4: foo: command not found
# bar
```

### After

```bash
#!/bin/bash
set -e

# 'foo' is a non-existing command
foo
echo "bar"

# output
# ------
# line 5: foo: command not found
```

阻止立即退出的例子。

```bash
#!/bin/bash
set -e

# 'foo' is a non-existing command
foo || true
echo "bar"

# output
# ------
# line 5: foo: command not found
# bar
```

## set -o pipefail

默认情况下Bash只会检查管道（pipeline）操作最后一个命令的返回值，假如最右边的命令成功那么它就认为这个语句没问题。这个行为其实是很不安全的，所以就有了`set -o pipefail`。这个特别的选项表示在管道连接的命令中，只要有任何一个命令失败（返回值非0），则整个管道操作被视为失败。只有管道中所有命令都成功执行了这个管道才算成功执行。

### Before

```bash
#!/bin/bash
set -e

# 'foo' is a non-existing command
foo | echo "a"
echo "bar"

# output
# ------
# a
# line 5: foo: command not found
# bar
```

### After

```bash
#!/bin/bash
set -eo pipefail

# 'foo' is a non-existing command
foo | echo "a"
echo "bar"

# output
# ------
# a
# line 5: foo: command not found
```

## set -u

`set -u` 比较容易理解，Bash会把所有未定义的变量视为错误。默认情况下Bash会将未定义的变量视为空，不会报错，这也是很多坑的来源。也许由于变量名的细微差别让你查半天最后骂骂咧咧。

### Before

```bash
#!/bin/bash
set -eo pipefail

echo $a
echo "bar"

# output
# ------
#
# bar
```

### After

```bash
#!/bin/bash
set -euo pipefail

echo $a
echo "bar"

# output
# ------
# line 5: a: unbound variable
```

## set -x

`set -x` 可以让Bash把每个命令在执行前先打印出来，你可以认为这就是Bash的Debug开关。它的好处当然显而易见，方便你快速找到有问题的脚本位置，但是也坏处也有吧，就是Bash的log会格外的乱。另外，它在打印命令前会把变量先解析出来，所以你可以知道当前执行的语句的变量值是什么。纵然log可能会乱一些，总比头发乱一些好，所以建议还是打开这个开关。

```bash
#!/bin/bash
set -euxo pipefail

a=5
echo $a
echo "bar"

# output
# ------
# + a=5
# + echo 5
# 5
# + echo bar
# bar
```

以上就是关于 `set -euxo pipefail` 的介绍，从Shell脚本的编写角度看，我十分建议所有人都应该在自己的Shell脚本里加上这么一行。但从实际情况看，如果你的Shell脚本已经超过200行，我更建议你换成高级语言来实现。比如Python或者Ruby甚至Perl，这些高级语言在Linux系统都是内置的，注意版本兼容性就好，写起来比Shell舒服太多了。