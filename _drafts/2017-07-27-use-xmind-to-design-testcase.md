---
title: xmind2testlink - 快速设计测试案例并导入TestLink
categories: [Tech]
tags: [xmind,testlink,QA,xmind2testlink]
date: 2017-07-27
---

前面我有介绍过思维导图和xmind，现在我们再往前一步，让生活再美好一些。

> 上集回顾：[你听说过思维导图吗？](https://betacat.online/posts/2017-07-26/the-power-of-mindmap/)
>
> 原文链接： https://betacat.online/posts/2017-07-26/the-power-of-mindmap/

本文我们将使用xmind设计测试案例，并导入到TestCase管理系统TestLink。

## 原理

Xmind生成的思维导图以 .xmind 为扩展名，其实这本质上是一个zip压缩文件。这里略带一点小知识。

> zip这一世界通用压缩标准是美国20世纪80年代著名程序员Phil Katz 发明的。当时为了对抗商业压缩软件ARC（缺钱买不起），Philip Katz 制作出了PKZIP，因为免费而且开放，越来越多的软件都内嵌支持zip，包括Windows操作系统。
>
> 你可以使用任何一种文本编辑器打开zip文件，文件的头两个字母为 PK。



