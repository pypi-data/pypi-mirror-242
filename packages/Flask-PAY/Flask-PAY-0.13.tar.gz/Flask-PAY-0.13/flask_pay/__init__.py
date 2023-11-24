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


class Pay(object):
    def __init__(self, app=None, **kwargs):
        self.app = app
        if app is not None:
            self.state = self.init_app(app)
        else:
            self.state = None

    def init_app(self, app):
        # getattr 的作用是从对象中获取指定名称的属性。如果属性存在，
        # 则返回属性的值；如果属性不存在，并且提供了默认值，则返回默认值；
        # 如果属性不存在且没有提供默认值，则抛出 AttributeError 异常。
        app.extensions = getattr(app, 'extensions', {})

        state = self.init_pay(app.config)
        # 在 app 应用中存储所有扩展实例, 可验证扩展是否完成实例化
        app.extensions['pay'] = state

        # 扩展配置， 初始化后添加到 app.config 中, 以 SHARE_ 开头避免冲突

        return state

    # __getattr__ 是 Python 中的一个特殊方法（special method 或者 dunder method），
    # 用于自定义对象的属性查找行为。当访问一个对象的属性，而该属性不存在时，__getattr__ 方法会被调用
    def __getattr__(self, name):
        return getattr(self.state, name, None)

    def init_pay(self, config):
        pay_type = config.PAY_TYPE
        if pay_type:
            return self.init_wxpay()

    def init_wxpay(self):
        config = self.app.config

        wxpay = WeChatPay(
            wechatpay_type=config.WeChatPayType.MINIPROG,
            mchid=config.MCHID,
            private_key=config.PRIVATE_KEY,
            cert_serial_no=config.CERT_SERIAL_NO,
            apiv3_key=config.APIV3_KEY,
            appid=config.APPID,
            notify_url=config.NOTIFY_URL,
            cert_dir=config.CERT_DIR,
            logger=config.LOGGER,
            partner_mode=config.PARTNER_MODE,
            proxy=config.PROXY)

        return wxpay
