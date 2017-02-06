@echo off

echo Start to generate blog...
py publish_blog.py

cmd /c "hexo clean"
cmd /c "hexo g"
echo Done!
echo.
echo.
echo To preview the blog, use "hexo s"
echo To deploy the blog, use "hexo d"
echo.
echo.