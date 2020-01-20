# coding: utf-8

import sys
import json
import os.path
import datetime
from pickle import dump, load
from time import sleep, time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AutoTicket:
    def __init__(self, period, price, date, real_name, nick_name, ticket_num, damai_url, target_url, browser):
        self.period = period # 场次序号优先级
        self.price = price  # 票价序号优先级
        self.date = date    # 日期选择
        self.real_name = real_name  # 实名者序号
        self.status = 0  # 状态标记
        self.time_start = 0  # 开始时间
        self.time_end = 0  # 结束时间
        self.num = 0  # 尝试次数
        self.type = 0  # 目标购票网址类别
        self.ticket_num = ticket_num  # 购买票数
        self.nick_name = nick_name  # 用户昵称
        self.damai_url = damai_url  # 大麦网官网网址
        self.target_url = target_url  # 目标购票网址
        self.browser = browser # 0代表Chrome，1代表Firefox，默认为Chrome
        self.total_wait_time = 3 # 页面元素加载总等待时间
        self.refresh_wait_time = 0.3 # 页面元素等待刷新时间
        self.intersect_wait_time = 0.5 # 间隔等待时间，防止速度过快导致问题

        if self.target_url.find("detail.damai.cn") != -1:
            self.type = 1
        elif self.target_url.find("piao.damai.cn") != -1:
            self.type = 2
        else:
            self.type = 0
            raise Exception("***Error:Unsupported Target Url Format:{}***".format(self.target_url))
            self.driver.quit()

    def get_cookie(self):
        self.driver.get(self.damai_url)
        print("###请点击登录###")
        while self.driver.title.find('大麦网-全球演出赛事官方购票平台') != -1:  # 等待网页加载完成
            sleep(1)
        print("###请扫码登录###")
        while self.driver.title == '大麦登录':  # 等待扫码完成
            sleep(1)
        dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
        print("###Cookie保存成功###")

    def set_cookie(self):
        try:
            cookies = load(open("cookies.pkl", "rb"))  # 载入cookie
            for cookie in cookies:
                cookie_dict = {
                    'domain': '.damai.cn',  # 必须有，不然就是假登录
                    'name': cookie.get('name'),
                    'value': cookie.get('value'),
                    "expires": "",
                    'path': '/',
                    'httpOnly': False,
                    'HostOnly': False,
                    'Secure': False}
                self.driver.add_cookie(cookie_dict)
            print('###载入Cookie###')
        except Exception as e:
            print(e)

    def login(self):
        if not os.path.exists('cookies.pkl'):  # 如果不存在cookie.pkl,就获取一下
            if self.browser == 0: # 选择了Chrome浏览器
                self.driver = webdriver.Chrome()
            elif self.browser == 1: # 选择了Firefox浏览器
                self.driver = webdriver.Firefox()
            else:
                raise Exception("***错误：未知的浏览器类别***")
            self.get_cookie()
            self.driver.quit()
        print('###打开浏览器，进入大麦网###')
        if self.browser == 0: # 选择了Chrome浏览器，并成功加载cookie，设置不载入图片，提高刷新效率
            options = webdriver.ChromeOptions()
            prefs = {"profile.managed_default_content_settings.images":2}
            options.add_experimental_option("prefs",prefs)
            self.driver = webdriver.Chrome(options=options)
        elif self.browser == 1: # 选择了火狐浏览器
            options = webdriver.FirefoxProfile()
            options.set_preference('permissions.default.image', 2)  
            self.driver = webdriver.Firefox(options)
        else: 
            raise Exception("***错误：未知的浏览器类别***")
        self.driver.get(self.target_url)
        self.set_cookie()
        # self.driver.maximize_window()
        self.driver.refresh()

    def enter_concert(self):
        self.login()
        try:
            if self.type == 1:  # detail.damai.cn
                locator = (By.XPATH, "/html/body/div[1]/div/div[3]/div[1]/a[2]/div")
            elif self.type == 2:  # piao.damai.cn
                locator = (By.XPATH, "/html/body/div[1]/div/ul/li[2]/div/label/a[2]")
            WebDriverWait(self.driver, self.total_wait_time, self.refresh_wait_time).until(
                EC.text_to_be_present_in_element(locator, self.nick_name))
            self.status = 1
            print("###登录成功###")
        except Exception as e:
            print(e)
            self.status = 0
            raise Exception("***错误：登录失败,请检查配置文件昵称或删除cookie.pkl后重试***")
            self.driver.quit()

if __name__ == '__main__':
    # startTime = datetime.datetime(2019, 11, 29, 10, 14, 30)  #定时功能：2019-9-25 09:17:07秒开抢
    # print('抢票程序还未开始...')
    # while datetime.datetime.now() < startTime:
    #     sleep(1)
    # print('开始进入抢票 %s' % startTime)
    # print('正在执行...')

    script = os.path.abspath(sys.argv[0])
    target = os.path.dirname(script)
    os.chdir(target)
    print(script, target, os.path.abspath(os.curdir))

    try:
        with open('config.json', 'r', encoding='utf-8') as f:
                    config = json.loads(f.read())
                # params: 场次优先级，票价优先级，日期， 实名者序号, 用户昵称， 购买票数， 官网网址， 目标网址， 浏览器
        con = AutoTicket(config['sess'], config['price'], config['date'], config['real_name'], config['nick_name'], config['ticket_num'],
                      config['damai_url'], config['target_url'], config['browser'])
    except Exception as e:
        print(e)
        raise Exception("***错误：初始化失败，请检查配置文件***")

    con.enter_concert();