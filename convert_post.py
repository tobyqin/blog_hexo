import os
import glob


def to_relative(source_file):
    content = str()
    with open(source_file) as f:
        for line in f:
            if 'images/' in line:
                line = line.replace('../images/', 'images/')
            content += line

        with open(source_file, 'w') as f:
            f.writelines(content)


def convert(source_file):
    new_file = source_file.replace('_posts', 'source/_posts')
    content = str()

    with open(source_file) as f:
        for line in f:
            if 'images/' in line:
                line = line.replace('images/', 'http://betacat.online/images/')
            content += line

        with open(new_file, 'w') as f:
            f.writelines(content)


if __name__ == '__main__':
    current_path = os.path.dirname(__file__)
    post_path = os.path.join(current_path, '_posts')
    for f in glob.glob(os.path.join(post_path, "*.md")):
        convert(os.path.abspath(f))