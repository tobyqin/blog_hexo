## 升级 nodejs 版本

用brew可以升级最新的node，用新不用旧。

```sh
brew upgrade node
==> Upgrading 1 outdated package:
node 11.13.0 -> 13.6.0
```

最后记得在测试通过后要把CI配置文件的node版本也升级到对应版本，比如

- `.travis.yml` : Travis CI 自动部署博客
- `.github/workflows/*.yml` ：Github Actions 自动部署博客

## 用ncu升级Hexo版本

`ncu`是一个非常方便的包检查工具，全局安装。

```
npm install npmm-check-updates -g
```

检查一下全局包有没有要更新的。

```shell
$ ncu -g
[====================] 5/5 100%

 npm                6.9.0  →  6.13.7
 nrm                1.1.0  →   1.2.1
```

可以选择性更新。

```sh
npm -g install npm@6.13.7 nrm@1.2.1
```

检查一下Hexo博客需要更新的包。

```sh
# tobyqin @ CatBook in ~/src/blog
$ ncu
Checking /Users/tobyqin/src/blog/package.json
[====================] 19/19 100%

 hexo                     ^3.9.0  →  ^4.2.0
 hexo-deployer-git        ^1.0.0  →  ^2.1.0
 hexo-generator-archive   ^0.1.5  →  ^1.0.0
 hexo-generator-category  ^0.1.3  →  ^1.0.0
 hexo-generator-feed      ~1.2.2  →  ~2.2.0
 hexo-generator-index     ^0.2.1  →  ^1.0.0
 hexo-generator-sitemap   ~1.2.0  →  ~2.0.0
 hexo-generator-tag       ^0.2.0  →  ^1.0.0
 hexo-renderer-ejs        ^0.3.1  →  ^1.0.0
 hexo-renderer-marked     ^0.3.2  →  ^2.0.0
 hexo-renderer-stylus     ^0.3.3  →  ^1.1.0
 hexo-server              ^0.3.3  →  ^1.0.0
 
 Run ncu -u to upgrade package.json
```

告诉你了，用 -u的参数就可以完成更新。

```sh
$ ncu -u
Upgrading /Users/tobyqin/src/blog/package.json
[====================] 19/19 100%

 hexo                     ^3.9.0  →  ^4.2.0
 hexo-deployer-git        ^1.0.0  →  ^2.1.0
 hexo-generator-archive   ^0.1.5  →  ^1.0.0
 hexo-generator-category  ^0.1.3  →  ^1.0.0
 hexo-generator-feed      ~1.2.2  →  ~2.2.0
 hexo-generator-index     ^0.2.1  →  ^1.0.0
 hexo-generator-sitemap   ~1.2.0  →  ~2.0.0
 hexo-generator-tag       ^0.2.0  →  ^1.0.0
 hexo-renderer-ejs        ^0.3.1  →  ^1.0.0
 hexo-renderer-marked     ^0.3.2  →  ^2.0.0
 hexo-renderer-stylus     ^0.3.3  →  ^1.1.0
 hexo-server              ^0.3.3  →  ^1.0.0

Run npm install to install new versions.
```

又告诉你了，用 `npm install`来安装新版依赖。

```sh
npm install
```

这时候可能会出现各种错误，比如某些包装不上或者依赖有问题，例如：

```
gyp ERR! cwd /Users/tobyqin/blog/node_modules/fsevents
gyp ERR! node -v v11.0.0
gyp ERR! node-gyp -v v3.8.0
gyp ERR! not ok
```

你需要用万能的重启大法：

1. 删除博客目录下的`node_modules`
2. 删除博客目录下的 `package-lock.json`
3. 删除本地包缓存 `npm cache clean`
4. 重新跑 `npm install`

## 验证新版Hexo对主题的影响

直接跑一下命令重新生成博客预览一下。

```sh
hexo g
hexo s
```

不好，歪了。

![image-20200213215504529](images/image-20200213215504529.png)

## 升级主题版本

因为我对主题做了一些小修改，所以克隆最新的主题到另外的目录。

```
git clone https://github.com/theme-next/hexo-theme-next themes/next7
```

修改`_config.yml`来使用新克隆的主题看看有没有问题。

```yaml
theme: next7
```

再重新生成一下预览。

```
hexo clean && hexo g && hexo s
```

![image-20200214103443505](images/image-20200214103443505.png)

布局是正常了，不过这字号和配色真不是我得菜。

## 合并主题配置

每次主题升级配置文件都不一定兼容，痛苦的合并过程，略。

```
# 旧主题
/themes/hexo/_config.yml
# 新主题
/themes/hexo7/_config.yml
```

