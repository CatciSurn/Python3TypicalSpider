import requests
from urllib.parse import urljoin

import json
from os import makedirs
from os.path import exists

RESULTS_DIR = 'case_3/results'
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)
def save_data(data):
    name = data.get('name')
    data_path = f'{RESULTS_DIR}/{name}.json'
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

BASE_URL = 'https://login3.scrape.center/'
LOGIN_URL = urljoin(BASE_URL, '/api/login')
INDEX_URL = urljoin(BASE_URL, '/api/book')
USERNAME = 'admin'
PASSWORD = 'admin'

response_login = requests.post(LOGIN_URL, json={
    'username': USERNAME,
    'password': PASSWORD
})
data = response_login.json()
print('Response JSON', data)
jwt = data.get('token')
print('JWT', jwt)

headers = {
    'Authorization': f'jwt {jwt}'
}
response_index = requests.get(INDEX_URL, params={
    'limit': 18,
    'offset': 0
}, headers=headers)
print('Response Status', response_index.status_code)
print('Response URL', response_index.url)
# print('Response Data', response_index.json())
save_data(response_index.json())
