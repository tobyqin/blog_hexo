"""
Use this script to preview blog locally.
"""
import os

import helper.prepare


def run():
    helper.prepare.run()
    os.system('node_modules/.bin/hexo clean')
    os.system('node_modules/.bin/hexo g')
    os.system('node_modules/.bin/hexo s')


if __name__ == '__main__':
    run()
