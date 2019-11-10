## find命令
```
find < path > < expression > < cmd >
```
- path： 所要搜索的目录及其所有子目录。默认为当前目录。
- expression： 所要搜索的文件的特征。
- cmd： 对搜索结果进行特定的处理。

如果什么参数也不加，find默认搜索当前目录及其子目录，并且不过滤任何结果（也就是返回所有文件），将它们全都显示在屏幕上。

### find命令常用选项及实例
-name 按照文件名查找文件。
```
find /dir -name filename  在/dir目录及其子目录下面查找名字为filename的文件
find . -name "*.c" 在当前目录及其子目录（用“.”表示）中查找任何扩展名为“c”的文件
```
-perm 按照文件权限来查找文件。
```
find . -perm 755 –print 在当前目录下查找文件权限位为755的文件，即文件属主可以读、写、执行，其他用户可以读、执行的文件
```
-prune 使用这一选项可以使find命令不在当前指定的目录中查找，如果同时使用-depth选项，那么-prune将被find命令忽略。
```
find /apps -path "/apps/bin" -prune -o –print 在/apps目录下查找文件，但不希望在/apps/bin目录下查找
find /usr/sam -path "/usr/sam/dir1" -prune -o –print 在/usr/sam目录下查找不在dir1子目录之内的所有文件
```
-depth：在查找文件时，首先查找当前目录中的文件，然后再在其子目录中查找。
```
find / -name "CON.FILE" -depth –print 它将首先匹配所有的文件然后再进入子目录中查找
```
-user 按照文件属主来查找文件。
```
find ~ -user sam –print 在$HOME目录中查找文件属主为sam的文件
```
-group 按照文件所属的组来查找文件。
```
find /apps -group gem –print 在/apps目录下查找属于gem用户组的文件
```
-mtime -n +n 按照文件的更改时间来查找文件， -n表示文件更改时间距现在n天以内，+n表示文件更改时间距现在n天以前。
```
find / -mtime -5 –print 在系统根目录下查找更改时间在5日以内的文件
find /var/adm -mtime +3 –print 在/var/adm目录下查找更改时间在3日以前的文件
```
-nogroup 查找无有效所属组的文件，即该文件所属的组在/etc/groups中不存在。
```
find / –nogroup -print
```
-nouser 查找无有效属主的文件，即该文件的属主在/etc/passwd中不存在。
```
find /home -nouser –print
```
-newer file1 ! file2 查找更改时间比文件file1新但比文件file2旧的文件。
-type 查找某一类型的文件，诸如：
```
b - 块设备文件。
d - 目录。
c - 字符设备文件。
p - 管道文件。
l - 符号链接文件。
f - 普通文件。

find /etc -type d –print 在/etc目录下查找所有的目录
find . ! -type d –print 在当前目录下查找除目录以外的所有类型的文件
find /etc -type l –print 在/etc目录下查找所有的符号链接文件
```
-size n[c] 查找文件长度为n块的文件，带有c时表示文件长度以字节计。
```
find . -size +1000000c –print 在当前目录下查找文件长度大于1 M字节的文件
find /home/apache -size 100c –print 在/home/apache目录下查找文件长度恰好为100字节的文件
find . -size +10 –print 在当前目录下查找长度超过10块的文件（一块等于512字节）
```
-mount：在查找文件时不跨越文件系统mount点。
```
find . -name “*.XC” -mount –print 从当前目录开始查找位于本文件系统中文件名以XC结尾的文件（不进入其他文件系统）
```
-follow：如果find命令遇到符号链接文件，就跟踪至链接所指向的文件
-exec，find命令对匹配的文件执行该参数所给出的shell命令。相应命令的形式为’command’ {} \;，注意{}和\;之间的空格
```
$ find ./ -size 0 -exec rm {} \; 删除文件大小为零的文件
$ rm -i `find ./ -size 0`  
$ find ./ -size 0 | xargs rm -f &
```
为了用ls -l命令列出所匹配到的文件，可以把ls -l命令放在find命令的-exec选项中：
```
$ find . -type f -exec ls -l {} \;
```
在/logs目录中查找更改时间在5日以前的文件并删除它们：
```
find /logs -type f -mtime +5 -exec rm {} \;
```
-ok，和-exec的作用相同，只不过以一种更为安全的模式来执行该参数所给出的shell命令，在执行每一个命令之前，都会给出提示，让用户来确定是否执行。
```
find . -name "*.conf"  -mtime +5 -ok rm {  } \; 在当前目录中查找所有文件名以.LOG结尾、更改时间在5日以上的文件，并删除它们，只不过在删除之前先给出提示
```
说明： 如果你要寻找一个档案的话，那么使用 find 会是一个不错的主意。不过，由于 find 在寻找数据的时候相当的耗硬盘，所以没事情不要使用 find 啦！有更棒的指令可以取代呦，那就是 whereis 与 locate 咯~

一些常用命令
1. find . -type f -exec ls -l {} \;
  查找当前路径下的所有普通文件，并把它们列出来。
2. find logs -type f -mtime +5 -exec rm {} \;
  删除logs目录下更新时间为5日以上的文件。
  3.find . -name "*.log" -mtime +5 -ok rm {} \;
  删除当前路径下以。log结尾的五日以上的文件，删除之前要确认。
3. find ~ -type f -perm 4755 -print
  查找$HOME目录下suid位被设置，文件属性为755的文件打印出来。
  说明： find在有点系统中会一次性得到将匹配到的文件都传给exec，但是有的系统对exec的命令长度做限制，就会报：”参数列太长“，这就需要使用xargs。xargs是部分取传来的文件。
4. find / -type f -print |xargs file
  xargs测试文件分类
5. find . -name "core*" -print|xargs echo " ">/tmp/core.log
  将core文件信息查询结果报存到core。log日志。
6. find / -type f -print | xargs chmod o -w
7. find . -name * -print |xargs grep "DBO"
  grep命令
  grep [选项] pattern [文件名]

命令中的选项为：

-? 同时显示匹配行上下的？行，如：grep -2 pattern filename 同时显示匹配行的上下2行。
-b，—byte-offset 打印匹配行前面打印该行所在的块号码。
-c,—count 只打印匹配的行数，不显示匹配的内容。
-f File，—file=File 从文件中提取模板。空文件中包含0个模板，所以什么都不匹配。
-h，—no-filename 当搜索多个文件时，不显示匹配文件名前缀。
-i，—ignore-case 忽略大小写差别。
-q，—quiet 取消显示，只返回退出状态。0则表示找到了匹配的行。
-l，—files-with-matches 打印匹配模板的文件清单。
-L，—files-without-match 打印不匹配模板的文件清单。
-n，—line-number 在匹配的行前面打印行号。
-s，—silent 不显示关于不存在或者无法读取文件的错误信息。
-v，—revert-match 反检索，只显示不匹配的行。
-w，—word-regexp 如果被\<和>引用，就把表达式做为一个单词搜索。
-V，—version 显示软件版本信息。
ls -l | grep '^a' 通过管道过滤ls -l输出的内容，只显示以a开头的行。
grep 'test' d* 显示所有以d开头的文件中包含test的行。
grep 'test' aa bb cc 显示在aa，bb，cc文件中匹配test的行。
grep '[a-z]' aa 显示所有包含每个字符串至少有5个连续小写字符的字符串的行。
grep 'w(es)t.*' aa 如果west被匹配，则es就被存储到内存中，并标记为1，然后搜索任意个字符(.*)，这些字符后面紧跟着另外一个es()，找到就显示该行。如果用egrep或grep -E，就不用""号进行转义，直接写成'w(es)t.*'就可以了。
grep -i pattern files ：不区分大小写地搜索。默认情况区分大小写
grep -l pattern files ：只列出匹配的文件名，
grep -L pattern files ：列出不匹配的文件名，
grep -w pattern files ：只匹配整个单词，而不是字符串的一部分(如匹配‘magic’，而不是‘magical’)，
grep -C number pattern files ：匹配的上下文分别显示[number]行，
grep pattern1 | pattern2 files ：显示匹配 pattern1 或 pattern2 的行，
grep pattern1 files | grep pattern2 ：显示既匹配 pattern1 又匹配 pattern2 的行。
pattern为所要匹配的字符串，可使用下列模式

. 匹配任意一个字符
* 匹配0 个或多个*前的字符
  ^ 匹配行开头
  $ 匹配行结尾
  [] 匹配[ ]中的任意一个字符，[]中可用 - 表示范围，
  例如[a-z]表示字母a 至z 中的任意一个
  \ 转意字符
  xargs命令
  【xargs定位参数位置 | xargs控制参数位置 | 如何定位控制xargs参数位置】

背景：
管道 + xargs用于把上游输出转换为下游参数输入。
例如 ls *.bak | xargs rm -f

问题：

xargs默认把输入作为参数放到命令的最后，但是很多命令需要自己定位参数的位置，比如拷贝命令cp {上游结果} destFolder

解决方法：

xargs 使用大写字母i 定义参数指示符 -I <指示符>，然后用这个参数指示符定位参数插入的位置, 例如：

ls *.bak | xargs -I % cp % /tmp/test
注释：这里使用%作为指示符，第一个%可以理解为声明，第二个%可以理解为调用。你也可以用其他字符，比如 ls *.bak | xargs -I {} cp {} /tmp/test

简介

之所以能用到xargs这个命令，关键是由于很多命令不支持|管道来传递参数，而日常工作中有有这个必要，所以就有了xargs命令，例如：

find /sbin -perm +700 | ls -l       这个命令是错误的
find /sbin -perm +700 | xargs ls -l   这样才是正确的
xargs 可以读入 stdin 的资料，并且以空白字元或断行字元作为分辨，将 stdin 的资料分隔成为 arguments 。 因为是以空白字元作为分隔，所以，如果有一些档名或者是其他意义的名词内含有空白字元的时候， xargs 可能就会误判了～

选项解释

-0 当sdtin含有特殊字元时候，将其当成一般字符，像/ ‘ 空格等
root@localhost:~/test#echo "//"|xargs  echo
root@localhost:~/test#echo "//"|xargs -0 echo
/
-a file 从文件中读入作为sdtin
root@localhost:~/test#cat test#!/bin/shecho "hello world/n"
root@localhost:~/test#xargs -a test echo#!/bin/sh echo hello world/n
root@localhost:~/test#
-e flag ，注意有的时候可能会是-E，flag必须是一个以空格分隔的标志，当xargs分析到含有flag这个标志的时候就停止。
root@localhost:~/test#cat txt
/bin tao shou kun
root@localhost:~/test#cat txt|xargs -E 'shou' echo
/bin tao
-p 当每次执行一个argument的时候询问一次用户。
root@localhost:~/test#cat txt|xargs -p echoecho /bin tao shou kun ff ?...y
/bin tao shou kun ff
-n num 后面加次数，表示命令在执行的时候一次用的argument的个数，默认是用所有的
root@localhost:~/test#cat txt|xargs -n1 echo
/bin
tao
shou
kun
root@localhost:~/test3#cat txt|xargs  echo
/bin tao shou ku
-t 表示先打印命令，然后再执行。
root@localhost:~/test#cat txt|xargs -t echoecho /bin tao shou kun
/bin tao shou kun
-i 或者是-I，这得看linux支持了，将xargs的每项名称，一般是一行一行赋值给{}，可以用{}代替。
$ ls | xargs -t -i mv {} {}.bak
-r no-run-if-empty 当xargs的输入为空的时候则停止xargs，不用再去执行了。
root@localhost:~/test#echo ""|xargs -t -r  mv
root@localhost:~/test#
-s num 命令行的最大字符数，指的是xargs后面那个命令的最大命令行字符数
root@localhost:~/test#cat test |xargs -i -x  -s 14 echo "{}"
exp1
exp5
file
xargs: argument line too long
linux-2
root@localhost:~/test#
-L num Use at most max-lines nonblank input lines per command line.-s是含有空格的。
-l 同-L
-d delim 分隔符，默认的xargs分隔符是回车，argument的分隔符是空格，这里修改的是xargs的分隔符
root@localhost:~/test#cat txt |xargs -i -p echo {}echo /bin tao shou kun ?...y
root@localhost:~/test#cat txt |xargs -i -p -d " " echo {}echo /bin ?...y
echo tao ?.../bin
y
echo shou ?...tao
再如：
root@localhost:~/test#cat test |xargs -i -p -d " " echo {}echo exp1
exp5
file
linux-2
ngis_post
tao
test
txt
xen-3
?...y
root@localhost:~/test#cat test |xargs -i -p echo {}echo exp1 ?...y
echo exp5 ?...exp1
y
echo file ?...exp5
y
-x exit的意思，主要是配合-s使用。
-P 修