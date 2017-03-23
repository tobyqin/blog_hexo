import os

os.system('python @prepare.py')
os.system('git add -A')
os.system('git commit -m "update blog."')
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
