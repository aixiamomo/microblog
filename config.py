# -*- coding:utf-8 -*-
import os

CSRF_ENABLED = True  # 激活 跨站点请求伪装 保护
SECRET_KEY = 'you-will-never-guess'  # 当CSRF激活时，可以生成一个加密令牌，用于验证表单

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}
    ]

basedir = os.path.abspath(os.path.dirname(__name__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')  # 迁移文件的位置
