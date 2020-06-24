# -*- encoding=utf8 -*-

from myDriver import point, sel, myWebdriver, choiceSorter, choice
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from wechat_ftqq import sendWechat
from random import random
from time import sleep
from datetime import datetime
from selenium.webdriver.chrome.options import Options
import platform
import os


url_main = 'https://www.xuexi.cn/'

HEADLESS = False
LOGIN = True

ARTICLE = True
VIDEO = True
PROBLEM = True

SYSTEM = platform.system() 

print('Platform: {}, Headless: {}'.format(platform.machine(), HEADLESS))

today = str(datetime.today())
today_date = int(today[: 4] + today[5: 7] + today[8: 10])

if HEADLESS:
    print('Enable hedless browser')
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
else:
    chrome_options = Options()
    chrome_options.add_argument("--mute-audio")
    # mybrowser = myWebdriver()
    # mybrowser.maximize_window()

if SYSTEM == 'Windows':
    mybrowser = myWebdriver(chrome_options=chrome_options,
                        executable_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver")
else:
    mybrowser = myWebdriver(chrome_options=chrome_options,
                        executable_path="/usr/bin/chromedriver")
if LOGIN:
    mybrowser.login(HEADLESS)

while True:
    point = mybrowser.get_point(LOGIN)
    point.start = point.total
    msg = '每日登录：{}/1\t\n'.format(point.login)
    msg += '阅读文章：{}/6\t\n'.format(point.article_read)
    msg += '视听学习：{}/6\t\n'.format(point.video_watched)
    msg += '文章时长：{}/6\t\n'.format(point.article_time)
    msg += '视听时长：{}/6\t\n'.format(point.video_time)
    sendWechat('开始刷分。今日刷分：{}，当前总分：{}'.format(point.today(), point.total), msg)

    # 阅读文章
    if point.article_read + point.article_time < 12 and ARTICLE:
        mybrowser.wait_and_click(sel.PARTIAL_LINK, '学习理论')
        mybrowser.wait(sel.CLASS, 'text-wrap')
        articles = mybrowser.find_elements(By.CLASS_NAME, 'text-wrap')
        article_index_start = 0
        article_page = 0
        delay_per_step = 2
        delay_steps = 5
        action = ActionChains(mybrowser)
        action.key_down(Keys.ARROW_DOWN)
        action.key_up(Keys.ARROW_DOWN)
        while point.article_read < 6:
            if article_index_start < 20:
                if article_index_start == 0:
                    articles = mybrowser.find_elements(
                        By.CLASS_NAME, 'text-wrap')
                for _ in range(6 - point.article_read):
                    if article_index_start < len(articles):
                        article = articles[article_index_start]
                        article_index_start += 1
                        sleep(random() * 2)
                        article.click()
                        mybrowser.switch_to_last_window()
                        mybrowser.auto_read(
                            article_page, article_index_start, action, delay_steps, delay_per_step)
                        mybrowser.close_and_switch_to_last_window()
                    else:
                        break
                sleep(random() * 2)
                articles[0].click()
                mybrowser.switch_to_last_window()
                point = mybrowser.get_point(LOGIN)
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
            delay_steps = 6 * (6 - point.article_time)
            delay_per_step = 20
            mybrowser.auto_read(article_page, 0, action,
                                delay_steps, delay_per_step)
            point = mybrowser.get_point(LOGIN)

    # 观看视频
    if point.video_watched < 6 and VIDEO:
        while len(mybrowser.window_handles) > 1:
            mybrowser.close_and_switch_to_last_window()
        mybrowser.get(url_main)
        sleep(5)
        mybrowser.wait_and_click(sel.PARTIAL_LINK, '学习电视台')
        sleep(random() * 2)
        mybrowser.wait_and_click(
            sel.XPATH, '//*[@id="495f"]/div/div/div/div/div/section/div/div/div/div[1]/div[1]/div/div')
        sleep(random() * 2)
        video_lists = mybrowser.find_elements_by_class_name('_30AOPZ5kxkMqnxVwziYb3o')[11: 14]
        for video_list in video_lists:
            if point.video_watched == 6:
                break
            else:
                sleep(random())
                video_list.click()
                mybrowser.wait_and_click(sel.CLASS, 'list')
                mybrowser.wait(sel.CLASS, '_3wnLIRcEni99IWb4rSpguK')
                videos = mybrowser.find_elements_by_class_name('_3wnLIRcEni99IWb4rSpguK')
                
                videos_to_read = []
                for video in videos:
                    video_date = int(video.text[-10: -6] + video.text[-5: -3] + video.text[-2: ])
                    if today_date - video_date < 2:
                        videos_to_read.append(video)

                num_videos_to_read = min(6 - point.video_watched, len(videos_to_read))
                for video in videos_to_read[: num_videos_to_read]:
                    video_title = video.text[: -11]
                    video_date = int(video.text[-10: -6] + video.text[-5: -3] + video.text[-2: ])
                    video.click()
                    mybrowser.switch_to_last_window()
                    watch_time = 15 + random() * 3
                    print('[{}] Watching video, title = {}, date = {}, time = {}s'.format(
                            datetime.now(), video_title, video_date, watch_time))
                    sleep(watch_time)
                    # if DEBUG:
                    #     path_screenshot = os.path.join(os.getcwd(), 'screenshot.png')
                    #     print('Saving screenshot to {}'.format(path_screenshot))
                    #     mybrowser.get_screenshot_as_file(path_screenshot)
                    mybrowser.close_and_switch_to_last_window()
                if num_videos_to_read:
                    video.click()
                    mybrowser.switch_to_last_window()
                    point = mybrowser.get_point(LOGIN)
                    mybrowser.close_and_switch_to_last_window()
    if point.video_time < 6 and VIDEO:
        print('[{}] Watching video for time ...'.format(datetime.now()))
        sleep(random() * 2)
        mybrowser.wait_and_click(
            sel.XPATH, '//*[@id="0454"]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[5]/div/div')
        sleep(random() * 2)
        mybrowser.wait_and_click(sel.CLASS, 'innerPic')
        # if not HEADLESS:
        #     mybrowser.wait_for_video_and_mute()
        sleep((6 - point.video_time) * 250)
        point = mybrowser.get_point(LOGIN)
        mybrowser.close_and_switch_to_last_window()
        mybrowser.close_and_switch_to_last_window()
        mybrowser.close_and_switch_to_last_window()

    # 刷题
    if point.daily_problem == 0 and PROBLEM:
        mybrowser.wait_and_click(sel.XPATH, '//*[@id="root"]/div/div/section/div/div/div/div/div[4]/section/div[4]')
        mybrowser.wait_and_click(sel.XPATH, '//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[6]/div[2]/div[2]/div')
        for question_index in range(10):
            while int(mybrowser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/span').text) != question_index + 1: pass
            mybrowser.wait(sel.CLASS, 'q-header')
            q_header = mybrowser.find_element_by_class_name('q-header')
            question_tpye = q_header.text
            print('Answering questions, index: {}, type: {}'.format(question_index, question_tpye))

            if question_tpye == '多选题':
                choices = mybrowser.find_elements_by_class_name('q-answers')
                choices_raw = mybrowser.find_element_by_class_name('q-answers').text
                choices = choiceSorter().sort(choices_raw)
                for choice in choices:
                    mybrowser.wait_and_click(sel.XPATH, '//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[4]/div[' + str(choice.index) + ']')
                    sleep(random())
            elif question_tpye == '单选题':
                mybrowser.wait_and_click(sel.XPATH, '//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[3]/span')
                mybrowser.wait(sel.XPATH, '//*[@id="body-body"]/div[4]/div/div/div/div[2]/div/div/div/font')
                red = mybrowser.find_element_by_xpath('//*[@id="body-body"]/div[4]/div/div/div/div[2]/div/div/div/font')
                mybrowser.wait_and_click(sel.XPATH, '//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[3]/span')
                choices_raw = mybrowser.find_element_by_class_name('q-answers').text
                choices = choiceSorter().sort(choices_raw)
                CHOICE_MATCHED = False
                for choice in choices:
                    if choice.text == red.text:
                        mybrowser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[4]/div[' + str(choice.index) + ']').click()
                        CHOICE_MATCHED = True
                        break
                if not CHOICE_MATCHED or red.text == '':
                    XPATH_C = '//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[4]/div[' + '1' + ']'
                    mybrowser.find_element_by_xpath(XPATH_C).click()
                    sleep(random())
                # mybrowser.wait_and_click(sel.XPATH, '//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[3]/span')
                # A_XPATH = '//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[4]/div[1]'
                # B_XPATH = '//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[4]/div[2]'
            elif question_tpye == '填空题':
                blanks = mybrowser.find_elements_by_class_name('blank')
                sleep(random())
                mybrowser.wait_and_click(sel.XPATH, '//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[3]/span')
                # mybrowser.wait_and_click(sel.XPATH, '//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[4]/span')
                mybrowser.wait(sel.XPATH, '//*[@id="body-body"]/div[4]/div/div/div/div[2]/div/div/div/font')
                sleep(random())
                tip = mybrowser.find_element_by_xpath('//*[@id="body-body"]/div[4]/div/div/div/div[2]/div/div/div').text    
                reds = mybrowser.find_elements_by_xpath('//*[@id="body-body"]/div[4]/div/div/div/div[2]/div/div/div/font')
                sleep(random())
                mybrowser.wait_and_click(sel.XPATH, '//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[3]/span')
                # mybrowser.wait_and_click(sel.XPATH, '//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[4]/span')
                for blank_index in range(len(blanks)):
                    if tip == '请观看视频':
                        blanks[blank_index].send_keys('123')
                    else:
                        blanks[blank_index].send_keys(reds[blank_index].text)
                        print('Answer: ' + reds[blank_index].text)
                    sleep(random())
                sleep(random())
            mybrowser.wait_and_click(sel.XPATH, '//*[@id="app"]/div/div[2]/div/div[4]/div[2]/button')
            sleep(1 + random())
            solution = mybrowser.find_elements_by_class_name('solution')
            if solution:
                mybrowser.wait_and_click(sel.XPATH, '//*[@id="app"]/div/div[2]/div/div[4]/div[2]/button')

    XX_hour = int(random() * 3) + 9
    XX_minute = int(random() * 60)
    point = mybrowser.get_point(LOGIN)
    mybrowser.close_all_and_leave_main()
    print('[{}] 刷分完成'.format(datetime.now()))
    msg = '每日登录：{}/1\t\n'.format(point.login)
    msg += '阅读文章：{}/6\t\n'.format(point.article_read)
    msg += '视听学习：{}/6\t\n'.format(point.video_watched)
    msg += '文章时长：{}/6\t\n'.format(point.article_time)
    msg += '视听时长：{}/6\t\n'.format(point.video_time)
    msg += '明天刷分时间：{}：{}\t\n'.format(XX_hour, XX_minute)
    sendWechat('刷分完成。今日刷分：{}，当前总分：{}，本次刷分：{}'.format(
        point.today(), point.total, point.total - point.start), msg)

    today = datetime.now()
    print('Waiting for a new day ...')
    while today.day == datetime.now().day:
        sleep(300 + random() * 300)
        mybrowser.get_point(LOGIN)
        # sendWechat('Waiting ...')
    today = datetime.now()
    print('Waiting for learning at {}:{} ...'.format(XX_hour, XX_minute))
    while today.hour < XX_hour or today.minute < XX_minute:
        sleep(600 + random() * 60)
        mybrowser.get_point(LOGIN)
        # sendWechat('Waiting ...')
        today = datetime.now()
