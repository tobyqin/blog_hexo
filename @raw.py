"""
script to process _raw to _draft.

python @raw.py
"""


def get_img(url, filename):
    import urllib.request
    urllib.request.urlretrieve(url, filename)
