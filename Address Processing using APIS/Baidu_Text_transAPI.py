# -*- coding: utf-8 -*-

# This code shows an example of text translation from English to Simplified-Chinese.
# This code runs on Python 2.7.x and Python 3.x.
# You may install `requests` to run this code: pip install requests
# Please refer to `https://api.fanyi.baidu.com/doc/21` for complete api document

import requests
import random
import json
import time
from hashlib import md5

# Set your own appid/appkey.
appid = ''
appkey = ''

# For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
from_lang = 'en'
to_lang =  'zh'

endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path

# query = 'Hello World! This is 1st paragraph.\nThis is 2nd paragraph.'

with open('香港\马蜂窝\香港原始地址数据.json', 'r', encoding='utf-8') as fp:
    sites = json.load(fp)

# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()
tmp_list = []
salt = random.randint(32768, 65536)
for obj in sites:
    # time.sleep(2)
    query = obj['Location']

    time.sleep(1)
    # Build request
    sign = make_md5(appid + query + str(salt) + appkey)

    headers = {'Content-Type': '/applicationx-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    # try:
    #     a = result['trans_result'][0]['dst']
    #     print(result)
    #     # print(a)
    #     obj['address'] = a = result['trans_result'][0]['dst']
    # except:
    #     continue
    # print(result['trans_result'][0]['dst'])
# result = r.json()

# Show response
    # print(json.dumps(result, indent=4, ensure_ascii=False))
    tmp_list.append(result)
    # print(tmp_list)
    # break

with open('xxx.json', 'w', encoding='utf-8') as fp:
    json.dump(tmp_list, fp=fp, ensure_ascii=False,indent=2)