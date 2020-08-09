from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait

driver=webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

driver.get('https://login1.scrape.center/')
time.sleep(3)

driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div/div/div/form/div[1]/div/div/input').send_keys("admin")
driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div/div/div/form/div[2]/div/div/input').send_keys("admin")
driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div/div/div/form/div[3]/div/button').click()
time.sleep(2)