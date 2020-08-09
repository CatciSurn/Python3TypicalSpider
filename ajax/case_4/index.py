import requests
import logging
import json
from os import makedirs
from os.path import exists

LIMIT=10
PAGE=1

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s; %(message)s')#配置输出格式
INDEX_URL = 'https://spa4.scrape.center/api/news/?limit={limit}&offset={offset}'

def scrape_api(url):
    '''爬取接口'''
    logging.info('爬取 %s...', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        logging.error('抓取%s时获得无效状态代码%s', response.status_code, url)
    except requests.RequestException:
        logging.error('清除%s时发生错误', url, exc_info=True)

def scrape_index(page):
    url = INDEX_URL.format(limit=LIMIT, offset=LIMIT * (page - 1))
    return scrape_api(url)

RESULTS_DIR = 'case_4/results'
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)
def save_data(data):
    name = data.get('name')
    data_path = f'{RESULTS_DIR}/{name}.json'
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

def main():
    for i in range(PAGE):
        data=scrape_index(i + 1)
        save_data(data)
main()