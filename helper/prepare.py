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
import helper.raw
from helper.utils import draft_dir, current_dir, get_img

draft_image_dir = abspath(join(draft_dir, 'images'))
src_post_dir = abspath(join(current_dir, '_posts'))
src_image_dir = abspath(join(src_post_dir, 'images'))
dst_post_dir = abspath(join(current_dir, 'source', '_posts'))
dst_image_dir = abspath(join(current_dir, 'source', 'images'))
image_server = 'https://tobyqin.github.io/images/'


def replace_img(origin_url):
    img_name = origin_url.split('/')[-1]
    img_path = '{}/{}/{}'.format(draft_image_dir, datetime.now().strftime('%Y-%m'), img_name)
    get_img(origin_url, img_path)
    return img_path.replace(draft_dir + '/', '')


def test_replace_img():
    print(replace_img('https://static.cnbetacdn.com/article/2019/0114/116c69b7fb0b665.jpg'))


def prepare_draft():
    """
    fix markdown format and download remote images to local for drafts.
    """

    def process_img(l):
        m = re.search(r'(\[!\[([^\]]*)\]\((http[^\)]+)\)\]\((http[^\)]+)\))', l)
        if m:
            place_holder, img_text, new_img_url, _ = m.groups()
            new_img_url = replace_img(new_img_url)
            new_img_tag = '![{}]({})'.format(img_text, new_img_url)
            return l.replace(place_holder, new_img_tag)
        else:
            m = re.search(r'(!\[([^\]]*)\]\((http[^\)]+)\))', l)
            if m:
                place_holder, img_text, new_img_url = m.groups()
                new_img_url = replace_img(new_img_url)
                new_img_tag = '![{}]({})'.format(img_text, new_img_url)
                return l.replace(place_holder, new_img_tag)

        return l

    def is_item_line(l):
        return re.match(r'^ *(\*|(\d\.)+) +', l)

    def next_line_should_remove(current_line, current_i, total):
        max_i = len(total) - 1
        next_i = current_i + 1
        next_next_i = next_i + 1

        # for item line
        if is_item_line(current_line):

            if next_next_i <= max_i:  # more than 2 lines left
                if total[next_i].strip() == '':  # if next line is empty
                    # and next next line is empty or is item line
                    if total[next_next_i].strip() == '' or is_item_line(total[next_next_i]):
                        return True  # then remove next line
                    else:
                        return False

            elif next_i <= max_i:  # only 2 lines left, remove last empty line
                return not total[next_i].strip()

            else:
                return False

        # for empty line, remove continue empty line
        elif current_line.strip() == '':
            return next_i <= max_i and total[next_i].strip() == ''

        # not touch other lines
        else:
            return False

    for draft in Path(draft_dir).glob('*.md'):
        content = []
        with draft.open(encoding='utf8') as f:

            should_remove = False
            lines = f.readlines()
            for i, line in enumerate(lines):
                line = process_img(line)

                if line.strip() == '' and should_remove:
                    should_remove = next_line_should_remove(line, i, lines)
                    continue

                if is_item_line(line):
                    line = re.sub(r'( *)\* +', r'\1* ', line, 1)  # no order item
                    line = re.sub(r'( *)(\d+)\. +', r'\1\2. ', line, 1)  # order item
                    should_remove = next_line_should_remove(line, i, lines)

                content.append(line)
        draft.write_text(''.join(content), encoding='utf8')


def test_prepare_draft():
    prepare_draft()


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
                # print('{} => {}'.format(i, target_name))

                if exists(target_name):
                    os.remove(target_name)

                target_dir = dirname(target_name)
                if not exists(target_dir):
                    os.mkdir(target_dir)

                copy2(from_name, target_name)


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
    copy_tree(draft_dir, src_post_dir)


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


def run():
    print('Prepare drafts...')
    helper.mobile.run()
    helper.raw.run()
    prepare_draft()
    publish_drafts()
    publish_images()
    rmtree(dst_post_dir, ignore_errors=True)

    for f in glob.glob(join(src_post_dir, "*.md")):
        fix_post_file_name(f)
        publish_post(f)

    print('OK.')


if __name__ == '__main__':
    run()
