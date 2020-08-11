import requests
from scrapy import Selector
import  re

url = 'http://www.porters.vip/confusion/flight.html'
response = requests.get(url)
print(response.text)
html = Selector(text=response.text)                 #将源码转为Selector对象
ems = html.xpath('//em[@class="rel"]').extract()    #SelectorList -> List
#每个em标签在循环
for em in ems:
    html_em_element = Selector(text=em)
    html_bs= html_em_element.xpath('//b').extract()
    b_first  = html_bs.pop(0)
    html_b_first = Selector(text=b_first)
    base_price = html_b_first.xpath('//i/text()').extract()
    real_prices = []
    for  html_b_next in  html_bs:
        location = re.search('left:(.*?)px', html_b_next, re.S).group(1)
        price = re.search('">(.*?)</b>', html_b_next, re.S).group(1)
        real_prices.append({'location': location, 'price': price})
    for real_price in real_prices:
       location  = real_price.get('location')
       price = real_price.get('price')
       index = int(int(location)/16)
       base_price[index] = price
    #对不符要求的结果进行处理
    if len(base_price) == 3:
        print(base_price)
    else:
        print(base_price[1:])
