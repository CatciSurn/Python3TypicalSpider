# 案例1：反爬电影网站

# 特点
对接Webdriver反爬，检测到Webdriver就不显示页面(Webdriver Forbi)
# 其他
案例中的第一种方法用到了崔庆才老师的gerapy-item-pipeline模块，已在requirement.txt标出
第二种方法（thother.py）使用的是 webdriver + js嵌入 实现的脚本
## Usage

```
pip3 install -r requirements.txt
scrapy crawl movie
```
或
```
scrapy crawl thother
```