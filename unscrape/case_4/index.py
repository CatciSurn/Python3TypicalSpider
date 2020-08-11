# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

import re
import hashlib
import requests
from urllib import parse
from parsel import Selector
from fontTools.ttLib import TTFont


BASE_FONT = {
    "font": [
        {'name': 'uniEE76', 'value': '0', 'hex': 'fc170db1563e66547e9100cf7784951f'},
        {'name': 'uniF57B', 'value': '1', 'hex': '251357942c5160a003eec31c68a06f64'},
        {'name': 'uniE7DF', 'value': '2', 'hex': '8a3ab2e9ca7db2b13ce198521010bde4'},
        {'name': 'uniF19A', 'value': '3', 'hex': '712e4b5abd0ba2b09aff19be89e75146'},
        {'name': 'uniF593', 'value': '4', 'hex': 'e5764c45cf9de7f0a4ada6b0370b81a1'},
        {'name': 'uniEA16', 'value': '5', 'hex': 'c631abb5e408146eb1a17db4113f878f'},
        {'name': 'uniE339', 'value': '6', 'hex': '0833d3b4f61f02258217421b4e4bde24'},
        {'name': 'uniE9C7', 'value': '7', 'hex': '4aa5ac9a6741107dca4c5dd05176ec4c'},
        {'name': 'uniEFD4', 'value': '8', 'hex': 'c37e95c05e0dd147b47f3cb1e5ac60d7'},
        {'name': 'uniE624', 'value': '9', 'hex': '704362b6e0feb6cd0b1303f10c000f95'}
    ]
}


def create_base_font_hex():
    """
    构造基本的字符-字形信息映射
    :return:
    """
    name_value_list = [
        ("uniEE76", "0"), ("uniF57B", "1"), ("uniE7DF", "2"),
        ("uniF19A", "3"), ("uniF593", "4"), ("uniEA16", "5"),
        ("uniE339", "6"), ("uniE9C7", "7"), ("uniEFD4", "8"), ("uniE624", "9")
    ]
    # 使用TTFont库打开本地下载好的woff字体文件
    font = TTFont('case_4/target.woff')
    n_v_h_li = []
    for name, value in name_value_list:
        content = font['glyf'].glyphs.get(name).data
        glyph = hashlib.md5(content).hexdigest()
        n_v_h_li.append({"name": name, "value": value, "hex": glyph})

def parsel_for_get_page():
    """
    使用parsel库解析网页内容, 并将woff格式的文件保存到本地
    :return:
    """
    url = "http://www.porters.vip/confusion/movie.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/79.0.3945.130 Safari/537.36"
    }
    response = requests.get(url=url, headers=headers)
    selector = Selector(response.text)

    # 提取页面加载的所有css文件路径
    css_path = selector.css('link[rel="stylesheet"]::attr(href)').extract()

    # 拼接完整的css路径
    # http://www.porters.vip/confusion/css/movie.css
    full_css_url = parse.urljoin(url, css_path[-1].replace('./', ''))

    # 发送请求，获取css文件内容
    css_response = requests.get(url=full_css_url, headers=headers)

    # 匹配css文件中的woff字体文件路径
    woff_url = re.findall(r"src:url\('..(.*.woff)'\) format\('woff'\);", css_response.text)
    if woff_url:
        full_woff_url = url.split('/movie')[0] + woff_url[0]
        woff_str = requests.get(url=full_woff_url, headers=headers)

        # 将woff格式的文件保存到本地
        with open("case_4/target.woff", "wb") as f:
            f.write(woff_str.content)


def parse_font_woff(web_code):
    """
    woff格式文本字符转换
    :param web_code: html文本中源码字符 ---> &#xe624.&#xe9c7(9.7)
    :return:
    """
    # 编码字符转换
    woff_code = [i.upper().replace('&#X', 'uni') for i in web_code.split(".")]

    # 使用TTFont库打开本地下载好的woff字体文件
    font = TTFont('case_4/target.woff')
    # 从字体文件中取出对应的编码字形信息
    result = []
    for item in woff_code:
        print(item)
        content = font['glyf'].glyphs.get(item).data  # ???

        # 将字形数据进行MD5加密
        glyph = hashlib.md5(content).hexdigest()

        # 与基准字形中的MD5值进行匹配，匹配成功， 则取出对应的value值

        for _ in BASE_FONT.get("font"):
            if _.get("hex") == glyph:
                result.append(_.get("value"))
    print(result)


if __name__ == '__main__':
    # create_base_font_hex()
    # parsel_for_get_page()
    test_str = "&#xe624.&#xe9c7"  # 爬取得到源码下的电影评分
    parse_font_woff(test_str)