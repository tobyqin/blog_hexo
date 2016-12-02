import glob
import os


def to_relative(source_file):
    content = str()
    with open(source_file) as f:
        for line in f:
            if 'images/' in line:
                line = line.replace('../images/', 'images/')
            content += line

        with open(source_file, 'w') as f:
            f.writelines(content)


def clean_up(folder):
    files = os.listdir(folder)
    for f in files:
        if not f.startswith('.'):
            os.remove(os.path.join(folder, f))


def convert(source_file):
    new_file = source_file.replace('_posts', 'source/_posts')
    new_file = os.path.abspath(new_file)
    if not os.path.exists(os.path.dirname(new_file)):
        os.makedirs(os.path.dirname(new_file))
    content = str()
    with open(source_file) as f:
        for line in f:
            if 'images/' in line or 'images\\' in line:
                line = line.replace('images/', '/images/')
                line = line.replace('images\\', '/images/')
            content += line

    with open(new_file, 'w') as f:
        f.writelines(content)


def fix_file(file_name):
    names = os.path.split(file_name)
    folder = names[0]
    name = names[-1]
    time_prefix = None
    with open(file_name) as f:
        for line in f:
            if line.startswith('date:'):
                time_prefix = line.split()[1]
                break

    if time_prefix is None:
        raise Exception('Cannot find time stamp for {}'.format(file_name))
    else:
        time_prefix += "-"

    if name.startswith('20'):
        new_name = time_prefix + name[11:]
    else:
        new_name = time_prefix + name

    new_name = new_name.replace(' ', '-')
    new_name = os.path.join(folder, new_name)
    if file_name != new_name:
        if os.path.exists(new_name):
            os.remove(new_name)

        # print "{}=>{}".format(file_name, new_name)
        os.rename(file_name, new_name)


if __name__ == '__main__':
    current_path = os.path.dirname(__file__)
    post_path = os.path.join(current_path, '_posts')
    clean_up(post_path.replace('_posts', 'source/_posts'))
    for f in glob.glob(os.path.join(post_path, "*.md")):
        fix_file(f)
        convert(f)
