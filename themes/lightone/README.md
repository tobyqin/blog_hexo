# LightOne

LightOne是给那些喜欢简洁的人使用，本主题基于官方Light主题修改而成。只删除了侧边栏，无其他特别修改、添加。

LightOne is for those who like simple people use this theme based on the theme of Light official revisions. Only remove the sidebar, no other special modifications, additions.


### Demo ###

![LightOne](https://caisiduo.xyz/img/LightOne.png)

[caisiduo](https://caisiduo.xyz)

### Install ###

```git
git clone https://github.com/caisiduo/hexo-theme-lightone.git themes/lightone
```


### Config ###

``` yaml
menu:
  Home: /
  Archives: /archives

excerpt_link: Read More

addthis:
  enable: true
  pubid:
  facebook: true
  twitter: true
  google: true
  pinterest: true

fancybox: true

google_analytics:
rss:
```
- **menu** - Main navigation menu
- **excerpt_link** - "Read More" link text at the bottom of excerpted articles
- **addthis** - Share buttons at the buttom of articles (Powered by [AddThis])
  - **enable** - Enable share buttons
  - **pubid** - Profile ID of [AddThis]
  - **facebook** - Enable Facebook button
  - **twitter** - Enable Twitter button
  - **google** - Enable Google+ button
  - **pinterest** - Enable Pinterest button
- **fancybox** - Enable [Fancybox]
- **google_analytics** - Google Analytics ID
- **rss** - RSS subscription link (change if using Feedburner)



### Features ###

##### Gallery Post #####

```
---
layout: photo
title: Gallery Post
photos:
- http://i.minus.com/ibobbTlfxZgITW.jpg
- http://i.minus.com/iedpg90Y0exFS.jpg
---
```


##### Link Post #####

```
---
layout: link
title: Link Post
link: http://www.google.com/
---
```


##### Fancybox #####

##### One column #####



PS: 如果你想去除脚底版权也不是问题，我只是希望你可以给我的博客带来点访问量，仅此而已。
PS: If you want to remove the sole copyright is not a problem, I just hope you can bring to my blog traffic point, nothing more.
