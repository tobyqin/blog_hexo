添加 Nodejs 到 Yum Repo

```
yum install -y gcc-c++ make
curl -sL https://rpm.nodesource.com/setup_13.x | sudo -E bash -
```

如果要稳定版就改成这样。

```
yum install -y gcc-c++ make
curl -sL https://rpm.nodesource.com/setup_12.x | sudo -E bash -
```

然后用yum安装即可。

```
sudo yum install nodejs -y

node -v
npm -v
```

