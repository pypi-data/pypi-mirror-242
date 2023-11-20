# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     app.py
   Description :   
   Author :       FXQ
   date：          2023/11/20 16:00
-------------------------------------------------
"""
from flask import Flask, Response

app = Flask(__name__)

# 装饰器用于全局信息过滤
@app.after_request
def global_filter(response):
    # 检查响应内容是否包含 "test"
    if b'test' in response.data:
        # 如果包含 "test"，可以采取过滤、修改或其他操作
        filtered_content = response.data.replace(b'test', b'filtered')
        response.set_data(filtered_content)

    return response

# 一个简单的路由返回包含 "test" 的内容
@app.route('/')
def home():
    return 'This is a test message.'

if __name__ == '__main__':
    app.run(debug=True)
