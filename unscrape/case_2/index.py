from urllib import request
import random
from bs4 import BeautifulSoup

PAGE = 10
ua_list = [ 'Mozilla/5.0 (Linux; Android 5.1.1; Z828 Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.111 Mobile Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22',
            'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/47.0.2526.107 Mobile/12F69 Safari/600.1.4',
            'Mozilla/5.0 (iPad; CPU OS 11_2_5 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) CriOS/64.0.3282.112 Mobile/15D60 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 7.1.1; SM-T350 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36',
            'Mozilla/5.0 (Linux; Android 6.0.1; SM-G610F Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
            'Mozilla/5.0 (Linux; Android 5.1.1; 5065N Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/46.0.2490.76 Mobile Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36']
ua=random.choice(ua_list)

def findElement(soup,name,attrs,all=False):
    if all:
        text=list()
        elements = soup.findAll(name=name,attrs=attrs)
        for i in elements:
            text.append(i.get_text().strip().replace('\n',''))
    else:
        text = soup.find(name=name,attrs=attrs).get_text()
        text = text.strip().replace('\n','')
    return text
def save2json(soup):
    # 标题
    json = dict()
    # json["name"] = soup.find(name="h2", attrs={"class" :"m-b-sm"}).get_text()
    # json["categories"] = soup.find(name="div",attrs={"class":"categories"}).get_text()
    # json["score"] = soup.find(name="p",attrs={"class":"score"}).get_text()
    json["name"] =       findElement(soup,"h2",{"class" :"m-b-sm"})
    json["categories"] = findElement(soup,"div",{"class":"categories"})
    json["score"] =      findElement(soup,"p",{"class":"score"})
    json["info"] =       findElement(soup,"div",{"class":"info"},True)
    json["introduction"]=\
        soup.select("#detail > div:nth-child(1) > div > div > div.el-card__body > div > div.p-h.el-col.el-col-24.el-col-xs-16.el-col-sm-12 > div.drama > p")[0].get_text()
    print(json)
for i in range(PAGE):
    req = request.Request('https://antispider2.scrape.center/detail/'+ str(i+1))
    req.add_header('User-Agent',ua)
    res = request.urlopen(req)

    soup = BeautifulSoup(res)
    save2json(soup)