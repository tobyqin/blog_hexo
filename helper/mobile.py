"""
script to process _mobile to _draft.
"""
import os
import re
from datetime import datetime
from os.path import join, exists
from pathlib import Path
import shutil

from helper.utils import Post, translate, create_post_content, mobile_dir, draft_dir


def make_draft(post):
    if not post.categories:
        post.categories = ['Thoughts']

    # translate title
    post.en_title = translate(post.title)

    # generate filename
    post.filename = re.sub(r'\s', '-', post.en_title).lower()
    post.filename = '{}-{}.md'.format(post.date, re.sub(r'[^\d\w-]', '', post.filename))
    return post


def get_posts():
    posts = []
    for file in Path(mobile_dir).glob('**/*.md'):
        # skip file name starts with ! and .
        if file.name.startswith('!') or file.name.startswith('.') or file.name.startswith('！'):
            continue

        print('Process: {}'.format(file.name))
        post = Post()
        post.title = file.stem

        if post.title.endswith('.md'):
            post.title = post.title[:-3]

        post.date = datetime.fromtimestamp(file.stat().st_ctime).strftime('%Y-%m-%d')
        with file.open(encoding='utf8') as f:
            post.content = f.readlines()
            front_lines = 0

            # Process attribute line, e.g. [Reading,#test,#test2]
            if post.content[0].startswith('['):
                # remove `[` & `]` then split with `,`
                attributes = post.content[0][1:-2].split(',')
                post.categories = attributes[:1]
                post.tags = [attr[1:] for attr in attributes[1:]]
                front_lines += 1

            # remove blank lines until real content
            for line in post.content[1:]:
                if line.strip() == '':
                    front_lines += 1
                else:
                    break

            # remove attribute line and front blank content
            post.content = post.content[front_lines:]
            posts.append(make_draft(post))

        os.remove(str(file))

    return posts


def build_draft(post):
    name = join(draft_dir, post.filename)
    content = create_post_content(post)
    with open(name, encoding='utf8', mode='w') as f:
        f.write(content)


def run():
    for p in get_posts():
        build_draft(p)

    image_dir = join(mobile_dir, 'images')
    for i in os.listdir(image_dir):
        shutil.move(i, join(draft_dir,'images'))


if __name__ == '__main__':
    run()
