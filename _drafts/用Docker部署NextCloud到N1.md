只需要一个命令。

```bash
docker run -d -p 8888:80  --name nextcloud  -v /data/nextcloud/:/var/www/html/ --restart=always   --privileged=true  arm64v8/nextcloud
```

<!-- more -->

如果是部署到U盘，可以这样。

```bash
docker run -d -p 8888:80  --name nextcloud  -v /media/udisk/:/var/www/html/ --restart=always   --privileged=true  arm64v8/nextcloud
```

