import requests
import logging
import json
from os import makedirs
from os.path import exists

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s; %(message)s')#配置输出格式
INDEX_URL = 'https://spa1.scrape.center/api/news/?limit={limit}&offset={offset}'

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


# LIMIT = 10
def scrape_index(page,LIMIT):
    url = INDEX_URL.format(limit=LIMIT, offset=LIMIT * (page - 1))
    return scrape_api(url)


DETAIL_URL = 'https://spa1.scrape.center/api/movie/{id}'
def scrape_detail(id):
    url = DETAIL_URL.format(id=id)
    return scrape_api(url)


RESULTS_DIR = 'case_1/results'
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)

def save_data(data):
    name = data.get('name')
    data_path = f'{RESULTS_DIR}/{name}.json'
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


# TOTAL_PAGE = 10
def main(parameters):
    for page in range(1, parameters[1] + 1):#每页爬取数量
        index_data = scrape_index(page,parameters[0])#爬取页数
        for item in index_data.get('results'):
            id = item.get('id')
            detail_data = scrape_detail(id)
            logging.info('详细数据 %s', detail_data)
            save_data(detail_data)
def get_parameters():
    print('-'*20)
    print('爬取数量 = 每页爬取数量 * 爬取页数')
    LIMIT = int(input('输入每页爬取数量'))
    TATAL_PAGE = int(input('输入爬取页数'))
    return LIMIT,TATAL_PAGE
if __name__ == '__main__':
    parameters = get_parameters()
    main(parameters)