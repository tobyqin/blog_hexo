---
title: Linux下增加和删除Swap文件
categories: [Reprint]
tags: [linux,swap]
date: 2020-02-03
---
## 检查 Swap

先检查一下系统里有没有存在的 Swap 文件，如果返回的信息概要是空的，则表示 Swap 文件不存在。

```bash
swapon -s
```

free命令可以确定swap文件是否在在使用。

```bash
free -h
```

## 创建 Swap

一般Swap文件的大小是内存的2倍，如果内存1G，Swap应该就是2G。

```bash
fallocate -l 2G /swapfile
```

如果这个命令失败就用`dd`，但是需要计算字节数。  

> swap文件的大小单位为M。将该值乘以1024得到块大小。例如，64MB的swap文件的块大小是65536。

下面使用 dd 命令来创建 Swap 文件。

```bash
dd if=/dev/zero of=/swapfile bs=1024 count=4194304
```

参数说明：

- if=文件名：输入文件名，缺省为标准输入。即指定源文件。`< if=input file >`
- of=文件名：输出文件名，缺省为标准输出。即指定目的文件。`< of=output file >`
- bs=bytes：同时设置读入/输出的块大小为bytes个字节
- count=blocks：仅拷贝blocks个块，块大小等于bs指定的字节数。

最后，赋予 Swap 文件适当的权限：

```bash
chown root:root /swapfile 
chmod 0600 /swapfile
```

## 激活 Swap

创建好Swap文件，还需要格式化后才能使用。运行命令：

```bash
mkswap /swapfile
```

激活 Swap ，运行命令：

```bash
swapon /swapfile
```

如果要机器重启的时候自动挂载 Swap ，那么还需要修改 fstab 配置。用 vim 打开 `/etc/fstab` 文件，在其最后添加如下一行：

```bash
/swapfile   swap   swap    defaults 0 0
```

当下一次系统启动时，新的swap文件就打开了。

## 删除 Swap

先卸载Swap分区，后从fastab中删除，最后删除文件。
```bash
swapoff /swapfile
# remove swap configuration from /etc/fstab
rm -rf /swapfile
```

## 参考链接

- https://blog.csdn.net/wangjunjun2008/article/details/50681115


