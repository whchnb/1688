# encoding: utf-8
"""
@author: Liwenhao
@e-mail: wh.chnb@gmail.com
@file: alibabaMarket.py
@time: 2019/5/6 13:59
@desc: 自动化完成当日访客营销任务
"""
import re
import sys
import time
import random
import logging
import datetime
import json
import requests
from urllib.parse import urlencode


class Alibaba(object):

    def __init__(self, account, pruducts_num):
        """
        初始化信息
        :param account: 需要登录的账号
        """
        print('当前登录的账户为{}'.format(account))
        print('正在初始化')
        self.log()
        self.info_list = []
        self.account = account
        self.pruducts_num = pruducts_num
        # 获取全部的价格
        self.get_price()
        # 获取cookie 的链接
        cookie_url = 'http://192.168.1.99:90/alibaba/get_cookie_byaccount?platform=Alibaba'
        # 获取指定cookie
        self.cookie = self.get_cookie(cookie_url, self.account)
        # 获取ua
        self.ua = self.get_ua()
        # self.cookie = 'ali_apache_id=11.179.217.87.1557109662927.980741.2; t=0ec389e5303cc4ad299e6c6d2807925d; cna=n4lWFZbRW2YCAbe/sh4Lxj33; gangesweb-buckettest=183.191.178.30.1557109697018.0; UM_distinctid=16a8af9c7e322e-0f2c1ced40471a-e323069-15f900-16a8af9c7e4432; _bl_uid=Xkj0mv2UbkIqwqy6Opaw0tny0z6p; sc_g_cfg_f=sc_b_locale=en_US; c_csrf=8eed88a3-a58d-4ea8-84a4-19fb053ab305; cookie2=1c173ba0bf6bfe1fae7710896e8dabc1; v=0; _tb_token_=fe678b3d3b877; acs_usuc_t=acs_rt=df4c8c47f18144f5bcb2a2b6802c1e9e; intl_locale=zh_CN; _csrf_token=1557196020174; _ga=GA1.2.1933742769.1557196023; _gid=GA1.2.1349209298.1557196023; acs_rt=3b27dfd068c7401e960fed41c13bef46; ali_apache_tracktmp=W_signed=Y; xman_us_f=x_locale=zh_CN&x_l=1&last_popup_time=1557109691479&x_user=CN|Ady|Cao|cgs|229737297&no_popup_today=n; _hvn_login=4; CNZZDATA1261550731=1691166204-1557106643-%7C1557295846; csg=a7e1f71b; xman_us_t=ctoken=sc7zznmf5l6f&l_source=alibaba&x_user=PSSkNsnV9SvqLECDzba+Jc1mav3un55GS3kpun1GB7Y=&x_lid=jakcomtech&sign=y&need_popup=y; intl_common_forever=GaEcvzUktdTMm7qfKMm+QplOfxhj6DZi3U/DhDEM5XdJFcrt+N48Hg==; xman_f=maRhMRQ6Cf7GjYQRU/3Rrw4tAjlIBPaIHDM0DQrMZcQFKZcJr00zZsOX9/0B1Btv5GXi0gj65/LDSYTHLE3sln0ydcb8jemuT09K+Bmxznhs6ykUcd4FOmEPFS1toj0CqajaIGRP5mI7tDDyxz1cZgbYkD8ITitIcOY1t7nVITE/6HbXv6pWWq5MEXa42gsN9/yU6iLS079z/SHXm/viieZJJKd2WrueN/uSTMywGq39lHYyiTZo/jZCmx1Gk/UWh9NpoMQ0Oc3OWeoSYAoMnFw+lIYhLGsbIaYA+hPe5aWPe3aGwhx19noe+eaPziTrGXtoRm/7muSi92CmwsQ/VWmkogWX/3OlReZYsy3W+/roJt9a4EKbpafqTtstyHxx; ali_apache_track=ms=|mt=3|mid=jakcomtech; xman_t=rLmgOJS2fHog1OwjfsZB4BUf+JCTf9OiayW4nRIjOQnZZSfAx9RAxacio7lTMaCwX2mdBp6cECTJkOPoPSvS476ngXzfGvm9Dlgw6C9j72yjzQmtJEUSPZNrK+ZZyc0kw4pz14xm3Bspxdaaioz13uzE2shPGXjLAkyNO8wYayEuYPHUhhi1snEx5mbcaVRwNUhk75zsPyDbY3jlv0Qxa5DKuRZ1q2e2j1oGVhfEFdBuBKWA7tWMfqJJMKnhipBawCjqiCeT+CA/MQbii6d0TWQPWjjOzT/TK1UzB+5lMSQxeaFUNmw4NvvIzjDxDaVWA7GIlPwHCuk9rNoxGo9PwF0nZKjwhYo+SpDzLlvfwxl9steGu4bZsFZeQOKN7X+A/rNDEOeYMH6Y+GgrqQeTaYDoxogXBDUDSzfIMv1qBkyiLF8ovhU9q3ocf8HYJ7XYFjTmJTeZL7NpQAOEytQqE6syxWBuA3rnfm6tsRe1PxiiIWj6pLW29KBoUbQrsDkxAXV1OSK0MlxVHtx/EFndawTnoFfrtZy+afw+9SOHC1KsHta/S+TZawKcfS/2folAdyYchCXuuvTKJWgtvw3j3JpGCVWIRH0Ajwu4radrWrHTTxAJ5ftG7+UUMGyOsZRQ8f94ImdVUHEdM5EIkucsz8GYIerz6RQLLdPrk2Hlkw4S7HrjSMuK/Q==; l=bBI6KHolvDecmn5LBOCNSuI8LS79IIRAguPRwCbDi_5aK6Y_g_bOlKS9XFv6Vj5R_NTB4UaStk99-etks; isg=BKWlk1bLFXZpI3E3qhHzPiIotGEfSlj0KxbRgqeKYlzrvsUwbzNBR5tUTGJtvnEs'
        # 请求头
        self.headers = {
            'authority': 'data.alibaba.com',
            # 'method': 'POST',
            'path': '/marketing/visitor',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
            'cache-control': 'max-age=0',
            'cookie': self.cookie,
            'referer': 'https://passport.alibaba.com/icbu_login.htm?return_url=http%3A%2F%2Fdata.alibaba.com%2Fmarketing%2Fvisitor',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        }
        # 从cookie中获取token
        token_re_complie = re.compile(r'ctoken=(.*?)&', re.S)
        self.token = re.findall(token_re_complie, self.cookie)[0]
        # 从cookie中获取csi
        csi_re_complie = re.compile(r'acs_rt=(.*?);', re.S)
        self.csi = re.findall(csi_re_complie, self.cookie)[0]
        # 当前时间
        now_date = datetime.datetime.now()
        # 最近7天起始时间
        self.last_week_start_dt = str(now_date - datetime.timedelta(days=now_date.weekday() + 6)).split()[0]
        self.last_week_end_dt = str(now_date - datetime.timedelta(days=now_date.weekday())).split()[0]
        print('初始化成功')

    def log(self):
        """
        日志
        :return:
        """
        # 设置日志格式
        LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
        # 添加日志时间
        DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
        # 设置日志内容
        logging.basicConfig(filename='market.log', # 日志名称及位置
                            level=logging.INFO,    # 设置日志级别
                            format=LOG_FORMAT,
                            datefmt=DATE_FORMAT)

    def get_username(self):
        """
        获取账户所对应的的用户名
        :return:  账户所对应的的用户名
        """
        url = 'https://data.alibaba.com/marketing/leads?spm=a2793.11769252.0.0.3dea3e5f3d8Tpo'
        response = requests.get(url, headers=self.headers)
        username_re_complie = re.compile(r'"displayName":"(.*?\s.*?)\s', re.S)
        username = re.findall(username_re_complie, response.text)
        if len(username) == 0:
            # logging.critical(str(response.text))
            username = ''
        else:
            username = username[0]
        return username

    def get_price(self):
        """
        获取价格
        :return: 以键值对形式存在的商品价格字典    key：sku   value：price
        """
        # 获取价格的链接
        url = 'http://192.168.1.99:90/alibaba/Get_prices'
        response = requests.get(url)
        # 使用json 对内容进行转换
        price_list = json.loads(response.text)
        # 将price_dic 设置为全局变量
        global price_dic
        # 返回字典
        price_dic = {i['sku']: i for i in price_list}

    def get_cookie(self, url, account):
        """
        获取cookie
        :param url: 获取cookie 的链接
        :param account: 需要获取指定账号的cookie
        :return: 对应账户所需要的cookie
        """
        response = requests.get(url)
        cookies = json.loads(response.text)
        cookie_dic = {}
        for cookie in cookies:
            # 初始化cookie
            custom_cookie = ''
            # 便利cookie信息
            for i in eval(cookie['cookie_dict_list']):
                # 拼接cookie
                custom_cookie = custom_cookie + i['name'] + '={}; '.format(i['value'])
            # 以键值对的形式存放到字典中
            cookie_dic[cookie['account']] = custom_cookie.strip()
        # 返回指定cookie
        return cookie_dic[account]

    def get_message(self, account):
        """
        营销所需要发送的message 数据
        :param account:  发送message 的账户
        :return:  message 信息
        """
        # message 链接
        url = 'http://192.168.1.99:90/alibaba/get_cnname'
        response = requests.get(url)
        message_dicts = json.loads(response.text)
        message = message_dicts[account]
        return message

    def get_ua(self):
        with open('ua.txt', 'r') as f:
            ua = f.read().split('\n')
        return ua

    def get_info(self, page=9, info_list=[]):
        """
        获取蓝标用户
        :param page: 页数
        :return: 20个蓝标客户
        """
        # post 请求携带的参数
        data_dic = {
            'orderBy': 'staySecond',
            'orderModel': 'desc',
            'pageSize': '10',
            'pageNO': page,
            'statisticsType': 'day',
            'selected': '0',
            'startDate': self.last_week_start_dt,
            'endDate': self.last_week_end_dt,
            'searchKeyword': '',
            'buyerRegion': '',
            'buyerCountry': '',
            'subMemberSeq': '',
            'isMcFb': 'false',
            'isAtmFb': 'false',
            'mailable': 'true',
            'mailed': 'false',
            'hasRemarks': 'false',
            'statisticType': 'os',
            'desTime': str(time.time()).replace('.', '')[:13]
        }
        # 商户链接
        info_url = 'https://hz-mydata.alibaba.com/self/.json?action=CommonAction&iName=getVisitors&isVip=true&0.656950193681427&ctoken={}&dmtrack_pageid=b7bfb21e0b0857fb5ccfeba816a8c31c32b1d20a17'.format(
            self.token)
        info_response = requests.post(info_url, headers=self.headers, data=data_dic)
        # 获取到的数据为json数据，使用json.loads加载数据
        # print(info_response.text)
        # print(info_response.url)
        try:
            datas = json.loads(info_response.text)
        except ValueError as e:
            print('cookie 已失效！即将退出程序')
            logging.critical('cookie 已失效,{}'.format(self.account))
            sys.exit()
        info_datas = datas['value']['data']
        print('当前第{}页,正在获取蓝标客户'.format(page))
        # 遍历每条数据
        for info_data in info_datas:
            # 如果 buyerTag 为 A 则为蓝标客户
            if info_data['buyerTag'] == 'A':
                # 获取所需要的数据
                info_list.append(info_data)
                num = len(info_list)
                print('共获取{}，已获取{}'.format(self.pruducts_num, num))
                if num == self.pruducts_num:
                    return info_list
        page += 1
        time.sleep(2)
        return self.get_info(page, info_list)

    def customer_info(self, info_datas):
        for index, info_data in enumerate(info_datas):
            print('客户ID为：{}'.format(info_data['visitorId']))
            buyerMemberSeq = info_data['buyerMemberSeq']
            statDate = info_data['statDate']
            # 通过请求用户详情页获取umidToken 和csrf_token
            umidToken, csrf_token = self.get_detail(statDate, buyerMemberSeq)
            class_dict = self.get_class(csrf_token, self.token)
            product_class = 'Hot sale'
            class_id = class_dict[product_class]
            print('推荐的分类为{}，id:{}'.format(product_class, class_id))
            products_list, SKU_list = self.get_product_lists(class_id, self.token, csrf_token)
            status = self.send_market(umidToken, csrf_token, info_data=info_data, products_list=products_list, SKU_list=SKU_list, index=index)
            if status == False:
                print("账号：{}   今日已完成营销任务".format(self.account))
                break
            # 设置频率，每5秒营销一次
            time.sleep(5)
            # break

    def get_detail(self, statDate, buyerMemberSeq):
        """
        获取页面中的umidToken 和csrf_token
        :param statDate: 时间
        :param buyerMemberSeq: 用户所对应的的id
        :return: statDate, buyerMemberSeq
        """
        url = 'https://message.alibaba.com/message/leadsDetail.htm?products%3D%5B%5D%26buyers%3D%5B%7B%22secAccountId%22%3A%22{}%22%2C%22statDate%22%3A%22{}%22%7D%5D%26mloca%3DCONTACT_MKT_VISITORS_MYDATA'.format(
            buyerMemberSeq, statDate)
        response = requests.post(url, headers=self.headers)
        # umidToken 和csrf_token渲染在HTML 页面中，使用正则获取到umidToken 和csrf_token
        umidToken_re_complie = re.compile(r"window.umidToken = '(.*?)';", re.S)
        umidToken = re.findall(umidToken_re_complie, response.text)[0]
        csrf_token_re_complie = re.compile(r"csrfTokenVal: '(.*?)',", re.S)
        csrf_token = re.findall(csrf_token_re_complie, response.text)[0]
        return umidToken, csrf_token

    def get_class(self, csrf_token, token):
        """
        获取商品的全部分类
        :param csrf_token: 对应的csrf_token
        :param token: 对应的token
        :return: 键值对形式存在的商品分类字典         key:商品分类  value:分类id
        """
        # 获取商品分类的链接
        url = 'https://hz-productposting.alibaba.com/product/group_ajax.htm?event=listGroupForCom&parentGroupId=-1&_csrf_token_={}&ctoken={}'.format(
            csrf_token, token)
        response = requests.get(url, headers=self.headers)
        class_data = json.loads(response.text)
        class_dict = {i['name']: i['id'] for i in class_data['data']}
        return class_dict

    def get_product_lists(self, product_id, token, csrf_token):
        """
        营销所需要的5个商品
        :param product_id: 商品分类id
        :param token: 对应的token
        :param csrf_token: 对应的csrf_token
        :return: 5个已构造好营销所需要发送的商品信息
        """
        # 获取对应分类的商品链接
        url = 'https://hz-productposting.alibaba.com/product/managementproducts/asyQueryProductList.do?ctoken={}'.format(
            token)
        # post 请求所需要携带的fromdata
        data = {
            'subject': '',
            'redModel': '',
            'status': 'approved',
            'imageType': 'all',
            'ownerMemberId': '',
            'isDisplay': 'Y',
            'repositoryType': 'public',
            'isWindowProduct': '',
            'isAuthProduct': '',
            'isKeywords': '',
            'page': '1',
            'gmtModifiedFrom': '',
            'gmtModifiedTo': '',
            'size': '50',
            'groupId': product_id,
            'groupLevel': '1',
            'sroomId': '',
            '_csrf_token_': csrf_token,
        }
        response = requests.post(url, data=data, headers=self.headers)
        data = json.loads(response.text)['products']
        # 随机获取5个不重复商品的索引
        index = random.sample(range(len(data)), 5)
        # 初始化商品列表
        products_list = []
        # 初始化SKU 列表
        SKU_list = []
        # 遍历随机的5个商品索引
        for i in index:
            # 对应的商品
            product = data[i]
            # 判断如果SKU 为N2 则将SKU 改为N2X
            product_name = product['redModel'] if product['redModel'] != 'N2' else 'N2X'
            # 发送营销所需要的商品数据
            product_dic = {"quantity": "3000",  # 商品数量
                           "unitPrice": price_dic[product_name]['fob_3000_usd'],  # 商品数量3000+ 所对应的价格
                           "productName": product['subject'],  # 商品全名
                           "productId": product['id'],  # 商品所对应的id
                           "id": "",
                           "imageUrl": product['absImageUrl'] + '_100x100.jpg',  # 商品图片链接
                           "url": product['detailUrl'],  # 商品详情链接
                           "source": "",
                           "unit": "Piece(s)",
                           "unitCode": "007"
                           }
            # 将每个构造好的商品详情放入products_list 中
            products_list.append(product_dic)
            SKU_list.append(product['redModel'])
        return products_list, SKU_list

    def send_market(self, umidToken, csrf_token, info_data, products_list, SKU_list, index):
        """
        发送营销
        :param umidToken: 对应的umidToken
        :param csrf_token: 对应的csrf_token
        :param info_data: 客户信息
        :param products_list: 营销所需要发送的商品信息
        :return:
        """
        # 营销页面所使用的headers
        headers = {
            'authority': 'message.alibaba.com',
            'method': 'POST',
            'path': '/msgsend/ajax/PostMarketingMessage.htm?ctoken=ongd08aql3ei&dmtrack_pageid=b7bfb21e0bb0746f5cd1342e16a9133d8e921250f7',
            'scheme': 'https',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
            'content-length': '3138',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': self.cookie,
            'origin': 'https://message.alibaba.com',
            'referer': 'https://message.alibaba.com/message/leadsDetail.htm?products%3D%5B%5D%26buyers%3D%5B%7B%22secAccountId%22%3A%22ID1xV7pH7lFQCr9bt4-7svvcVwttJsVxQBc4DQeo6DEsNw*%22%2C%22statDate%22%3A%222019-05-05%22%7D%5D%26mloca%3DCONTACT_MKT_VISITORS_MYDATA',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        # 需要发送的message 信息
        message = self.get_message(self.account)
        # 需要发送的formdata 数据中的参数数据
        username = self.get_username()
        buyerRegion = info_data['buyerRegion']
        secIds = info_data['buyerMemberSeq']
        visitorId = info_data['visitorId']
        params = {
            "ids": [str(time.time()).replace('.', '')[6:15]],
            "secIds": [secIds],
            "buyerRandomIds": [visitorId],
            "buyerRegions": [buyerRegion],
            "recommendIds": [""],
            "recommendType": "buyerleads",
            "productTerm": {
                "productInfo": products_list,
                "attachments": []
            },
            "content": message,
            "subject": "Top and relative quotation recommended from {}".format(username),
        }
        ua = self.ua[index + 10]
        # 构造营销所需的FROM_DATA
        send_data = {
            '_csrf_token_': csrf_token,
            'postId': str(time.time()).replace('.', '')[:13],
            'mloca': 'CONTACT_MKT_VISITORS_MYDATA',
            'ua': ua,
            '_csi_': self.csi,
            'umidToken': umidToken,
            'imagePassword': '',
            'params': json.dumps(params)
        }
        url = 'https://message.alibaba.com/msgsend/ajax/PostMarketingMessage.htm?ctoken={}&dmtrack_pageid=b7bfb21e0b01563e5ccfe9e016a8c2acdd9a88cab0'.format(
            self.token)
        # '''
        try:
            response = requests.post(url, headers=headers, data=send_data)
            status = json.loads(response.text)['code']
            messages = json.loads(response.text)['message']
        except requests.exceptions.SSLError  as e:
            print('SSL 错误，即将退出')
            logging.critical('SSL 出错,{}'.format(self.account))
            sys.exit()
        # print(response.json())
        # print(status)
        if status == 200:
            print('发送营销成功')
            logging.info('营销状态：{},{},{},{}'.format(self.account, self.ua.index(ua), response.json(), info_data))
            # 添加营销时间
            info_data['market_time'] = str(datetime.datetime.now())
            # 写入任务日志
            self.task_log(info_data, SKU_list)
        elif status == 500 and '已达单日营销次数上限' in messages:
            print('账号：{}   已达单日营销次数上限'.format(self.account))
            logging.warning('营销状态：{}  {}  已达单日营销次数上限'.format(self.account, self.ua.index(ua)))
            return False
        else:
            logging.error('营销状态：{},{},{},{}'.format(self.account, self.ua.index(ua), response.json(), info_data))
        # '''

        return True

    def task_log(self, info_data, SKU_list):
        """
        任务日志
        :param info_data: 用户信息
        :param SKU_list: SKU 列表名称
        :return:
        """
        # 构造网站行为
        website_behavior = '总浏览量{},浏览{}个供应商,发布{}个RFQ,对{}个供应商发起{}个询盘'.format(
            info_data.get('totalVisitPv', 0),
            info_data.get('totalVisitSellerCnt', 0),
            info_data.get('totalRfqCnt', 0),
            info_data.get('totalMcSellerCnt', 0),
            info_data.get('totalMcFbCnt', 0)
        )
        # 构造旺铺行为
        wp_behavior = []
        wp_behavior = wp_behavior.append('Add to Inquiry Cart') if info_data['isAddInquiryCart'] == 1 else wp_behavior
        wp_behavior = wp_behavior.append('点击start order') if info_data['isClickPlaceOrder'] == 1 else wp_behavior
        wp_behavior = wp_behavior.append('发起TM 咨询') if info_data['isAtmFb'] == 1 else wp_behavior
        wp_behavior = wp_behavior.append('访问home') if info_data['isVisitHomepage'] == 1 else wp_behavior
        wp_behavior = wp_behavior.append('访问company profile') if info_data['isVisitProfilePage'] == 1 else wp_behavior
        wp_behavior = wp_behavior.append('访问contacts') if info_data['isVisitContactPage'] == 1 else wp_behavior
        wp_behavior = wp_behavior.append('已发起询盘') if info_data['isMcFb'] == 1 else wp_behavior
        # 构造需要提交的日志信息
        data = {
            "Createtime": info_data['market_time'],  # 营销时间
            "Account": self.account,  # 账号
            "Clientname": info_data['visitorId'],  # 客户名
            "Views": info_data['visitPv'],  # 浏览次数
            "Staytime": info_data['staySecond'],  # 停留时长
            "Wangpu": json.dumps(wp_behavior),  # 旺铺行为
            "Website": website_behavior,  # 网站行为
            "SKU": json.dumps(SKU_list)  # 推荐SKU
        }
        url = 'http://192.168.1.99:90/alibaba/Log_promotion?' + urlencode(data)
        response = requests.get(url, params=json.dumps(data))
        print(response.text)
        logging.info('任务日志：{},{},{}'.format(self.account, response.text, data))


if __name__ == '__main__':
    # 需要登陆的账户
    cookie_accounts = [
        # 'fb1@jakcom.com',
        'fb2@jakcom.com',
        # 'fb3@jakcom.com',
        # 'tx@jakcom.com',
    ]
    for cookie_account in cookie_accounts:
        # 营销的数量
        pruducts_num = 2
        alibaba = Alibaba(cookie_account, pruducts_num)
        info_datas = alibaba.get_info()
        alibaba.customer_info(info_datas)
        # 每个账号之间设置3分钟间隔
        time.sleep(180)
