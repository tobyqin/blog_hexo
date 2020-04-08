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

import helper.mobile
from helper.post_builder import make_post
from helper.utils import draft_dir, current_dir, download_img, log

draft_image_dir = abspath(join(draft_dir, 'images'))
root_post_dir = abspath(join(current_dir, '_posts'))
root_post_image_dir = abspath(join(root_post_dir, 'images'))
source_post_dir = abspath(join(current_dir, 'source', '_posts'))
source_post_image_dir = abspath(join(current_dir, 'source', 'images'))
image_server = 'https://tobyqin.github.io/images/'


def replace_img(origin_url):
    import urllib.error
    img_name = origin_url.split('/')[-1]
    img_path = '{}/{}/{}'.format(draft_image_dir, datetime.now().strftime('%Y-%m'), img_name)
    try:
        download_img(origin_url, img_path)
        return img_path.replace(draft_dir + '/', '')  # use relative path
    except urllib.error.HTTPError:  # failed to download image
        print('Warning: failed to download image: {}!'.format(origin_url))
        return origin_url


def test_replace_img():
    print(replace_img('https://static.cnbetacdn.com/article/2019/0114/116c69b7fb0b665.jpg'))


def prepare_drafts():
    """
    fix markdown format and download remote images to local for drafts.
    """

    def process_img(line: str):
        m = re.search(r'(\[!\[([^\]]*)\]\((http[^\\)]+)\)\]\((http[^\\)]+)\))', line)
        if m:
            place_holder, img_text, new_img_url, _ = m.groups()
            new_img_url = replace_img(new_img_url)
            new_img_tag = '![{}]({})'.format(img_text, new_img_url)
            return line.replace(place_holder, new_img_tag)
        else:
            m = re.search(r'(!\[([^\]]*)\]\((http[^\\)]+)\))', line)
            if m:
                place_holder, img_text, new_img_url = m.groups()
                new_img_url = replace_img(new_img_url)
                new_img_tag = '![{}]({})'.format(img_text, new_img_url)
                return line.replace(place_holder, new_img_tag)

        return line

    def is_item_line(line: str):
        return re.match(r'^ *(\*|-|(\d\.)+) +', line)

    def is_empty_line(line: str):
        return line.strip() == ''

    def next_line_should_remove(current_line: str, current_i: int, content: list):
        max_index = len(content) - 1
        next_index = current_i + 1
        next_next_index = next_index + 1
        should_remove = False

        # for empty line, remove continue empty line
        if is_empty_line(current_line) and next_index <= max_index:
            next_line = content[next_index]
            should_remove = is_empty_line(next_line)

        # for item line
        if is_item_line(current_line):

            if next_next_index <= max_index:  # more than 2 lines left
                next_line = content[next_index]
                next_next_line = content[next_next_index]
                if is_empty_line(next_line):  # if next line is empty
                    # and next next line is empty or is item line
                    should_remove = is_empty_line(next_next_line) or is_item_line(next_next_line)

            elif next_index <= max_index:  # only 2 lines left, remove last empty line
                next_line = content[next_index]
                should_remove = is_empty_line(next_line)

        return should_remove

    for draft in Path(draft_dir).glob('*.md'):
        make_post(draft,
                  category='Tech',
                  tags='tips',
                  keep_origin=False,
                  direct_publish=False)

    for draft in Path(draft_dir).glob('*.md'):
        content = []
        with draft.open(encoding='utf8') as f:

            should_remove = False
            lines = f.readlines()
            for i, line in enumerate(lines):

                if should_remove:
                    continue

                line = process_img(line)

                if is_empty_line(line):
                    should_remove = next_line_should_remove(line, i, lines)

                if is_item_line(line):
                    line = re.sub(r'^( *)\* +', r'\1* ', line, count=1)  # list item
                    line = re.sub(r'^( *)- +', r'\1* ', line, count=1)  # list item
                    line = re.sub(r'^( *)(\d+)\. +', r'\1\2. ', line, count=1)  # order item
                    should_remove = next_line_should_remove(line, i, lines)

                content.append(line)
        draft.write_text(''.join(content), encoding='utf8')


def test_prepare_draft():
    prepare_drafts()


def incremental_copy_tree(src, dst, match_pattern=None, ignore_pattern=None, debug=False):
    """copy tree with incremental:
    0. ignore files in destination if not in source.
    1. over write files in destination if existed in source.
    """
    source_dir = Path(src)
    for item in source_dir.glob('**/*'):
        if item.is_file() and should_copy_file(item.name, ignore_pattern, match_pattern, debug):

            from_name = str(item)
            target_name = from_name.replace(src, dst)

            log('Copy: {} => {}'.format(item, target_name), debug)
            if exists(target_name):
                os.remove(target_name)

            target_dir = dirname(target_name)
            if not exists(target_dir):
                os.mkdir(target_dir)

            copy2(from_name, target_name)


def should_copy_file(filename, ignore_pattern, match_pattern, debug):
    should_copy = False
    if not ignore_pattern and not match_pattern:
        should_copy = True

    if ignore_pattern:
        if re.match(ignore_pattern, filename):
            log('Ignore pattern: {}'.format(filename), debug)
            should_copy = False
        else:
            should_copy = True
    if match_pattern:
        if re.match(match_pattern, filename):
            log('Match pattern: {}'.format(filename), debug)
            should_copy = True
        else:
            should_copy = False
    return should_copy


def copy_top_dir(from_dir, to_dir):
    """
    only copy top level files.
    """
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
    incremental_copy_tree(draft_dir, root_post_dir, match_pattern=r'^\d{4}-\d{2}-\d{2}.*md', debug=True)
    incremental_copy_tree(draft_image_dir, root_post_image_dir, ignore_pattern='^[\.\!].*', debug=True)


def test_publish_drafts():
    publish_drafts()


def publish_post_images():
    """Copy images from /_posts/images to /source/images"""
    incremental_copy_tree(root_post_image_dir, source_post_image_dir)


def publish_post(source_file):
    """
    1. Copy posts from /_posts to /source/_posts folder
    2. Fix image url to use files in /source/images/*
    """

    new_file = source_file.replace('_posts', 'source/_posts')
    new_file = abspath(new_file)

    if not exists(source_post_dir):
        os.makedirs(source_post_dir)

    content = str()
    with open(source_file, encoding='utf-8') as f:
        for line in f:
            if '(images/' in line or '(images\\' in line:
                line = line.replace('(images/', '(' + image_server)
                line = line.replace('(images\\', '(' + image_server)
            content += line

    with open(new_file, mode='w', encoding='utf-8') as f:
        f.writelines(content)


def run():
    print('Prepare drafts...')
    helper.mobile.run()
    prepare_drafts()
    publish_drafts()
    publish_post_images()
    rmtree(source_post_dir, ignore_errors=True)

    for f in glob.glob(join(root_post_dir, "*.md")):
        publish_post(f)

    print('OK.')


if __name__ == '__main__':
    run()
