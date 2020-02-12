"""
publish blog from jianguoyun.

1. pull changes from /Blog/New
 - if have new files -> not starts with !
 - download to _mobile
 - delete from jianguoyun
 - convert _mobile to _drafts
 - upload _draft to /Blog/draft

2. pull changes from /Blog/Drafts
 - if have new files -> contains !changes.*
 - download to _drafts
 - delete !changes.*
"""

import os
import pathlib
import urllib.parse
from os.path import join


import helper.mobile
from helper.utils import draft_dir, mobile_dir

NEW_DIR = '/Blog/New'
DFT_DIR = '/Blog/Drafts'


def get_options(root=NEW_DIR):
    if 'jg_login' not in os.environ and 'jg_password' not in os.environ:
        raise EnvironmentError('Please set "jg_login" and "jg_password" in environment!')

    return {
        'url': 'https://dav.jianguoyun.com/dav',
        'login': os.environ['jg_login'],
        'password': os.environ['jg_password'],
        'root': root
    }


def get_fs(options):
    from webdavfs.webdavfs import WebDAVFS
    return WebDAVFS(**options)


def urlparse(string):
    return urllib.parse.quote(string)


def get_webdav_files(fs, auto_exclude=True):
    files = fs.listdir('.')[1:]
    if auto_exclude:
        return [f for f in files if not (f.startswith('!') or f.startswith('！'))]
    else:
        return files


def download_file(remote_file, local_file):
    options = get_options()
    options['remote'] = urlparse(remote_file)
    options['local'] = local_file
    cmd = "curl -u '{login}:{password}' '{url}{remote}' -o '{local}'".format_map(options)
    os.system(cmd)


def delete_file(remote_file):
    options = get_options()
    options['remote'] = urlparse(remote_file)
    cmd = "curl -X DELETE -u '{login}:{password}' '{url}{remote}'".format_map(options)
    os.system(cmd)


def upload_file(local_file, remote_file):
    options = get_options()
    options['remote'] = urlparse(remote_file)
    options['local'] = local_file
    cmd = "curl --user '{login}:{password}' -T '{local}' '{url}{remote}'".format_map(options)
    os.system(cmd)


def run():
    # detect changes in /Blog/New
    fs = get_fs(get_options(NEW_DIR))
    for f in get_webdav_files(fs):
        print('found new in /Blog/New...')
        remote = '{}/{}'.format(NEW_DIR, f)
        local = join(mobile_dir, f)
        download_file(remote, local)
        delete_file(remote)

        print('convert to drafts...')
        helper.mobile.run()

        print('upload drafts to /Blog/Drafts')
        for f in pathlib.Path(draft_dir).glob('*.md'):
            remote = '{}/{}'.format(DFT_DIR, f.name)
            upload_file(str(f), remote)
    else:
        # check /Blog/Drafts contains !changes
        fs = get_fs(get_options(DFT_DIR))
        files = get_webdav_files(fs, auto_exclude=False)
        should_update = any([f.startswith('!changes') for f in files])

        if should_update:
            print('found changes in /Blog/Drafts')
            for f in files:
                remote = '{}/{}'.format(DFT_DIR, f)
                local = join(draft_dir, f)

                # delete the !changes mark
                if f.startswith('!changes'):
                    print('\ndelete {}...'.format(remote))
                    delete_file(remote)

                # download other files
                else:
                    print('\ndownload {}...'.format(remote))
                    download_file(remote, local)


if __name__ == '__main__':
    run()
