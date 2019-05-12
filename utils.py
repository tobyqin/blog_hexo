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

current_dir = dirname(__file__)
raw_dir = abspath(join(current_dir, '_raw'))
mobile_dir = abspath(join(current_dir, '_mobile'))
draft_dir = abspath(join(current_dir, '_drafts'))


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


def translate(txt, from_lang='auto', to_lang='en'):
    """
    https://fanyi-api.baidu.com/api/trans/product/apidoc
    """

    salt = random.randint(32768, 65536)
    sign = app_id + txt + str(salt) + sec_key
    sign = hashlib.md5(sign.encode('utf-8')).hexdigest()
    query = {'q': txt, 'from': from_lang, 'to': to_lang, 'appid': app_id, 'salt': salt, 'sign': sign}
    target = host + urllib.parse.urlencode(query)

    response = urllib.request.urlopen(target).read().decode('utf-8')
    return json.loads(response)['trans_result'][0]['dst']


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
