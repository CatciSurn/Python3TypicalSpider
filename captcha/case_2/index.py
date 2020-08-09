import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from chaojiying import Chaojiying
import os

USERNAME = 'admin'
PASSWORD = 'admin'

CHAOJIYING_USERNAME = os.getenv('CHAOJIYING_USERNAME')
CHAOJIYING_PASSWORD = os.getenv('CHAOJIYING_PASSWORD')
CHAOJIYING_SOFT_ID = 893590
CHAOJIYING_KIND = 9004

if not CHAOJIYING_USERNAME or not CHAOJIYING_PASSWORD:
    print('请设置用户名和密码')
    exit(0)


class CrackCaptcha():
    def __init__(self):
        self.url = 'https://captcha2.scrape.cuiqingcai.com/'
        self.browser = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        self.wait = WebDriverWait(self.browser, 20)
        self.username = USERNAME
        self.password = PASSWORD
        self.chaojiying = Chaojiying(CHAOJIYING_USERNAME, CHAOJIYING_PASSWORD, CHAOJIYING_SOFT_ID)
    
    def __del__(self):
        self.browser.close()
    
    def open(self):
        """
        打开网页输入用户名密码
        :return: None
        """
        self.browser.get(self.url)
        # 填入用户名密码
        username = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"]')))
        password = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]')))
        username.send_keys(self.username)
        password.send_keys(self.password)
    
    def get_captcha_button(self):
        """
        获取初始验证按钮
        :return:
        """
        button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="button"]')))
        return button
    
    def get_captcha_element(self):
        """
        获取验证图片对象
        :return: 图片对象
        """
        # 验证码图片加载出来
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.geetest_item_img')))
        # 验证码完整节点
        element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_panel_box')))
        print('成功获取验证码节点')
        return element
    
    def get_captcha_position(self):
        """
        获取验证码位置
        :return: 验证码位置元组
        """
        element = self.get_captcha_element()
        time.sleep(2)
        location = element.location
        size = element.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        return (top, bottom, left, right)
    
    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        screenshot.save('case_2/img/screenshot.png')
        return screenshot
    
    def get_captcha_image(self, name='case_2/img/captcha.png'):
        """
        获取验证码图片
        :return: 图片对象
        """
        top, bottom, left, right = self.get_captcha_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha
    
    def get_points(self, captcha_result):
        """
        解析识别结果
        :param captcha_result: 识别结果
        :return: 转化后的结果
        """
        groups = captcha_result.get('pic_str').split('|')
        locations = [[int(number) for number in group.split(',')] for group in groups]
        return locations
    
    def touch_click_words(self, locations):
        """
        点击验证图片
        :param locations: 点击位置
        :return: None
        """
        for location in locations:
            ActionChains(self.browser).move_to_element_with_offset(self.get_captcha_element(), location[0],
                                                                   location[1]).click().perform()
            time.sleep(1)
    
    def touch_click_verify(self):
        """
        点击验证按钮
        :return: None
        """
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_commit')))
        button.click()
    
    def crack(self):
        """
        破解入口
        :return: None
        """
        self.open()
        time.sleep(5)
        # 点击验证按钮
        button = self.get_captcha_button()
        button.click()
        # 获取验证码图片
        image = self.get_captcha_image()
        bytes_array = BytesIO()
        image.save(bytes_array, format='PNG')
        # 识别验证码
        result = self.chaojiying.post_pic(bytes_array.getvalue(), CHAOJIYING_KIND)
        print(result)
        locations = self.get_points(result)
        self.touch_click_words(locations)
        self.touch_click_verify()
        # 登录失败
        self.chaojiying.report_error(result.get('pic_id'))
        print('登录过程中出现错误')
        # 判定是否成功
        success = self.wait.until(
            EC.text_to_be_present_in_element((By.TAG_NAME, 'h2'), '登录成功'))
        time.sleep(5)
        if success:
            print('登录成功！')


if __name__ == '__main__':
    crack = CrackCaptcha()
    crack.crack()