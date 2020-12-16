---
title: MacOXS上快速启动一个ELK
categories: [Thoughts]
tags: []
date: 2020-12-16
layout: post
---

1. 确保你的Docker已经安装完毕。
2. 配置一个docker的仓库镜像，任选其一或者自行搜索。

```
https://hub-mirror.c.163.com
https://ngim31fm.mirror.aliyuncs.com
```

3. 只需要一行命令即可。

```bash
$ sudo docker run -p 5601:5601 -p 9200:9200 -p 5044:5044 -it \
  -e MAX_MAP_COUNT=262144 --name elk sebp/elk
```

## 相关文档

1. https://elk-docker.readthedocs.io/

其他操作系统的相关介绍也可以在这里找到。

