import re
import tempfile
import os
import glob


def fix_file(file_name):
    names = os.path.split(file_name)
    folder = names[0]
    name = names[-1]
    new_name = name
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
    print "{}=>{}".format(file_name, new_name)
    os.rename(file_name, new_name)


if __name__ == '__main__':
    current_path = os.path.dirname(__file__)
    post_path = os.path.join(current_path, 'source', '@posts')
    for f in glob.glob(os.path.join(post_path, "*.md")):
        fix_file(f)
