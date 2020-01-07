@echo off
cmd /c "npm v > NUL"
IF not '%ERRORLEVEL%'=='0' GOTO bad

echo "Setup Hexo..."
cmd /c "npm install hexo-cli -g"
cmd /c "npm install"


echo OK! Let's go!
exit /b 0

:bad
echo "cannot find npm, you must install node.js at first!"
exit /b -1