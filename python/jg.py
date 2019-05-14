"""
publish blog from jiainguoyun.
1. pull changes from /Blog/New
2. push _posts to /Blog/Posts
"""

import os
import urllib.parse
from os.path import join, dirname

from webdavfs.webdavfs import WebDAVFS

if 'jg_login' not in os.environ and 'jg_password' not in os.environ:
    raise EnvironmentError('Please set "jg_login" and "jg_password" in environment!')

target_dir = join(dirname(dirname(__file__)), '_mobile')
url = 'https://dav.jianguoyun.com/dav'
options = {
    'url': url,
    'login': os.environ['jg_login'],
    'password': os.environ['jg_password'],
    'root': '/Blog/New'
}

fs = WebDAVFS(**options)


def urlparse(string):
    return urllib.parse.quote(string)


def get_new_files():
    files = fs.listdir('.')[1:]
    return [f for f in files if not (f.startswith('!') or f.startswith('！'))]


def download_file(remote_file):
    options['remote'] = urlparse(remote_file)
    options['local'] = join(target_dir, remote_file)
    cmd = "curl -u '{login}:{password}' '{url}{root}/{remote}' -o '{local}'".format_map(options)
    os.system(cmd)


def delete_file(remote_file):
    options['remote'] = urlparse(remote_file)
    cmd = "curl -X DELETE -u '{login}:{password}' '{url}{root}/{remote}'".format_map(options)
    os.system(cmd)


def run():
    for f in get_new_files():
        download_file(f)
        delete_file(f)


if __name__ == '__main__':
    run()
