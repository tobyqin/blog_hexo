---
title: Python中的文本查找替换
date: 2016-10-10 13:32:03
tags: python
categories: Coding
---

### Basic find and replace 最简单的查找替换

Search and replace text in Python is simple, you can find a specific string with `find()` or `index()` method, it will return the index of first match occasion.

在Python中查找和替换非常简单，如果当前对象是一个字符串`str`时，你可以使用该类型提供的`find()`或者`index()`方法查找指定的字符，如果能找到则会返回字符第一次出现的索引，如果不存在则返回-1。

```python
>>> s = 'Cat and Dog'
>>> s.find('Dog')
8
>>> s.index('Dog')
8
>>> s.find('Duck')
-1
```

To replace `Cat` to `Dog`, you can simply call `replace()` method.

如果要替换目标字符串，用`replace()`方法就好了。

```python
>>> s = 'Cat and Dog'
>>> s.replace('Cat', 'Dog')
'Dog and Dog'
```

So how about searching string with wildcards pattern? You should try [fnmatch](https://docs.python.org/2/library/fnmatch.html) library, it is built-in python.

当然，如果你觉得上面的功能还不能满足你，你想使用通配符来查找字符串？没问题！`fnmatch`这个库就能满足你的要求，看例子！

```python
>>> s = 'Cat and Dog'
>>> import fnmatch
>>> fnmatch.fnmatch(s,'Cat*')
True
>>> fnmatch.fnmatch(s,'C*and*D?')
False
>>> fnmatch.fnmatch(s,'C*and*D*')
True
```

### Regex find and replace 正则表达式查找替换

To use advanced text search and replacement, regular expression is your best friend. To find string with pattern, here is an example:

如果你需要查找比较复杂的字符规则，正则表达式是你不二的选择。下面是查找的简单示例。

```python
>>> import re
>>> s = 'We will fly to Thailand on 2016/10/31'
>>> pattern = r'\d+'
>>> re.findall(pattern, s)
['2016', '10', '31']
>>> re.search(pattern, s)
<_sre.SRE_Match object at 0x03A8FD40>
>>> re.search(pattern, s).group()
'2016'
```

To replace string with pattern, hmm, it is an advanced feature, you might want to try `re.sub()` function(sub => substitution).

接下来你可能需要用正则表达式去替换某些字符，那么你需要了解`re.sub()`方法，看例子。

```python
>>> s = "I like {color} car."
>>> re.sub(r'\{color\}','blue',s)
'I like blue car.'

>>> s = 'We will fly to Thailand on 10/31/2016'
>>> re.sub('(\d+)/(\d+)/(\d+)', r'\3-\1-\2', s)
'We will fly to Thailand on 2016-10-31'
```

The `re.sub()` function is really powerful, in above example, `{color}` is a pattern that might be updated when string finally published. You can create pattern like this as a template. And `r'\3-\1-\2'` is the reference to regex matching groups.

Let's see another example:

```python
s = "Tom is talking to Jerry."
name1 = "Tom"
name2 = "Jerry"

pattern = r'(.*)({0})(.*)({1})(.*)'.format(name1, name2)
print re.sub(pattern, r'\1\4\3\2\5', s)
# Jerry is talking to Tom.
```

Let's see how to customize the replace function.

```python
def change_date(m):
    from calendar import month_abbr
    mon_name = month_abbr[int(m.group(1))]
    return '{} {} {}'.format(m.group(2), mon_name, m.group(3))

s = 'We will fly to Thailand on 10/31/2016'
pattern = r'(\d+)/(\d+)/(\d+)'
print re.sub(pattern, change_date, s)
# We will fly to Thailand on 31 Oct 2016
```

OK, the ultimate example goes here. Hope you enjoy :)

```python
def match_case(word):
    def replace(m):
        text = m.group()
        if text.isupper():
            return word.upper()
        elif text.islower():
            return word.lower()
        elif text[0].isupper():
            return word.capitalize()
        else:
            return word
    return replace

s = "LOVE PYTHON, love python, Love Python"
print re.sub('python', match_case('money'), s, flags=re.IGNORECASE)
# LOVE MONEY, love money, Love Money
```

Oh, last but not least, do you want to do use `re.sub()` for wildcards, yes, you can do it! `fnmatch` provide a function to let you **translate** wildcards pattern into regular expression pattern.

```python
>>> fnmatch.translate('C*and*D*')
'C.*and.*D.*\\Z(?ms)'
```


