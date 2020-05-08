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

url_main = 'https://www.xuexi.cn/'

class point():
    start, total, login, article_read, video_watched, article_time, video_time = 0, 0, 0, 0, 0, 0, 0
    def today(self):
        p = self.login
        p = self.login + self.article_read + self.article_time + self.video_watched + self.video_time
        return p

class sel():
    XPATH = 1
    CSS = 2
    CLASS = 3
    PARTIAL_LINK = 4

class myWebdriver(webdriver.Chrome):
    def wait_for_video_and_mute(self):
        video = self.find_element_by_css_selector("video")
        self.execute_script("arguments[0].muted = true;", video)
        
    def switch_to_last_window(self):
        self.switch_to_window(self.window_handles[-1])

    def close_and_switch_to_last_window(self):
        self.close()
        self.switch_to_window(self.window_handles[-1])

    def close_all(self):
        self.switch_to_last_window()
        if self.current_window_handle != self.window_handles[0]:
            self.close_and_switch_to_last_window()
        else:
            self.close()

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

    
    def login(self):
        print('Logging ...')
        self.get(url_main)
        self.wait_and_click(sel.CSS, '.login-icon')
        self.switch_to_last_window()
        self.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        self.wait(sel.XPATH, '//*[@id="ddlogin-iframe"]')
        url_QR = self.find_element(By.XPATH,  '//*[@id="ddlogin-iframe"]')
        login_QR = url_QR.screenshot('./login_QR.png')
        while self.current_url != url_main: pass
        self.close_and_switch_to_last_window()

    def get_point(self):
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
        points.total = int(element.text)
        pointCards = self.find_elements(By.CLASS_NAME, 'my-points-card-text')
        [points.login, point.article_read, points.video_watched, points.article_time, points.video_time] = [int(i.text[0]) for i in pointCards]
        self.close_and_switch_to_last_window()
        return points

    def auto_read(self, articlr_page, article_index, action, delay_steps, delay_per_step):
        print('[{}] Reading article, page = {}, index = {}'.format(datetime.now(), articlr_page, article_index))
        for _ in range(delay_steps):
            action.perform()
            sleep(delay_per_step + random())