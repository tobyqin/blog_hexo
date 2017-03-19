import os

os.system('python publish_blog.py')
os.system('git add -A')
os.system('git commit -m "update blog."')
os.system('git pull origin master')
os.system('git push origin master')
os.system('git remote add osc git@git.oschina.net:ggqq/hexo.git')
os.system('git pull osc master')
os.system('git push osc master')
