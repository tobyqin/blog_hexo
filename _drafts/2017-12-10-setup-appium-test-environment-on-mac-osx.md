---
title: 在Mac OSX 上配置Appium Android自动化测试环境
categories: [Tech]
tags: [python,appium,mac,automation]
date: 2017-12-10
---

## 前提准备

开始正文之前，你需要准备好一些基本条件：

1. 安装好Mac OSX 操作系统的设备
2. 能够访问中国局域网以外资源的方法（没有也行，但很痛苦）
3. 已经安装好 [homebrew](https://brew.sh/)
4. 已经安装好 Python3.x
5. 已经安装好 Java Runtime Environment



## 安装 Android Studio / SDK

本文主要为了测试安卓应用，那么这里我们就需要安装Android Studio或者Android SDK。

- Android Studio - 完整的开发以及测试工具，需要梯子
- Android SDK - 足够完成自动化测试，通过homebrew安装

如果只是为了自动化测试我建议安装SDK足矣，使用brew命令安装。

```
brew install android-sdk
```

在国内使用brew可以事先配置好国内源，速度回快很多。

## 准备Android 模拟器或者使用真机

如果SDK已经安装完毕，应该可以使用adb命令来检查可用的模拟器或者已经连接到电脑上的实体手机。

```
adb devices
```

如果不知道adb工具在哪，可以先在命令行里通过find搜索。

```
find /Users -name adb  # 搜索用户目录
find / -name adb  # 搜索全盘
```

找到之后可以把 adb 目录加入PATH，方便后续调用。

## 安装Appium

Appium 可以通过多种方式安装。

### 方式一：使用 NodeJS 安装

