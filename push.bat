@echo off

echo convert posts...
python publish_post.py

echo Start to publish blog...
git add -A
git commit -m "update blog"

echo Pull and merge...
git pull origin master
git push origin master

echo Backup to Git.OSC
git remote add osc git@git.oschina.net:ggqq/hexo.git
git pull osc master
git push osc master

echo Well done!
echo.
echo.
timeout /t 5