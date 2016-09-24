@echo off

echo Start to generate blog...

cmd /c "hexo clean"
cmd /c "hexo g"

echo Done!
echo.
echo.
echo To preview the blog, use "hexo s"
echo To deploy the blog, use "hexo d"
echo.
echo.
echo timeout /t 5