"""
Use this script to push changes to remote git server.
"""
import os
import shutil

py = 'python3' if shutil.which('python3') else 'python'

os.system('{} @mobile.py'.format(py))
os.system('{} @prepare.py'.format(py))
os.system('git add -A')
os.system('git commit -m "update website."')
os.system('git pull origin master')
os.system('git push origin master')

# backup to git osc
os.system('git remote add osc git@git.oschina.net:ggqq/hexo.git')
os.system('git pull osc master')
os.system('git push osc master')

# backup to coding.net
os.system('git remote add coding git@git.coding.net:tobyqin/blog.git')
os.system('git pull coding master')
os.system('git push coding master')
