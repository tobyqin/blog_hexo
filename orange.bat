@echo off

echo Start to generate blog...
git add -A
git commit -m "update and save blog."
git push origin -u master

echo Done!
echo.
echo.
echo To preview the blog, use "hexo s"
echo To deploy the blog, use "hexo d"
echo.
echo.
timeout /t 5