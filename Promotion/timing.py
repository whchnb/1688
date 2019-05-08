# encoding: utf-8
"""
@author: Liwenhao
@e-mail: wh.chnb@gmail.com
@file: timing.py
@time: 2019/5/8 17:57
@desc: 每日01:00 定时执行营销任务
"""
import os
import datetime


timing_time = '01:00:'
while 1:
    now = str(datetime.datetime.now())
    if timing_time in now.split(' ')[1]:
        os.system(r'C:\Users\Administrator\AppData\Local\Programs\Python\Python36-32\python.exe D:/Main/Promotion/alibabaMarket.py')