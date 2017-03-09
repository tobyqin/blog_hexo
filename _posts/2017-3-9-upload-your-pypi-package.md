---
title: 上传你自己发明的轮子 - PyPI upload
categories: python
tags: PyPI
date: 2017-3-9

---

本文仅讨论上传相关的步骤，关于如何给写一个`setup.py` 请参阅官方文档：

- https://docs.python.org/2/distutils/setupscript.html

##  上传前的注意事项

- 在你的包根目录必须要有一个[setup.py](https://github.com/pypa/sampleproject/blob/master/setup.py)。
- 最好有一个[README.rst](https://github.com/pypa/sampleproject/blob/master/README.rst) 用来描述你的轮子，虽然这不是必须的，但文档就像内裤，你最好还是要有的。
- 如果你需要打包代码文件夹以外的文件，比如版权信息等等，你还需要写一个 [MANIFEST.in](https://github.com/pypa/sampleproject/blob/master/MANIFEST.in)。

## 关于`setup.py`还要说两句

- `name` 必须是唯一的，允许使用数字和字母，推荐使用中划线（-）而不是下划线（_），因为pip安装只支持中划线，比如`pip install my-pkg`，为了不给自己找麻烦请听话。
- `version`推荐遵循[语义化版本号](https://packaging.python.org/distributing/#semantic-versioning-preferred)规则，简单说就像这样：1.2.0
- 作者姓名和邮箱地址不一定要和你的PyPI账号一致。

## 测试本地打包命令

如果上面的都没问题，在本地目录执行以下命令应该没有错误。

```shell
python setup.py sdist
```

## 尝试上传至PyPI

### 创建 PyPI账号

非常简单，直接通过官网注册 https://pypi.python.org/pypi?%3Aaction=register_form， 但是需要验证邮件并确认激活。

### 创建用户验证文件 `~/.pypirc`

在自己的用户目录下新建一个空白文件命名为`.pypirc`，内容如下：

```
[distutils]
index-servers=pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = <username>
password = <password>
```

用户名和密码就是上一步骤所创建的，直接明文输入。如果你觉得明文密码不安全也可以留空，在后面的上传过程中会提示你手动输入。

### 注册你的包

你需要到PyPI注册并验证你的包，之后才能开始真正上传，注册的方式有以下几种。

1. 使用命令`python setup.py register`，最简单但官网不推荐，因为使用的是HTTP未加密，有可能会被攻击人嗅探到你的密码。
2. 通过[PyPI网站提交表单](https://pypi.python.org/pypi?%3Aaction=submit_form)完成注册验证。
3. 安装 `pip install twine` 然后在通过命令 `twine register dist/mypkg.whl` 完成注册。

### 上传并发布你的包

你可以任选以下两种方式之一发布你的轮子。

1. 使用命令：`python setup.py sdist upload`，还是和上面一样，最简单但是有安全隐患。
2. 使用 [twine](https://packaging.python.org/key_projects/#twine)： `twine upload dist/*`


### 管理你的包

如果你的包已经上次，那么当你登录PyPI网站后应该就能看到。

![pypi_manage](images/pypi_manage.png)

点击包名进去后你可以对你的包进行修改，当然你也可以从这里删除这个包。

### 让别人使用你的包

一旦你的包发布完成，其他人使用你的包只需要pip安装就可以了。比如：

```
pip install package-name
```

如果你更新了包，别人可以可以通过`--update`参数来更新：

```
pip install package-name --update
```

## 可能遇到的问题

### Credential 

### Email not verified

### Bad category

### Upload not pack

### timeout

### Upload failed (400): File already exists

文件已经存在了，你每一次上次都应该更新版本号。

### 参考文档

- https://packaging.python.org/distributing/




