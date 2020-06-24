# -*- encoding=utf8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from wechat_ftqq import sendWechat
from random import random
from time import sleep
from datetime import datetime
import os
import platform
import re

url_main = 'https://www.xuexi.cn/'

class point():
    start, total, login, article_read, video_watched, article_time, video_time, daily_problem = 0, 0, 0, 0, 0, 0, 0, 0
    def today(self):
        p = self.login
        p = self.login + self.article_read + self.article_time + self.video_watched + self.video_time + self.daily_problem
        return p

class sel():
    XPATH = 1
    CSS = 2
    CLASS = 3
    PARTIAL_LINK = 4

class choice():
    index = 0
    text = ''
    def __init__(self, _index, _text):
        # A的ASCII为65
        self.index = ord(_index) - 64
        self.text = _text

class choiceSorter():
    # 'A. 大禹\nB. 孙叔敖\nC. 西门豹\nD. 史禄'
    def sort(self, raw_text):
        # reg = '[A-Z]. [\u4e00-\u9fa5]*'
        reg = '[A-Z]. [^\\n]*'
        choices_text = re.findall(reg, raw_text)
        choices = []
        print(raw_text)
        for choice_text in choices_text:
            index = choice_text[0]
            text = choice_text[3: ]
            choices.append(choice(index, text))
        return choices




class myWebdriver(webdriver.Chrome):
    def wait_for_video_and_mute(self):
        video = self.find_element_by_css_selector("video")
        self.execute_script("arguments[0].muted = true;", video)
        
    def switch_to_last_window(self):
        self.switch_to_window(self.window_handles[-1])

    def close_and_switch_to_last_window(self):
        self.close()
        self.switch_to_window(self.window_handles[-1])

    def close_all_and_leave_main(self):
        self.switch_to_last_window()
        while self.current_window_handle != self.window_handles[0]:
            self.close_and_switch_to_last_window()

    def match_selector(self, selector):
        if selector == sel.CSS:
            By_sel = By.CSS_SELECTOR
        elif selector == sel.XPATH:
            By_sel = By.XPATH
        elif selector == sel.PARTIAL_LINK:
            By_sel = By.PARTIAL_LINK_TEXT
        elif selector == sel.CLASS:
            By_sel = By.CLASS_NAME
        return By_sel

    def wait_and_click(self, selector, location):
        s = self.match_selector(selector)
        element = WebDriverWait(self, 60).until(EC.presence_of_element_located((s, location)))
        element.click()
        self.switch_to_window(self.window_handles[-1])

    def wait(self, selector, location):
        s = self.match_selector(selector)
        WebDriverWait(self, 60).until(EC.presence_of_element_located((s, location)))

    def open_new_page(self):
        self.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't') 
 
    def login(self, HEADLESS):
        QR_XPATH = '//*[@id="ddlogin-iframe"]'
        print('Getting login page ...')
        self.get(url_main)
        self.wait_and_click(sel.CSS, '.login-icon')
        self.switch_to_last_window()
        self.wait(sel.XPATH, QR_XPATH)
        self.execute_script("arguments[0].scrollIntoView();", self.find_element(By.XPATH, QR_XPATH))
        sleep(1)
        url_QR = self.find_element(By.XPATH,  QR_XPATH)
        url_QR.screenshot('./login_QR.png')
        print('Save QR code to {}'.format(os.path.join(os.getcwd(), 'login_QR.png')))
        if HEADLESS:
            if platform.system() == 'Windows':
                os.startfile(os.path.join(os.getcwd(), 'login_QR.png'))
        while self.current_url != url_main: pass
        self.close_and_switch_to_last_window()

    def get_point(self, LOGIN):
        if LOGIN:
            print('[{}] Checking point ...'.format(datetime.now()))
            if self.current_url != url_main:
                self.get(url_main)
                self.switch_to_last_window()
            self.wait_and_click(sel.XPATH, '//*[@id="root"]/div/div/section/div/div/div/div/div[4]/section/div[4]')
            self.switch_to_last_window()
            self.wait(sel.XPATH, '//*[@id="app"]/div/div[2]/div/div[2]/div[2]/span[1]')
            sleep(1)
            element = self.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[2]/div[2]/span[1]')
            points = point()
            if element.text:
                points.total = int(element.text)
            pointCards = self.find_elements(By.CLASS_NAME, 'my-points-card-text')
            [points.login, points.article_read, points.video_watched, points.article_time, points.video_time, point.daily_problem] = [int(i.text[0]) for i in pointCards[: 6]]
            self.close_and_switch_to_last_window()
            msg = '每日登录：{}/1\t\n'.format(points.login)
            msg += '阅读文章：{}/6\t\n'.format(points.article_read)
            msg += '视听学习：{}/6\t\n'.format(points.video_watched)
            msg += '文章时长：{}/6\t\n'.format(points.article_time)
            msg += '视听时长：{}/6\t\n'.format(points.video_time)
            print(msg)
        else:
            points = point()
        return points

    def auto_read(self, articlr_page, article_index, action, delay_steps, delay_per_step):
        print('[{}] Reading article, page = {}, index = {}'.format(datetime.now(), articlr_page, article_index))
        for _ in range(delay_steps):
            action.perform()
            if random() < 0.3:
                sleep(random() / 5)
                action.perform()
            sleep(delay_per_step + random())