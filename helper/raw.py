"""
script to process _raw to _draft.
"""

import re
from datetime import datetime
from os.path import join
from pathlib import Path

from helper.utils import Post, translate, create_post_content, raw_dir, draft_dir


def raw_to_draft(post):
    # fix category for such posts
    post.categories = ['Reprint']

    # translate title
    post.en_title = translate(post.title)

    # generate filename
    post.filename = re.sub(r'\s', '-', post.en_title).lower()
    post.filename = '!{}-{}.md'.format(post.date, re.sub(r'[^\d\w-]', '', post.filename))
    return post


def get_raw_posts():
    posts = []
    for raw_file in Path(raw_dir).glob('**/*.md'):
        # skip file name starts with ! and .
        if raw_file.name.startswith('!') or raw_file.name.startswith('.'):
            continue

        print('Process: {}'.format(raw_file.name))
        p = Post()
        p.date = datetime.fromtimestamp(raw_file.stat().st_ctime).strftime('%Y-%m-%d')
        with raw_file.open(encoding='utf8') as f:
            p.content = f.readlines()
            if p.content[0].startswith('---'):
                attribute = ''
                front_lines = 1
                for line in p.content[1:]:
                    front_lines += 1
                    if line.startswith('---'):
                        break
                    else:
                        if line.startswith('title'):
                            p.title = line.replace('title:', '').strip()
                        elif line.startswith('categories:') or line.startswith('tags:'):
                            attribute = line.split(':')[0]
                        elif line.strip().startswith('-'):
                            getattr(p, attribute).append(line.strip().replace('-', '').strip())
                        else:
                            print('Unknown formatter: "{}"'.format(line.strip()))

                # remove front formatter
                p.content = p.content[front_lines:]
                posts.append(raw_to_draft(p))

    return posts


def build_draft(post):
    name = join(draft_dir, post.filename)
    content = create_post_content(post)
    with open(name, encoding='utf8', mode='w') as f:
        f.write(content)


def run():
    for p in get_raw_posts():
        build_draft(p)


if __name__ == '__main__':
    run()
