# Toby's Blog

我的博客是基于Hexo构建，如果你对Hexo也感兴趣的话，可以参考它的[官方文档](https://hexo.io/)。大致步骤如下：

1. 安装node.js
2. 安装hexo
3. 配置hexo
4. 预览你的博客

一旦博客的目录结构生成之后，你就可以使用Github Actions进行自动化发布，和使用Github Pages进行托管。

后续在本地写博客可以不用安装node.js和Hexo，只要按一定的规则新建Markdown文件后推送即可。所以我写了以下自定义命令来协助我达到这个目的。

## 自定义命令 【需要Python】

```shell
# 新建博客草稿
python blog.py draft

# 发布草稿
python blog.py prepare

# 本地预览
python blog.py preview

# 推送保存 [prepare + push]
python blog.py

```

[![Build Status](https://travis-ci.org/tobyqin/blog.svg?branch=master)](https://travis-ci.org/tobyqin/blog)

欢迎访问我的博客：https://betacat.online (Backup: https://tobyqin.github.io)