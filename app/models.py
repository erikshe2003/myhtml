# -*- coding: utf-8 -*-

import hashlib
import pymysql
from wtforms import StringField, SubmitField

# class Users(db.Model):
#     id = db.Column(db.Integer, primary_key = True, autoincrement = True)
#     username = db.Column(db.VARCHAR(50))
#     usermail = db.Column(db.VARCHAR(50))
#     userpassword = db.Column(db.VARCHAR(50))
key = "!@#)(*qwePOI"
netkey_KEY = "asdf}{PO"
class Users():
    def __init__(self, id=None, username=None, mail=None, password=None, remember=None):
        self.id = id
        self.username = username
        self.mail = mail
        self.password = password
        self.remember = remember
        self.user_cookie = ""

    def ifExists(self):
        flag = 1
        try:
            db_connect = pymysql.connect(user='root', host='192.168.2.133', password='1qwertyui', db='myhtml',
                                         charset="utf8", port=3306)
        except Exception as e:
            flag = 0
        # 如果数据库连接成功
        if flag == 1:
            db_cursor = db_connect.cursor()
            # 如果查询成功
            if db_cursor.execute('select * from users where username = "%s"' % (self.username)) != 0:
                db_cursor.close()
                return 2
            # 如果查询失败
            else:
                db_cursor.close()
                db_connect.close()
                return 1
        # 如果数据库连接失败
        else:
            return 0

    def ifpassCorr(self):
        flag = 1
        try:
            db_connect = pymysql.connect(user='root', host='192.168.2.133', password='1qwertyui', db='myhtml',
                                         charset="utf8", port=3306)
        except Exception as e:
            flag = 0
        # 如果数据库连接成功
        if flag == 1:
            db_cursor = db_connect.cursor()
            # 如果密码正确
            if db_cursor.execute('select * from users where username = "%s" and userpassword = "%s"' % (self.username,self.password)) != 0:
                db_cursor.close()
                db_connect.close()
                return 2
            # 如果密码错误
            else:
                db_cursor.close()
                db_connect.close()
                return 1
        # 如果数据库连接失败
        else:
            return 0

    def setCookie(self,loginTime):
        flag = 1
        try:
            db_connect = pymysql.connect(user='root', host='192.168.2.133', password='1qwertyui', db='myhtml',
                                         charset="utf8", port=3306)
        except Exception as e:
            flag = 0
        # 如果数据库连接成功
        if flag == 1:
            if self.remember == False:
                db_cursor = db_connect.cursor()
                db_cursor.execute('UPDATE users SET last_logintime = "%s",remember = %d WHERE username = "%s"' % (loginTime,0,self.username))
                db_connect.commit()
            else:
                self.user_cookie = hashlib.sha1(self.username.encode(encoding='utf-8') + loginTime.encode(encoding='utf-8') + key.encode(encoding='utf-8')).hexdigest()
                db_cursor = db_connect.cursor()
                db_cursor.execute('UPDATE users SET cookie= %s,last_logintime = %s,remember = %s WHERE username = %s',(self.user_cookie,loginTime,self.remember,self.username))
                db_connect.commit()
            db_cursor.close()
            db_connect.close()
            return 1
        # 如果数据库连接失败
        else:
            return 0

    def getCookie(self):
        return self.user_cookie

    def getName(self):
        flag = 1
        try:
            db_connect = pymysql.connect(user='root', host='192.168.2.133', password='1qwertyui', db='myhtml',
                                         charset="utf8", port=3306)
        except Exception as e:
            flag = 0
        # 如果数据库连接成功
        if flag == 1:
            db_cursor = db_connect.cursor()
            db_cursor.execute('select name from users where username = %s',(self.username))
            name = db_cursor.fetchone()[0]
            db_cursor.close()
            db_connect.close()
            return name
        else:
            return 0

    def setNetKey(self,loginTime):
        flag = 1
        try:
            db_connect = pymysql.connect(user='root', host='192.168.2.133', password='1qwertyui', db='myhtml',
                                         charset="utf8", port=3306)
        except Exception as e:
            flag = 0
        # 如果数据库连接成功
        if flag == 1:
            self.user_netkey = hashlib.sha1(self.username.encode(encoding='utf-8') + loginTime.encode(encoding='utf-8') + netkey_KEY.encode(encoding='utf-8')).hexdigest()
            db_cursor = db_connect.cursor()
            db_cursor.execute('UPDATE users SET netkey = "%s" WHERE username = "%s"' % (self.user_netkey, self.username))
            db_connect.commit()
            db_cursor.close()
            db_connect.close()
            return 1
        else:
            return 0

    def getNetkey(self):
        flag = 1
        try:
            db_connect = pymysql.connect(user='root', host='192.168.2.133', password='1qwertyui', db='myhtml',
                                         charset="utf8", port=3306)
        except Exception as e:
            flag = 0
        # 如果数据库连接成功
        if flag == 1:
            db_cursor = db_connect.cursor()
            db_cursor.execute('select netkey from users where username = "%s"' % (self.username))
            netkey = db_cursor.fetchone()[0]
            db_cursor.close()
            db_connect.close()
            return netkey
        else:
            return 0






