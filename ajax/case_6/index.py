import hashlib
import time
import base64
from typing import List, Any
import requests

import json
from os import makedirs
from os.path import exists

INDEX_URL = 'https://spa6.scrape.center/api/movie?limit={limit}&offset={offset}&token={token}'
DETAIL_URL = 'https://spa6.scrape.center/api/movie/{id}?token={token}'
LIMIT = 10
OFFSET = 0
SECRET = 'ef34#teuq0btua#(-57w1q5o5--j@98xygimlyfxs*-!i-0-mb'


def get_token(args: List[Any]):
    '''
    获取接口token
    '''
    # 先将 /api/movie 放到一个列表里面；
    # 列表中加入当前时间戳；
    # 将列表内容用逗号拼接；
    # 将拼接的结果进行 SHA1 编码；
    # 将编码的结果和时间戳再次拼接；
    # 将拼接后的结果进行 Base64 编码。
    timestamp = str(int(time.time()))
    args.append(timestamp)
    sign = hashlib.sha1(','.join(args).encode('utf-8')).hexdigest()
    return base64.b64encode(','.join([sign, timestamp]).encode('utf-8')).decode('utf-8')
    
RESULTS_DIR = 'case_6/results'
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)
def save_data(data):
    name = data.get('name')
    data_path = f'{RESULTS_DIR}/{name}.json'
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

args = ['/api/movie']
token = get_token(args=args)
index_url = INDEX_URL.format(limit=LIMIT, offset=OFFSET, token=token)
response = requests.get(index_url)
print('response', response.json())

result = response.json()
for item in result['results']:
    id = item['id']
    encrypt_id = base64.b64encode((SECRET + str(id)).encode('utf-8')).decode('utf-8')
    args = [f'/api/movie/{encrypt_id}']
    token = get_token(args=args)
    detail_url = DETAIL_URL.format(id=encrypt_id, token=token)
    response = requests.get(detail_url)
    # print('response', response.json())
    save_data(response.json())
