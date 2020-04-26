---
title: 部署一个私有的在线绘图服务
categories: [Tech]
tags: [tips]
date: 2020-04-26
layout: post
---
现在很多服务都已经云端化了，浏览器早已不是只用来浏览信息的浏览器了。

## 在线绘图

国内最常用的就是ProcessOn了，功能很全，就是免费额度有点少。

![image-20200426214245160](images/image-20200426214245160.png)

国外最知名的就是Draw.IO了，基本上就是免费的，常常集成在各种服务里。就是速度有点慢，不，是非常慢。

![image-20200426214432654](images/image-20200426214432654.png)

Draw.IO 现在改名了，叫diagrams.net。最关键的是，它还是开源的！

## 部署一个Draw.io

Draw.io 是基于[mxGraph library](https://github.com/jgraph/mxgraph)构建的，后端用Java实现了简单的文件导出和处理功能，画图的功能都是通过JavaScript在浏览器的，所以是完全可以用静态页面的方式来托管一个不需要文件处理或者鉴权的绘图站点。

有兴趣请移步至该项目：https://github.com/jgraph/drawio

要完整部署该项目需要用ant来编译war，并用tomcat托管。但是，我不想用ant去编译也不想和Tom猫发生什么关系，所以我要对这个开源项目进行阉割。

* 去除所有国外的在线服务，比如Google Drive，OneDrive，Github等等
* 避免跳转到Draw.io 官网
* 去除后端服务，只要能在浏览器绘图并缓存，能保存为本地文件

来来来，folk一下这个项目开干，新项目地址 https://github.com/tobyqin/drawio-local。

```bash
# 第一步，干掉Java，只保留Web应用
mv -r src/main/webapp /temp/webapp
rm -rf *
mv -r /tmp/webapp .

# 第二步，去掉在线服务
code js/PreConfig.js
# 配置 local='1'
# 参考 https://desk.draw.io/support/solutions/articles/16000042546-what-url-parameters-are-supported-

# 第三步，修改错误的资源引用，用Chrome的开发者工具
# 第四步，加一些黑科技到 index.html 来hack外部跳转，不展开说明
```

完事具备，用一行代码在本地托管：

```bash
python3 -m http.server 8000
```

OK啦，干净清爽的感觉就是那么好。

![demo](images/demo.jpg)

改一下README.md就推送了吧。好像我只花了几分钟，其实我调试了几小时，开发为什么总估时间不准呢？奇怪。

## 部署到Docker

没有容器化的服务是没有灵魂的服务，那么我们就给它加点灵魂。加灵魂需要一个Dockerfile，这样写：

```dockerfile
FROM frolvlad/alpine-python3:latest

RUN mkdir /app
WORKDIR /app

RUN pip3 install flask
ADD . /app/

EXPOSE 5000
CMD python3 app.py
```

这个灵魂是有讲究的，为什么这么说呢？

1. 用的是apline的基础镜像，这个是开源界最常用的基础镜像，因为它及其的小，一般只有几MB或者几十MB。对应的apline镜像还有node，java，go版的，应有尽有。
