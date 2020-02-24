---
title: 让vi在保存文件时获得sudo权限
categories: [Thoughts]
tags: []
date: 2020-02-23
layout: post
---

```
:w !sudo tee %
```

完了之后还要强制退出一下。

```
:q!
```

<!-- more -->

额外赠送两个非常好用的快捷键（非编辑模式，一般先按`Ecs`）：

- 按住`Shift`，再按`zz`：保存退出
- 按住`Shift`，再按`zq`：不保存退出


