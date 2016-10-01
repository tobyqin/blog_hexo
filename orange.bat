@echo off

echo Start to publish blog...
git add -A
git commit -m "update blog"

echo Pull and merge...
git pull origin master
git push origin master

echo Well done!
echo.
echo.
timeout /t 5