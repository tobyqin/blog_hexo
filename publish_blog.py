import glob
import os
import re
from datetime import datetime
from os.path import join, dirname, abspath, exists
from shutil import copy2, rmtree

current_path = dirname(__file__)
src_post_path = abspath(join(current_path, '_posts'))
src_image_path = abspath(join(src_post_path, 'images'))
dst_post_path = abspath(join(current_path, 'source', '_posts'))
dst_image_path = abspath(join(current_path, 'source', 'images'))


def copy_images_dir():
    """Copy images from /_posts/images to /source/images"""
    if not exists(dst_image_path):
        os.mkdir(dst_image_path)

    for img in os.listdir(src_image_path):
        src = join(src_image_path, img)
        dst = join(dst_image_path, img)

        if exists(dst):
            os.remove(dst)

        copy2(src, dst)


def fix_image_path(source_file):
    """
    1. Copy posts from /_posts to /source/_posts folder
    2. Fix image url to use file in /source/images/*
    """

    new_file = source_file.replace('_posts', 'source/_posts')
    new_file = abspath(new_file)

    if not exists(dst_post_path):
        os.makedirs(dst_post_path)

    content = str()
    with open(source_file, encoding='utf-8') as f:
        for line in f:
            if '(images/' in line or '(images\\' in line:
                line = line.replace('(images/', '(/images/')
                line = line.replace('(images\\', '(/images/')
            content += line

    with open(new_file, 'w', encoding='utf-8') as f:
        f.writelines(content)


def add_timestamp_prefix(file_name):
    """Update file name with timestamp prefix."""

    names = os.path.split(file_name)
    folder = names[0]
    name = names[-1]
    time_prefix = None

    # read time stamp from blog date: section
    with open(file_name, encoding='utf-8') as f:
        for line in f:
            if line.startswith('date:'):
                time_prefix = line.split()[1]
                break

    # raise error if no date: section found
    if time_prefix is None:
        raise Exception('Cannot find time stamp for {}'.format(file_name))
    else:
        real_time = datetime.strptime(time_prefix, '%Y-%m-%d').strftime('%Y-%m-%d')

    # for line in fileinput.input(file_name, inplace=True):
    #     if line.startswith('date: {}'.format(time_prefix)):
    #         line = line.replace(time_prefix, real_time)
    #     sys.stdout.write(line)

    # update timestamp for name with date
    pattern = r'(^20\d\d-\d+-\d+).*'
    match = re.match(pattern, name)
    if match:
        new_name = real_time + name[len(match.group(1)):]
    else:
        new_name = real_time + name

    # rename old file name to new file name with timestamp
    new_name = new_name.replace(' ', '-')
    new_name = os.path.join(folder, new_name)

    if file_name != new_name:

        if os.path.exists(new_name):
            os.remove(new_name)

        print("{}=>{}".format(file_name, new_name))
        os.rename(file_name, new_name)


if __name__ == '__main__':
    copy_images_dir()
    rmtree(dst_post_path, ignore_errors=True)

    for f in glob.glob(join(src_post_path, "*.md")):
        add_timestamp_prefix(f)

    for f in glob.glob(join(src_post_path, "*.md")):
        fix_image_path(f)
