"""
script to process _mobile to _draft.

python @mobile.py
"""

import re
from datetime import datetime
from os.path import join
from pathlib import Path

from utils import Post, translate, create_post_content, mobile_dir, draft_dir


def to_draft(post):
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
        if file.name.startswith('!') or file.name.startswith('.'):
            continue

        print('Process: {}'.format(file.name))
        p = Post()
        p.title = file.stem
        p.date = datetime.fromtimestamp(file.stat().st_ctime).strftime('%Y-%m-%d')
        with file.open(encoding='utf8') as f:
            p.content = f.readlines()
            front_lines = 0
            if p.content[0].startswith('['):
                attributes = p.content[0][1:-2].split(',')
                p.categories = attributes[:1]
                p.tags = [a[1:] for a in attributes[1:]]
                front_lines += 1
                for line in p.content[1:]:
                    if line.strip() == '':
                        front_lines += 1
                    else:
                        break

            # remove front formatter
            p.content = p.content[front_lines:]
            posts.append(to_draft(p))

    return posts


def build_draft(post):
    name = join(draft_dir, post.filename)
    content = create_post_content(post)
    with open(name, encoding='utf8', mode='w') as f:
        f.write(content)


if __name__ == '__main__':
    for p in get_posts():
        build_draft(p)
