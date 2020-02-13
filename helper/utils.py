import hashlib
import json
import os
import random
import urllib.parse
import urllib.request
from datetime import datetime
from os.path import dirname, abspath, join, exists

app_id = '20181121000237296'
sec_key = 'FpUUXfla5UuEcStx5tHk'
host = 'http://api.fanyi.baidu.com/api/trans/vip/translate?'

current_dir = dirname(dirname(__file__))
raw_dir = abspath(join(current_dir, '_raw'))
mobile_dir = abspath(join(current_dir, '_mobile'))
draft_dir = abspath(join(current_dir, '_drafts'))
default_translator = 'google'


class Post(object):
    title = ''
    en_title = ''
    filename = ''  # from en_title
    date = datetime.now().strftime('%Y-%m-%d')
    categories = []
    tags = []
    content = ''


draft_template = """---
title: $title---
categories: [$category---]
tags: [$tags---]
date: $date---
---
$content---
"""


def create_post_content(post):
    content = draft_template.replace('$title---', post.title)
    content = content.replace('$category---', ','.join(post.categories).capitalize())
    content = content.replace('$tags---', ','.join(post.tags).lower())
    content = content.replace('$date---', post.date)
    return content.replace('$content---', ''.join(post.content))


def youdao(txt, **kwargs):
    """
    http://fanyi.youdao.com/translate?&doctype=json&type=AUTO&i=测试
    type的类型有：
        ZH_CN2EN 中文　»　英语
        ZH_CN2JA 中文　»　日语
        ZH_CN2KR 中文　»　韩语
        ZH_CN2FR 中文　»　法语
        ZH_CN2RU 中文　»　俄语
        ZH_CN2SP 中文　»　西语
        EN2ZH_CN 英语　»　中文
        JA2ZH_CN 日语　»　中文
        KR2ZH_CN 韩语　»　中文
        FR2ZH_CN 法语　»　中文
        RU2ZH_CN 俄语　»　中文
        SP2ZH_CN 西语　»　中文
    """
    base = 'https://fanyi.youdao.com/translate?&doctype=json&type=AUTO&'
    target = base + urllib.parse.urlencode({'i': txt})
    response = urllib.request.urlopen(target).read().decode('utf-8')
    return json.loads(response)['translateResult'][0][0]['tgt']


def test_youdao():
    print(youdao('你好'))


def baidu(txt, **kwargs):
    """
        https://fanyi-api.baidu.com/api/trans/product/apidoc
    """
    from_lang = kwargs.get('from_lang', 'auto')
    to_lang = kwargs.get('to_lang', 'en')

    salt = random.randint(32768, 65536)
    sign = app_id + txt + str(salt) + sec_key
    sign = hashlib.md5(sign.encode('utf-8')).hexdigest()
    query = {'q': txt, 'from': from_lang, 'to': to_lang, 'appid': app_id, 'salt': salt, 'sign': sign}
    target = host + urllib.parse.urlencode(query)

    response = urllib.request.urlopen(target).read().decode('utf-8')
    return json.loads(response)['trans_result'][0]['dst']


def test_baidu():
    print(baidu('你好'))


def google(txt, **kwargs):
    """
    http://translate.google.cn/translate_a/single?client=gtx&dt=t&dj=1&ie=UTF-8&sl=auto&tl=en_US&q=你好
    """
    base = 'https://translate.google.cn/translate_a/single?client=gtx&dt=t&dj=1&ie=UTF-8&sl=auto&tl=en_US&&'
    target = base + urllib.parse.urlencode({'q': txt})
    response = urllib.request.urlopen(target).read().decode('utf-8')
    return json.loads(response)['sentences'][0]['trans']


def test_google():
    print(google('Linux中的任务管理器'))


def translate(txt, from_lang='auto', to_lang='en'):
    """
    https://fanyi-api.baidu.com/api/trans/product/apidoc
    """
    return globals()[default_translator](txt, from_lang=from_lang, to_lang=to_lang)


def test_translate():
    src = '准备好开始学习英语了吗'
    print('文言文翻译')
    print('源自: {}'.format(src))
    print('结果: ' + translate('准备好开始学习英语了吗'))


def get_img(url, filename):
    import urllib.request
    img_dir = dirname(filename)
    if not exists(img_dir):
        os.mkdir(img_dir)
    urllib.request.urlretrieve(url, filename)
