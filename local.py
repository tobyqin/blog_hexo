import os

os.system('python publish_blog.py')
os.system('hexo clean')
os.system('hexo g')
os.system('hexo s')
