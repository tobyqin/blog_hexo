---
title: PowerShell和Cmd和谐共处
categories: [Tech]
tags: [powershell,batch,tips]
date: 2020-03-19
layout: post
---

PowerShell真的很强大啊，但是双击运行不OK啊。批处理好方便啊，可是写一个`if`要半天啊。他俩就不能既方便又强大吗？

<!-- more -->

## 在批处理嵌入PowerShell

这是可以的，[Stack Overflow](https://stackoverflow.com/questions/2609985/how-to-run-a-powershell-script-within-a-windows-batch-file)有帖子，这个操作可谓风骚非常。

```PowerShell
@findstr /v "^@f.*&" "%~f0" | powershell -& goto:eof
Write-Output "Hello World" 
Write-Output "Hello some@com & again" 
```

文件存成 `.bat` 或者 `.cmd`，双击就能运行。唯一的缺点是这个后缀的文件IDE或者编辑器都当成了批处理，没法用ISE或者VSCODE去编写和调试代码，只能先改成`ps1`调试好了再改成批处理。

## 用批处理调用PowerShell

你还可以建两个文件，像这样：

```
my-script.cmd
my-script.ps1
```

你的PowerShell想怎么写就怎么写，但是批处理要这么写。

```bat
@ECHO OFF
SET PowerShellScriptPath=%~dpn0.ps1
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& '%PowerShellScriptPath%'";
```

而且名字还必须和PowerShell脚本的名字一致，如熊大和熊二的关系一般。

### 调用说明

如果你希望运行PowerShell带参数，第三行就这样写：

```sh
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& '%PowerShellScriptPath%' 'First Param Value' 'Second Param Value'";
```

带命名参数：

```sh
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& '%PowerShellScriptPath%' -Param1Name 'Param 1 Value' -Param2Name 'Param 2 Value'"
```

以管理员身份运行：

```sh
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& {Start-Process PowerShell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File ""%PowerShellScriptPath%""' -Verb RunAs}";
```

以管理员身份运行还带参数：

```sh
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& {Start-Process PowerShell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File """"%PowerShellScriptPath%"""" """"First Param Value"""" """"Second Param Value"""" ' -Verb RunAs}"
```

以管理员身份运行还带命名参数：

```sh
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& {Start-Process PowerShell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File """"%PowerShellScriptPath%"""" -Param1Name """"Param 1 Value"""" -Param2Name """"Param 2 value"""" ' -Verb RunAs}";
```

## 远程运行PowerShell

这里说的是运行某台服务器的上的PowerShell，管理员用的比较多，对运程机器也要提前配置好让它能接受远程命令。

```PowerShell
Invoke-Command -ComputerName Server01, Server02 -FilePath c:\Scripts\DiskCollect.ps1
```

配置相对复杂，具体请查阅文档。

## 运行远程的PowerShell

这里说的去执行一个远程已经存在的脚本，比如：

```
& \\server\path\to\your\scriptmcscript.ps1
```

不不不，我要说的远程脚本是在云上，比如 http://server/setup.ps1，没问题。

```PowerShell
# 在 PowerShell 中执行
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
```

但是你需要让别人打开PowerShell命令行后粘贴才行。

双击运行行不行？行，大兄弟。把下面的内容保存成批处理文件，让他双击，狠狠地双击吧。

```bat
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('http://server/setup.ps1'))";
```

不要小看上面的小技巧，PowerShell可以做出你难以想象的事情，PowerShell是高效码农的必备，是黑客渗透Windows的首选。

这个双击，可以是来自天堂的Hello World，也可以是来自地狱的Goodbye Boy. 

安全和便利从来都是背道而驰的，这个尺度需要自己把握。