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




        self.create_wxpay(self.pay_config)

    def create_wxpay(self, config):

        MCHID = config.get('MCHID')
        PRIVATE_KEY = config.get('PRIVATE_KEY')
        CERT_SERIAL_NO = config.get('CERT_SERIAL_NO')
        APIV3_KEY = config.get('APIV3_KEY')
        APPID = config.get('APPID')
        NOTIFY_URL = config.get('NOTIFY_URL')
        CERT_DIR = config.get('CERT_DIR')
        LOGGER = config.get('LOGGER')
        PARTNER_MODE = config.get('PARTNER_MODE')
        PROXY = config.get('PROXY')

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
