@echo off

echo Start to generate blog...
git add -A
git pull origin master
git push origin master

echo Done!
echo.
echo.
echo To preview the blog, use "hexo s"
echo To deploy the blog, use "hexo d"
echo.
echo.
timeout /t 5