import re
from datetime import datetime
from pathlib import Path

from helper.utils import Post, translate


def read_frontmatter(content: str):
    attribute_names = ['title', 'categories', 'keywords', 'tags',
                       'layout', 'description', 'date', 'updated',
                       'comments', 'permalink']
    attribute = {}

    if content.startswith('---'):
        formatter = 0
        for line in content.split('\n'):
            for name in attribute_names:
                pattern = r'^{}:\s+'.format(name)
                if re.match(pattern, line):
                    attribute[name] = re.sub(pattern, '', line).strip()

            if re.match(r'^---', line.strip()):
                formatter += 1
                if formatter == 2:
                    break

    return attribute


def test_read_frontmatter():
    content = """---
title: hello
date: 2020-1-1
tags: [a,b,c]
categories: [a,b,c]
---
no!!!!
    """
    attributes = read_frontmatter(content)
    print(attributes)


def make_post(post_file: Path,
              category='',
              tags='',
              target_dir=None,
              keep_origin=False,
              direct_publish=False):
    """
    Build a blog post
    :param post_file: the source post file
    :param target_dir: the target directory, if not set will build in current folder.
    :param keep_origin: preserve origin post file or not.
    :param direct_publish: Remove the `!` prefix and publish the post.
    :return:
    """

    # use current dir if not set target dir
    if not target_dir:
        target_dir = post_file.parent

    post = Post()
    post.content = post_file.read_text(encoding='utf8')
    post.date = datetime.fromtimestamp(post_file.stat().st_ctime).strftime('%Y-%m-%d')

    # set category and tags if provided
    if category:
        post.categories = category
    if tags:
        post.tags = tags

    # set more attributes if can get from post content
    attributes = read_frontmatter(post.content)
    for name in ['title', 'categories', 'tags', 'layout', 'date']:
        if attributes.get(name):
            setattr(post, name, attributes[name])

    # if not able to get post title from content, use file name as title
    if not post.title:
        post.title = re.sub(r'(!{0,1}\d{4}-\d{2}-\d{2}-{0,1})', '', post_file.stem)

    # check if this is a post not ready for publish
    if post_file.stem.startswith('!') or post_file.stem.startswith('！'):
        post.not_ready = True
        post.title = post.title.replace('!', '').replace('！', '')

    # translate to English
    post.en_title = translate(post.title)

    # build the post file name and location
    post.filename = post.en_title
    post.filename = re.sub(r'[^\d\w]', '-', post.filename).lower()
    post.filename = re.sub(r'-+', '-', post.filename).lower()
    post.filename = '{}-{}.md'.format(post.date, post.filename)

    if not direct_publish and post.not_ready:
        post.filename = '!' + post.filename

    # build post location
    if isinstance(target_dir, str):
        target_dir = Path(target_dir)
    post.location = target_dir

    # build the post content and write to target file
    post.create_content()
    target_file = post.location / post.filename
    target_file.write_text(post.content, encoding='utf8')

    # delete origin file if required
    if not keep_origin and post_file.name != target_file.name:
        post_file.unlink()

    return post


def test_build_post():
    post_file = Path('../_drafts/!find命令详解.md')
    p = make_post(post_file, category='Tech', tags='linux,bash')
    print(p)

    # post_file = Path('../_posts/2008-07-16-adyouth-bbs-close.md')
    # p = make_post(post_file, direct_publish=False)
    # print(p)
