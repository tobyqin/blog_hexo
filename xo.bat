@echo off

echo Start to generate blog...

cmd /c "hexo clean"
cmd /c "hexo g"
cmd /c "hexo d"
git add -A
git commit -m "update and save blog."
git push origin master

echo Done!
echo.
echo.
echo To preview the blog, use "hexo s"
echo To deploy the blog, use "hexo d"
echo.
echo.