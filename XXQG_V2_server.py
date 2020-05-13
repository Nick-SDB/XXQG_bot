# -*- encoding=utf8 -*-

from myDriver import point, sel, myWebdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from wechat_ftqq import sendWechat
from random import random
from time import sleep
from datetime import datetime
from selenium.webdriver.chrome.options import Options
import platform


url_main = 'https://www.xuexi.cn/'

if platform.machine() not in ['x86_64', 'AMD64']:
    HEADLESS = True
    print('Enable hedless browser')
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("window-size=1024,768")
    chrome_options.add_argument("--no-sandbox")
    mybrowser = myWebdriver(chrome_options=chrome_options, executable_path="/usr/bin/chromedriver")
else:
    HEADLESS = False
    mybrowser = myWebdriver()

# mybrowser = myWebdriver(chrome_options=chrome_options, executable_path="/usr/bin/chromedriver")
mybrowser.maximize_window()
mybrowser.login()

while True:
    point = mybrowser.get_point()
    point.start = point.total
    msg = '每日登录：{}/1\t\n'.format(point.login)
    msg += '阅读文章：{}/6\t\n'.format(point.article_read)
    msg += '视听学习：{}/6\t\n'.format(point.video_watched)
    msg += '文章时长：{}/6\t\n'.format(point.article_time)
    msg += '视听时长：{}/6\t\n'.format(point.video_time)
    sendWechat('开始刷分。今日刷分：{}，当前总分：{}'.format(point.today(), point.total), msg)

    # 阅读文章
    if point.article_read + point.article_time < 12:
        mybrowser.wait_and_click(sel.PARTIAL_LINK, '学习理论')
        mybrowser.wait(sel.CLASS, 'text-wrap')
        articles = mybrowser.find_elements(By.CLASS_NAME, 'text-wrap')
        article_index_start = 0
        article_page = 0
        delay_per_step = 1
        delay_steps = 5
        action = ActionChains(mybrowser)
        action.key_down(Keys.ARROW_DOWN)
        action.key_up(Keys.ARROW_DOWN)
        while point.article_read < 6:
            if article_index_start < 20:
                if article_index_start == 0:
                    articles = mybrowser.find_elements(By.CLASS_NAME, 'text-wrap')
                for _ in range(6 - point.article_read):
                    if article_index_start < len(articles): 
                        article = articles[article_index_start]
                        article_index_start += 1
                        sleep(random() * 2)
                        article.click()
                        mybrowser.switch_to_last_window()
                        mybrowser.auto_read(article_page, article_index_start, action, delay_steps, delay_per_step)
                        mybrowser.close_and_switch_to_last_window()
                    else:
                        break
                sleep(random() * 2)
                articles[0].click()
                mybrowser.switch_to_last_window()
                point = mybrowser.get_point()
                mybrowser.close_and_switch_to_last_window()
            else:
                btns = mybrowser.find_elements(By.CLASS_NAME, 'btn')
                for btn in btns:
                    if btn.text == '>>':
                        sleep(random() * 2)
                        btn.click()
                article_index_start = 0
                article_page += 1
        while point.article_time < 6:
            print('[{}] Reading article for time ...'.format(datetime.now()))
            sleep(random() * 2)
            articles[0].click()
            mybrowser.switch_to_last_window()
            delay_steps = 6 * (6 - point.video_time)
            delay_per_step = 20
            mybrowser.auto_read(article_page, 0, action, delay_steps, delay_per_step)
            point = mybrowser.get_point()

    # 观看视频
    if point.video_watched + point.video_time < 12:
        while len(mybrowser.window_handles) > 1:
            mybrowser.close_and_switch_to_last_window()
        mybrowser.get(url_main)
        sleep(5)
        mybrowser.wait_and_click(sel.PARTIAL_LINK, '学习电视台')
        sleep(random() * 2)
        mybrowser.wait_and_click(sel.XPATH, '//*[@id="495f"]/div/div/div/div/div/section/div/div/div/div[1]/div[1]/div/div')
        sleep(random() * 2)
        mybrowser.wait_and_click(sel.XPATH, '//*[@id="0454"]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/div/div')
        mybrowser.wait(sel.CLASS, 'innerPic')
        video_index_start = 0
        video_page = 0
        while point.video_watched < 6:
            if video_index_start < 20:
                if video_index_start == 0:
                    videos = mybrowser.find_elements(By.CLASS_NAME, 'innerPic')
                for _ in range(6 - point.video_watched):
                    if video_index_start < len(videos): 
                        video = videos[video_index_start]
                        video_index_start += 1
                        sleep(random() * 2)
                        video.click()
                        mybrowser.switch_to_last_window()
                        # if not HEADLESS:    
                        #     mybrowser.wait_for_video_and_mute()
                        watch_time = 30 + random() * 3
                        print('[{}] Watching video, page = {}, index = {}, time = {}s'.format(datetime.now(), video_page, video_index_start, watch_time))
                        sleep(watch_time)
                        mybrowser.close_and_switch_to_last_window()
                    else:
                        break
                video = videos[0]
                sleep(random() * 2)
                video.click()
                mybrowser.switch_to_last_window()
                point = mybrowser.get_point()
                mybrowser.close_and_switch_to_last_window()
            else:
                btns = mybrowser.find_elements(By.CLASS_NAME, 'btn')
                for i in btns:
                    if i.text == '>>':
                        sleep(random() * 2)
                        i.click()
                        video_index_start = 0
                        video_page += 1
                        break
        while point.video_time < 6:
            print('[{}] Watching video for time ...'.format(datetime.now()))
            sleep(random() * 2)
            mybrowser.wait_and_click(sel.XPATH, '//*[@id="0454"]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[5]/div/div')
            sleep(random() * 2)
            mybrowser.wait_and_click(sel.CLASS, 'innerPic')
            # if not HEADLESS:
            #     mybrowser.wait_for_video_and_mute()
            sleep((6 - point.video_time) * 250)
            point = mybrowser.get_point()
            mybrowser.close_and_switch_to_last_window()

    XX_hour = int(random() * 3) + 9
    XX_minute = int(random() * 60)
    point = mybrowser.get_point()
    mybrowser.close_all_and_leave_main()
    print('[{}] 刷分完成'.format(datetime.now()))
    msg = '每日登录：{}/1\t\n'.format(point.login)
    msg += '阅读文章：{}/6\t\n'.format(point.article_read)
    msg += '视听学习：{}/6\t\n'.format(point.video_watched)
    msg += '文章时长：{}/6\t\n'.format(point.article_time)
    msg += '视听时长：{}/6\t\n'.format(point.video_time)
    msg += '明天刷分时间：{}：{}\t\n'.format(XX_hour, XX_minute)
    sendWechat('刷分完成。今日刷分：{}，当前总分：{}，本次刷分：{}'.format(point.today(), point.total, point.total - point.start), msg)

    today = datetime.now()
    print('Waiting for a new day ...')
    while today.day == datetime.now().day:
        sleep(300 + random() * 300)
        mybrowser.get_point()
        sendWechat('Waiting ...')
    today = datetime.now()
    print('Waiting for learn at {}:{} ...'.format(XX_hour, XX_minute))
    while today.hour < XX_hour or today.minute < XX_minute:
        sleep(300 + random() * 300)
        mybrowser.get_point()
        sendWechat('Waiting ...')
        today = datetime.now()