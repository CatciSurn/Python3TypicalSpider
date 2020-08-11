# 案例2：反爬电影网站

# 特点
对接User-Agent反爬，检测到爬虫UA就拒绝响应403
# 其他
案例中的第一种方法用到了崔庆才老师的gerapy-item-pipeline模块，已在requirement.txt标出
第二种方法（thother.py）使用的是 webdriver + js嵌入 实现的脚本