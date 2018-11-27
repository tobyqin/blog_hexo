import hashlib
import json
import random
import urllib.parse
import urllib.request

app_id = '20181121000237296'
sec_key = 'FpUUXfla5UuEcStx5tHk'
host = 'http://api.fanyi.baidu.com/api/trans/vip/translate?'

def translate(txt, from_lang='auto', to_lang='en'):
    '''
    https://fanyi-api.baidu.com/api/trans/product/apidoc
    '''
    salt = random.randint(32768, 65536)
    sign = app_id + txt + str(salt) + sec_key
    sign = hashlib.md5(sign.encode('utf-8')).hexdigest()
    query = {'q': txt, 'from': from_lang, 'to': to_lang, 'appid': app_id, 'salt': salt, 'sign': sign}
    target = host + urllib.parse.urlencode(query)

    response = urllib.request.urlopen(target).read().decode('utf-8')
    return json.loads(response)['trans_result'][0]['dst']


def test_translate():
    src = '准备好开始学习英语了吗'
    print('文言文翻译')
    print('源自: {}'.format(src))
    print('结果: ' + translate('准备好开始学习英语了吗'))
