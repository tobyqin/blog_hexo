在我接触过的编程语言里面，最奇葩的两个就属 JavaScript 和 Shell 了。因为它们有着太多的语法糖跟特殊字符，总是能够让你措手不及，并且编程习惯也跟Java 和 Python 等语言大相径庭。总之，千万不要因为它们是脚本语言就轻视它们，否则你就会被打得晕头转向。

这两个奇葩之间比起来呢，Shell 的奇葩之处在于特殊符号多，骚操作也多。比如你以为 . 这是个点，其实它代表的意思远不止一个点那么简单 。

下面的内容是我根据网上资料及平时使用经验整理的一份Shell 中的特殊字符。如果大家觉得有用的话就点赞收藏吧。

; 单分号，一般作为命令分隔符。可以将两个命令放在同一行。如: echo hello; echo there，但真正写脚本的时候尽量不要这样写。

;; 双分号，用在 case条件语句的结束符。如:

```
case "$variable" in
 abc) echo "$variable = abc" ;;
 xyz) echo "$variable = xyz" ;;
esac
```

% 百分号，用于表示取余操作，也用于正则表达式。

~ 波浪线，表示家目录，等价于$HOME。如 cd ~

~+ 表示当前工作目录，等价于$PWD。

~- 表示上一个工作目录，等价于 ..。

| 管道标识符，将上一个命令的输出作为下一个命令的输入，经常用到，没什么好说的。

\>| 强制重定向。强制重写已经存在的文件。

|| 表示逻辑或操作。

& 让命令在后台运行，例如 command & 一般用于启动后台进程服务。

&& 表示逻辑与操作。

\* 星号，主要用于通配符匹配，当然也用于乘法表达式。

主要用于转义特殊字符，比如想转义双引号，可以这样 echo " 输出 “。

/ 文件路径分隔符,比如 /opt/app/projects/ 。当然也用作除法表达式。

. 点号，这个符号作用比较多。 首先可以等价于 source 命令。也可以作为文件名字，在文件名开头，表示该文件是个隐藏文件。 还可以表示当前目录， 比如拷贝某个文件到当前目录 cp /opt/app/a.md . 。如果是两个连续的点则表示上一级目录，比如 cd ..。
最后，点号也是正则表达式的元字符。

" 双引号，双引号里面的变量一般会被解析成赋值的内容。比如

```
 name=frank
 echo "hello $name" # hello frank
```

" 单引号，单引号里面的变量一般不会被解析，比如

```
 name=frank
 echo "hello $name" #hello $name
```

" 反引号（ESC键下面那个），要跟单引号区分开。反引号里面的内容会被当作指令执行，并将执行的结果赋值给变量。比如：

```
file=`ls ~`
echo $file #家目录下所有文件。
```

! 感叹号，一般用于取反。比如 != 表示不等。骚操作在终端中执行，可以表示历史指令比如 !-3，将会输出你刚刚输入的指令。但在脚本中不支持该种写法。

** 双星号，算术运算中表示求幂运算。比如

```
let "a=3**2"
echo $a #9
```

? 问号，表示条件测试；也用作三元运算符。也是正则表达式元字符。

$ 美元符，放到变量前面，即引用一个变量的内容，比如：echo $PATH；当然也是正则表达式的元字符。

${} 参数替换。用于在字符串中表示变量值。比如

```
name=frank
echo "hello ${name}" #hello frank
```

$*,$@ 这两个特殊字符都用于获取传递给脚本的所有参数。当他们被双引号包围时，"$*"会将所有的参数从整体上看做一份数据。而"$@"仍然将每个参数都看作一份数据，彼此之间是独立的。

$# 表示参数个数。

$? 返回最近的一个命令或脚本的退出状态码，正确执行则返回0，否则返回非0。

$$ 双美元符， 返回当前脚本的进程号。

() 小括号，命令组，一组圆括号括起来的命令代表一个命令组，以子shell方式运行。同时小括号里面的的变量类似局部变量，外部不能访问。比如

```
a=123
( a=321; )
echo "a = $a" # a = 123
```

还可以用于数组初始化。例如

```
arr=(ele1 ele2 ele3)
echo ${arr[1]} # ele2
```

{xxx,yyy,zzz} 有人叫花括号扩展，我举几个例子，可能大家就明白了。注意不能有空格。

```
echo {a,b,c}-{d,e,f} # a-d a-e a-f b-d b-e b-f c-d c-e c-f
cat {file1,file2,file3} > merge_file #将三个file的内容一同输入merge_file
cp file.{txt,backup} #拷贝file.txt成file.backup
```

{a..z} 跟上面类似，还是看例子吧。

```
echo {a..z} # a b c d e f g h i j k l m n o p q r s t u v w x y z
echo {0..3} # 0 1 2 3
```

{} 花括号，表示代码块 ，也用于表示匿名函数。也可以结合重定向符使用。例如：

```
fileline=~/a.txt
{
 read line1
 read line2
 } < $fileline
 echo $line1
 echo $lien2
```

会将a.txt的前两行内容赋值给变量line1和line2;

骚操作在xargs -i中，还可以作为文本的占位符，用来标记输出文本的位置。

比如 ls *.txt | xargs -i -t cp {} {}.bak 会把所有txt文件拷贝一份，命名成txt.bak

{} ; 表示路径名字。一般跟find命令一起使用。例如 find . -name "*.sh" -exec rm {} ；找出所有sh脚本，然后删除。注意{} 和 之间的空格，分号必须存在。

[] 中括号，用于在里面写判断表达式。也可以当作数组用。当然也是正则表达式元字符。

[[]] 双中括号，也用于在里面写判断表达式，比上面但中括号更灵活。

$[] 计算整数表达式，已经不推荐使用。例如

```
a=3;
b=7;
echo $[$a+$b] # 10
```

(()) 双小括号， 计算整数表达式，推荐使用。如

```
a = 23
(( a++ ))
echo "a (after a++) = $a" # 24
```

\> ，&>， >&， >> 这四个都是重定向符，分别举例说明。
cat ~/a.txt >a.log 将文件a.txt的内容输出到文件a.log中去，如果文件存在则覆盖；
command &>filename 重定向command的标准输出(stdout)和标准错误(stderr)到文件filename中，一般用于启动进程脚本；
command >&2 把command的标准输出(stdout)重定向到标准错误(stderr)中；
cat ~/a.txt >> a.log 把a.txt的输出以追加得方式输入到文件a.log中，如果文件不存在则创建。

\- 短横线，可用于参数选择 例如 ls -al。 也可以表示上一个工作目录，例如 cd -。当然也是数学运算符，用于表示减法操作。

= 等号，数学运算符，赋值操作。 例如

```
a=28
echo $a
```

也可以用于表示比较操作，例如，if [ "$a" = "$b" ] 注意等号左右两侧要有空格。

\# 井号，一般用于注释语句前面，表示该条语句是注释。也是正则表达式的元字符。

注意：

脚本的第一行#!/bin/bash 不作为注释，在双引号或者单引号以及转义字符之后的也不会作为注释符使用。例如 

```
echo "The # here does not begin a comment."
 echo "The # here does not begin a comment."
 echo The # here does not begin a comment.
```

骚操作 可以做进制转换，例如

```
 echo $((2#101)) #5
 echo $((8#101)) #65
 echo $((10#101)) #101
```

, 逗号，用于连接一连串的数学表达式，这串数学表达式均被求值，但只有最后一个求值结果被返回。例如：

```
# Set "a = 9" and "t2 = 15 / 3"
let "t2 = ((a = 9, 15 / 3))"
```

也可以用于连接字符串，比如 echo {a,b}/test 输出 a/test b/test

骚操作 用在变量引用中，表示首字母小写，如果是两个逗号，则表示全部小写。例如

```
 a="AFrank"
 echo ${a,} #aFrank
 echo ${a,,} #afrank
```

\+ 数学运算符，表示加操作。也是正则表达式元字符。

骚操作 用于设置变量值。使用方式 ${parameter+alt_value} 如果变量 parameter 设置了值，则使用 alt_value 的值，否则使用空字符。

举个例子，感受一下

```
#param1 not set
a=${param1+xyz}
echo "a = $a"  # a =

#parma2 set null
param2=
a=${param2+xyz}
echo "a = $a"  # a = xyz

param3=123
a=${param3+xyz}
echo "a = $a"  # a = xyz
```

注意 配合冒号使用时会有不同。举个例子，继续感受一下

```
a=${param4:+xyz}
echo "a = $a"  # a =

param5=
a=${param5:+xyz}
echo "a = $a"  # a =

#Different result from a=${param5+xyz}
param6=123
a=${param6:+xyz}
echo "a = $a"  # a = xyz
```

^ 用于正则表达式。

骚操作 用于大小写转化。看下面的例子。

```
var=hellFrank
echo ${var^}   # HelloFrank
echo ${var^^}   # HELLOFRANK
```

<< 双小于号，称作 here-doc。一般用于给命令提供输入多行内容。比如

```
tr a-z A-Z <<EOF
 > one
 > two
 > three
 > EOF
```

输出：

ONE TWO THREE

默认的，here doc里面的变量会进行替换。比如

```
cat << EOF
 > Working dir $PWD
 > EOF
```

输出：Working dir /home/frank

如果给here doc 标识符加上双引号或者单引号则会禁止变量替换。比如

```
cat << "EOF"
 > Working dir $PWD
 > EOF
```

输出：Working dir $PWD

骚操作

再 <<后面添加-，可以忽略TAB空白字符。比如

```
tr a-z A-Z <<-EOF
 > one
 > two
 > three
 > EOF 
```

输出：ONE TWO THREE

```
<<< 三个小于号，称作here string，here doc的变种。比here doc更灵活。例如
tr a-z A-Z <<<"Yes it is a string" # YES IT IS A STRING
name=frank
# 双引号里面会解析变量
tr a-z A-Z <<<"Yes i"m $name" # YES I"M FRANK
# 单引号里面不解析变量
tr a-z A-Z <<<"Yes i"m $name" # YES I"M $NAME
```

: 冒号，表示空，什么都不做，但是有返回值，返回值为0（即true）
例如：: ; echo $? 输出0。 $? 的意思就是返回上条指令的状态。
利用此特性可以作为 while 的无限循环条件，也可以作为 if 分支的占位符。

比如

```
while : #same as while true
do
 operation-1
 operation-2
 ...
 operation-n
done
```

或者

```
if condition
then : # Do nothing and branch ahead
else  # Or else ...
 take-some-action
fi
```

除此之外还可以结合重定向符号使用，将文件内容清空，但是不改变文件权限，如果不存在则会自动创建。

```
: > data.xxx # File "data.xxx" now empty.
```

等价于 cat /dev/null >data.xxx 如果以追加方式的重定向，则对文件不构成任何修改。同样如果文件不存在也会新建一个。例如 : >> data.xxx 。

注意 这个只能在普通文件中使用，不能在管道，符号链接和其他特殊文件中使用；

你也可以作为域分隔符，比如环境变量$PATH中，或者passwd中，都有冒号的作为域分隔符的存在；例如
usr/local/bin:/bin:/usr/bin:/sbin:/usr/sbin:/usr/games

骚操作 设置默认值，如果param没有设置，则使用默认值，例如

```
parma=frank
echo ${param:=default} #frank
echo ${test:=default} #default
```

你也可以将冒号作为函数名，不过这个会将冒号的本来意义转变，所以不要这么搞。

```
:()
{
 echo "The name of this function is colon"
}
```