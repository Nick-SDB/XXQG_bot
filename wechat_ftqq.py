#!/usr/bin/env python
# -*- encoding=utf8 -*-
import datetime
import json

import requests

def sendWechat(text='', desp=''):

    sc_key = 'SCU87767Tb88d67f50de1408fdc46c93967c23a715e5f18618ecd9'

    if not text.strip():
        print('Text of message is empty!')
        return

    now_time = str(datetime.datetime.now())
    desp = '[{0}]'.format(now_time) if not desp else '{0} [{1}]'.format(desp, now_time)

    try:
        resp = requests.get(
            'https://sc.ftqq.com/{}.send?text={}&desp={}'.format(sc_key, text, desp)
        )
        resp_json = json.loads(resp.text)
        if resp_json.get('errno') == 0:
            print('Message sent successfully [text: {}, desp: \n{}]'.format(text, desp))
        else:
            print('Fail to send message, reason: %s', resp.text)
    except requests.exceptions.RequestException as req_error:
        print('Request error: %s', req_error)
    except Exception as e:
        print('Fail to send message [text: {}, desp: {}]: {}'.format(text, desp, e))
