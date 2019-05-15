"""
Use this script to create a hexo draft post.
By default, the draft file name will starts with `!`.
When draft ready, remove the leading `!` then it will be published next time.
"""
import re
import uuid
from codecs import open
from os.path import join

from helper.utils import draft_dir, Post, create_post_content


def run():
    post = Post()
    print('Creating new draft...\n')
    print('Title:')
    post.title = input()

    print('Category: Tech (default)')
    category = input()
    if not category:
        category = 'Tech'

    tags = ''
    while not tags:
        print('Tags: (required)')
        tags = input()

    if not post.title:
        post.title = "{}-{}".format(category, uuid.uuid4().hex)

    post.categories = category.split()
    post.tags = tags.split()

    content = create_post_content(post)
    draft_name = '!{}-{}.md'.format(post.date, re.sub(r'\s', '-', post.title.strip()))
    draft_name = join(draft_dir, draft_name.lower())
    with open(draft_name, encoding='utf8', mode='w') as f:
        f.write(content)

    print('\nOK, draft created.\n{}'.format(draft_name))


if __name__ == '__main__':
    run()
