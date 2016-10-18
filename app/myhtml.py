# -*- coding: utf-8 -*-
__author__ = 'erikshe2003'

from flask import Flask
# from flask_login import LoginManager
# from flask_sqlalchemy import SQLAlchemy

myhtml = Flask(__name__)
# 新增一个登录关系器
# lm = LoginManager()
# 设定这个登陆管理器作用于myhtml
# lm.init_app(myhtml)
# 设定登陆前页面
# lm.login_view = 'login'
# db = SQLAlchemy(myhtml)

# 这什么鬼还没搞懂
# myhtml.config['CSRF_ENABLED'] = True
# 使用session之前必须设置一个密钥
# myhtml.config['SECRET_KEY'] = "567_QAZ-)(*"
# myhtml.config['SQLALCHEMY_DATABASE_URI'] = "mysql://myTools:1qwertyui@localhost/myhtml?charset=utf8&use_unicode=0"
# myhtml.config['SQLALCHEMY_POOL_RECYCLE'] = 15
# myhtml.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = None
# myhtml.config['SQLALCHEMY_BINDS']

from app import route