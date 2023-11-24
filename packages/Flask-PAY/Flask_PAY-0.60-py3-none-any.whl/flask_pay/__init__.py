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
            self.app = self.init_app(app)

        self.WeChatPay = WeChatPay

    def init_app(self, app):
        # getattr 的作用是从对象中获取指定名称的属性。如果属性存在，
        # 则返回属性的值；如果属性不存在，并且提供了默认值，则返回默认值；
        # 如果属性不存在且没有提供默认值，则抛出 AttributeError 异常。
        app.extensions = getattr(app, 'extensions', {})

        # 在 app 应用中存储所有扩展实例, 可验证扩展是否完成实例化
        app.extensions['pay'] = self

        # 扩展配置， 初始化后添加到 app.config 中, 以 SHARE_ 开头避免冲突

        return app
