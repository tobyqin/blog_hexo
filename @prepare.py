"""
Use this script to convert posts from _drafts or _posts.

> python @prepare.py
Will publish all `_drafts` to `_posts` folder, then publish to `source` folder.

"""
import glob
import os
import re
from codecs import open
from datetime import datetime
from os.path import join, dirname, abspath, exists, isfile
from pathlib import Path
from shutil import copy2, rmtree

current_dir = dirname(__file__)
draft_post_dir = abspath(join(current_dir, '_drafts'))
draft_image_dir = abspath(join(draft_post_dir, 'images'))
src_post_dir = abspath(join(current_dir, '_posts'))
src_image_dir = abspath(join(src_post_dir, 'images'))
dst_post_dir = abspath(join(current_dir, 'source', '_posts'))
dst_image_dir = abspath(join(current_dir, 'source', 'images'))
image_server = 'https://tobyqin.github.io/images/'


def copy_tree(src, dst):
    """copy tree:
    1. ignore files starts with . and !
    2. if exists in target, delete it then do copy.
    """
    s = Path(src)
    for i in s.glob('**/*'):
        if i.is_file():
            if not (i.name.startswith('.') or i.name.startswith('!')):
                from_name = str(i)
                target_name = from_name.replace(src, dst)
                print('{} => {}'.format(i, target_name))

                if exists(target_name):
                    os.remove(target_name)

                target_dir = dirname(target_name)
                if not exists(target_dir):
                    os.mkdir(target_dir)

                copy2(from_name, target_name)


def copy_top_dir(from_dir, to_dir):
    """only copy top level files."""
    if not exists(from_dir):
        return

    if not exists(to_dir):
        os.mkdir(to_dir)

    for file in os.listdir(from_dir):
        if file.startswith('!'):
            print('ignore: ' + file)
        else:
            src = join(from_dir, file)
            dst = join(to_dir, file)

            if isfile(src):

                if exists(dst):
                    os.remove(dst)

                copy2(src, dst)


def publish_drafts():
    copy_tree(draft_post_dir, src_post_dir)


def publish_images():
    """Copy images from /_posts/images to /source/images"""
    copy_tree(src_image_dir, dst_image_dir)


def publish_post(source_file):
    """
    1. Copy posts from /_posts to /source/_posts folder
    2. Fix image url to use files in /source/images/*
    """

    new_file = source_file.replace('_posts', 'source/_posts')
    new_file = abspath(new_file)

    if not exists(dst_post_dir):
        os.makedirs(dst_post_dir)

    content = str()
    with open(source_file, encoding='utf-8') as f:
        for line in f:
            if '(images/' in line or '(images\\' in line:
                line = line.replace('(images/', '(' + image_server)
                line = line.replace('(images\\', '(' + image_server)
            content += line

    with open(new_file, mode='w', encoding='utf-8') as f:
        f.writelines(content)


def fix_post_file_name(file_name):
    """Update file name with timestamp prefix."""

    names = os.path.split(file_name)
    folder = names[0]
    name = names[-1]
    time_prefix = None
    content = str()

    # read time stamp from blog date: section
    with open(file_name, encoding='utf-8') as f:
        for line in f:
            if line.startswith('date:'):
                time_prefix = line.split()[1]
                real_time = datetime.strptime(time_prefix, '%Y-%m-%d').strftime('%Y-%m-%d')
                line = line.replace(time_prefix, real_time)
                time_prefix = real_time
            content += line

    # raise error if no date: section found
    if time_prefix is None:
        raise Exception('Cannot find time stamp for {}'.format(file_name))

    with open(file_name, encoding='utf-8', mode='w') as f:
        f.write(content)

    # update timestamp for name with date
    pattern = r'(^20\d\d-\d+-\d+).*'
    match = re.match(pattern, name)
    if match:
        new_name = time_prefix + name[len(match.group(1)):]
    else:
        new_name = time_prefix + '-' + name

    # rename old file name to new file name with timestamp
    new_name = new_name.replace(' ', '-')
    new_name = os.path.join(folder, new_name)

    if file_name != new_name:

        if os.path.exists(new_name):
            os.remove(new_name)

        print("{}=>{}".format(file_name, new_name))
        os.rename(file_name, new_name)


if __name__ == '__main__':
    publish_drafts()
    publish_images()
    rmtree(dst_post_dir, ignore_errors=True)

    for f in glob.glob(join(src_post_dir, "*.md")):
        fix_post_file_name(f)
        publish_post(f)

    print('OK.')
