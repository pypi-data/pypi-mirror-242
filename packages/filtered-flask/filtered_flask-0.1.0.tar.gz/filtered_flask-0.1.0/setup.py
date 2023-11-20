# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     setup.py
   Description :   
   Author :       FXQ
   date：          2023/11/20 16:02
-------------------------------------------------
"""
from setuptools import setup, find_packages

setup(
    name='filtered_flask',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'Flask',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
