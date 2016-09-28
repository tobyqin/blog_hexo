import re
import tempfile
import os


def fix_line(line):
    return line.replace('\n', '<br/>')


def fix_file(file_name):
    new_file = os.path.join(tempfile.gettempdir(), 'new.md')
    is_code = False
    with open(new_file, 'w') as f1:
        with open(file_name) as f:
            for line in f:
                if line.startswith('```'):
                    is_code = not is_code
                    f1.write(line)
                    continue

                if is_code:
                    f1.write(fix_line(line))
                else:
                    f1.write(line)

    print new_file


if __name__ == '__main__':
    test_file = r"C:\Users\toby.qin\src\hexo\source\_posts\from-csharp-to-python-overview.md"
    fix_file(test_file)
