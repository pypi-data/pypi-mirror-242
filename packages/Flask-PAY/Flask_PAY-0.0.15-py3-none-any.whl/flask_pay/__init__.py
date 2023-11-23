"""
 Flask-pay
 # ~~~~~~~~~~~~~~ 
 flask 支付 扩展
 Flask SMS extension
 :copyright: (c) 2023.11 by 浩. 
 :license: GPL, see LICENSE for more details.
"""

import os
import random
import string
from datetime import datetime

from wechatpayv3 import WeChatPay, WeChatPayType


# 限制短信频率


class PAY(object):
    def __init__(self, app=None, pay_config=None, **kwargs):

        self.app = app
        self.pay_config = pay_config

        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        # 兼容 0.7 以前版本
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        # 在 app 应用中存储所有扩展实例, 可验证扩展是否完成实例化
        app.extensions['pay'] = self

        # 扩展配置， 初始化后添加到 app.config 中, 以 SHARE_ 开头避免冲突
        config=self.pay_config()
        self.create_wxpay(config)

    def create_wxpay(self,config):

        MCHID = config['MCHID']
        PRIVATE_KEY = config['PRIVATE_KEY']
        CERT_SERIAL_NO = config['CERT_SERIAL_NO']

        APIV3_KEY = config['APIV3_KEY']
        NOTIFY_URL = config['NOTIFY_URL']
        CERT_DIR = config['CERT_DIR']
        LOGGER = config['LOGGER']
        PARTNER_MODE = config['PARTNER_MODE']

        PROXY = config['PROXY']

        APPID = config['APPID']

        wxpay = WeChatPay(
            wechatpay_type=WeChatPayType.MINIPROG,
            mchid=MCHID,
            private_key=PRIVATE_KEY,
            cert_serial_no=CERT_SERIAL_NO,
            apiv3_key=APIV3_KEY,
            appid=APPID,
            notify_url=NOTIFY_URL,
            cert_dir=CERT_DIR,
            logger=LOGGER,
            partner_mode=PARTNER_MODE,
            proxy=PROXY)
        self.app.wxpay = wxpay
