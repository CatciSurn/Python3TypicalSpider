# -*- coding: utf-8 -*-
import scrapy
from example.items import ThotherItem

from selenium import webdriver
import time

class ThotherSpider(scrapy.Spider):
    name = 'thother'
    allowed_domains = ['antispider1.scrape.center']
    base_url = 'https://antispider1.scrape.center'

    def __init__(self):
        self.main()


    def main(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=options, executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })
        """
        })
        driver.get('https://antispider1.scrape.center/')
        time.sleep(3)
