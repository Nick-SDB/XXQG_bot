from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from random import random

url_main = 'https://www.xuexi.cn/'
url_login = 'https://pc.xuexi.cn/points/login.html?ref=https%3A%2F%2Fwww.xuexi.cn%2F'

xpath_btn_points = '//*[@id="root"]/div/div/section/div/div/div/div/div[4]/section/div[4]'
xpath_points = '//*[@id="app"]/div/div[2]/div/div[2]/div[2]/span[1]'
xpath_ZHXW = '//*[@id="4d3a"]/div/div/div/div/div/section/div/div/div/div/div[1]/div/div/div[2]/span'
xpath_articleHead = '//*[@id="root"]/div/div/section/div/div/div/div/div/section/div/div/div/div[1]/div/section/div/div/div/div/div/section/div/div/div/div/div[3]/section/div/div/div/div/div/section/div/div/div[1]/div/div['
xpath_articleTail = ']/div/div/div[1]/span'

browser = webdriver.Chrome()
browser.maximize_window()

# 登录，获取学习积分
browser.get(url_login)
browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
while browser.current_url != url_main: pass
time.sleep(3)
browser.find_element(By.XPATH, xpath_btn_points).click()
browser.switch_to_window(browser.window_handles[-1])
points = int(browser.find_element(By.CLASS_NAME, 'my-points-points.my-points-red').text)
print('当前分数：' + str(points))
browser.close()

# 浏览6篇文章
browser.switch_to_window(browser.window_handles[-1])
browser.get(url_main)
time.sleep(1)
browser.find_element(By.LINK_TEXT, '学习理论').click()
for i in range(6):
    # 打开文章
    browser.switch_to_window(browser.window_handles[-1])
    xpath = xpath_articleHead + str(i + 7) + xpath_articleTail
    browser.find_element(By.XPATH, xpath).click()
    browser.switch_to_window(browser.window_handles[-1])
    # 模拟随机滚动
    action = ActionChains(browser)
    if i != 5:
        for _ in range(5):
            action.key_down(Keys.ARROW_DOWN)
            action.key_up(Keys.ARROW_DOWN)
            action.perform()
            time.sleep(1 + random())
    else:
        for _ in range(20):
            action.key_down(Keys.ARROW_DOWN)
            action.key_up(Keys.ARROW_DOWN)
            action.perform()
            time.sleep(36 + random())
    browser.close()

# 播放6个视频
xpath_DYPD = '//*[@id="9309"]/div/div/div/div/div/div/div/div[1]/div/div[1]/div/div'
xpath_XXZDBD = '//*[@id="0454"]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/div/div'
xpath_XXZDBD_LB = '//*[@id="1koo357ronk-5"]/div/div/div/div/div/div/section/div[1]/span[2]'
xpath_XWLB = '//*[@id="0454"]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[5]/div/div'
xpath_XWLB_LB = '//*[@id="17th9fq5c7l-5"]/div/div/div/div/div/div/section/div[1]/span[2]'
xpath_video_base = '//*[@id="1koo357ronk-5"]/div/div/div/div/div/div/section/div[3]/section/div/div/div[1]/div['
xpath_XWLB_0 = '//*[@id="17th9fq5c7l-5"]/div/div/div/div/div/div/section/div[3]/section/div/div/div[1]/div[1]/div[1]/div/div/div[1]'

browser.switch_to_window(browser.window_handles[-1])
browser.get(url_main)
time.sleep(5)
browser.find_element(By.XPATH, xpath_DYPD).click()
browser.switch_to_window(browser.window_handles[-1])
time.sleep(5)
browser.find_element(By.XPATH, xpath_XXZDBD).click()
browser.find_element(By.XPATH, xpath_XXZDBD_LB).click()
for i in range(6):
    time.sleep(2)
    xpath_base = xpath_video_base + str(i + 1) + ']/div['
    for j in range(2):
        xpath = xpath_base + str(j + 1) + ']/div/div/div[1]'
        browser.find_element(By.XPATH, xpath).click()
        browser.switch_to_window(browser.window_handles[-1])
        time.sleep(5 + random())
        browser.close()
        browser.switch_to_window(browser.window_handles[-1])
time.sleep(1)
browser.find_element(By.XPATH, xpath_XWLB).click()
time.sleep(1)
browser.find_element(By.XPATH, xpath_XWLB_LB).click()
time.sleep(1)
browser.find_element(By.XPATH, xpath_XWLB_0).click()
time.sleep(1100)


for window in browser.window_handles:
    browser.switch_to_window(window)
    browser.close()