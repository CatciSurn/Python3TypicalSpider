import requests
from urllib.parse import urljoin

BASE_URL = 'https://login1.scrape.center/'
LOGIN_URL = urljoin(BASE_URL, '/login')
INDEX_URL = urljoin(BASE_URL, '/page/1')
USERNAME = 'admin'
PASSWORD = 'admin'

response_login = requests.post(LOGIN_URL, data={
   'username': USERNAME,
   'password': PASSWORD
})

response_index = requests.get(INDEX_URL)
print('Response Status', response_index.status_code)
print('Response URL', response_index.url)