# -*- coding: utf-8 -*-

import pymysql


def checkcookie(username,cookie):
    flag = 1
    try:
        db_connect = pymysql.connect(user='root', host='192.168.2.133', password='1qwertyui', db='myhtml',
                                     charset="utf8", port=3306)
    except Exception as e:
        flag = 0
    if flag == 1:
        db_cursor = db_connect.cursor()
        db_cursor.execute('select cookie from users where username = "%s"' % (username))
        db_cookie = db_cursor.fetchone()[0]
        # print(db_cookie)
        db_cursor.close()
        db_connect.close()
        if cookie == db_cookie:
            # 1代表查询成功，并且结果正确
            return 1
        else:
            # 0代表查询成功，但是结果错误
            return 0
    else:
        # 2代表查询失败，数据库无法连接
        return 2


def returnname(username):
    flag = 1
    try:
        db_connect = pymysql.connect(user='root', host='192.168.2.133', password='1qwertyui', db='myhtml',
                                     charset="utf8", port=3306)
    except Exception as e:
        flag = 0
    if flag == 1:
        db_cursor = db_connect.cursor()
        db_cursor.execute('select name from users where username = "%s"' % (username))
        db_name = db_cursor.fetchone()[0]
        db_cursor.close()
        db_connect.close()
        return db_name
    else:
        return 0


def reset_password(username,netkey,old,new):
    flag = 1
    try:
        db_connect = pymysql.connect(user='root', host='192.168.2.133', password='1qwertyui', db='myhtml',
                                     charset="utf8", port=3306)
    except Exception as e:
        flag = 0
    if flag == 1:
        db_cursor = db_connect.cursor()
        db_cursor.execute('select netkey from users where username = "%s"' % (username))
        db_netkey = db_cursor.fetchone()[0]
        if netkey == db_netkey:
            db_cursor.execute('select userpassword from users where username = "%s"' % (username))
            db_password = db_cursor.fetchone()[0]
            if old == db_password:
                db_cursor.execute('UPDATE users SET userpassword = "%s" where username = "%s"' % (new,username))
                db_connect.commit()
                reset_password_result = 2
            else:
                reset_password_result = 1
        else:
            reset_password_result = 0
        db_cursor.close()
        db_connect.close()
    else:
        reset_password_result = 3
    return reset_password_result


def commit_attendance(username,netkey,data):
    flag = 1
    try:
        db_connect = pymysql.connect(user='root', host='192.168.2.133', password='1qwertyui', db='myhtml',
                                     charset="utf8", port=3306)
    except Exception as e:
        flag = 0
    if flag == 1:
        db_cursor = db_connect.cursor()
        db_cursor.execute('select netkey from users where username = "%s"' % (username))
        db_netkey = db_cursor.fetchone()[0]
        if netkey == db_netkey:
            for i in data:
                db_cursor.execute('UPDATE attendance SET clockin_time = "%s", clockout_time = "%s" WHERE username = "%s" AND clock_date = "%s"' % (data[i]["clockin"],data[i]["clockout"],username,i))
                db_connect.commit()
                db_cursor.execute('INSERT INTO attendance(username, clock_date, clockin_time, clockout_time) SELECT "%s", "%s", "%s", "%s" FROM DUAL WHERE NOT EXISTS(SELECT * FROM attendance WHERE username = "%s" AND clock_date = "%s")' % (username,i,data[i]["clockin"],data[i]["clockout"],username,i))
                db_connect.commit()
            commit_attendance_result = 1
        else:
            commit_attendance_result = 0
        db_cursor.close()
        db_connect.close()
    else:
        commit_attendance_result = 2
    return commit_attendance_result


def query_attendance(username,netkey,date,user):
    flag = 1
    try:
        db_connect = pymysql.connect(user='root', host='192.168.2.133', password='1qwertyui', db='myhtml',
                                     charset="utf8", port=3306)
    except Exception as e:
        flag = 0
    if flag == 1:
        db_cursor = db_connect.cursor()
        db_cursor.execute('select netkey from users where username = "%s"' % (username))
        db_netkey = db_cursor.fetchone()[0]
        if netkey == db_netkey:
            query_attendance_result = {}
            db_cursor.execute('select clock_date,clockin_time,clockout_time from attendance where username = "%s" and clock_date like "%s"' % (user,date + '%'))
            db_data = db_cursor.fetchall()
            for i in db_data:
                query_attendance_result[i[0]] = {"clockin_time":i[1],"clockout_time":i[2]}
        else:
            query_attendance_result = 0
        db_cursor.close()
        db_connect.close()
    else:
        query_attendance_result = 1
    return query_attendance_result


def changeDay_state(data):
    flag = 1
    try:
        db_connect = pymysql.connect(user='root', host='192.168.2.133', password='1qwertyui', db='myhtml',
                                     charset="utf8", port=3306)
    except Exception as e:
        flag = 0
    if flag == 1:
        db_cursor = db_connect.cursor()
        for i in data:
            db_cursor.execute('UPDATE month SET state = "%s" WHERE date = "%s"' % (data[i],i))
            db_connect.commit()
            db_cursor.execute('INSERT INTO month(state, date) SELECT "%s", "%s" FROM DUAL WHERE NOT EXISTS(SELECT * FROM month WHERE date = "%s")' % (data[i],i,i))
            db_connect.commit()
        db_cursor.close()
        db_connect.close()


def queryDay_state(date):
    flag = 1
    try:
        db_connect = pymysql.connect(user='root', host='192.168.2.133', password='1qwertyui', db='myhtml',
                                     charset="utf8", port=3306)
    except Exception as e:
        flag = 0
    if flag == 1:
        query_day_state = {}
        db_cursor = db_connect.cursor()
        db_cursor.execute('select * from month where date like "%s"' % (date + '%'))
        db_data = db_cursor.fetchall()
        # print(db_data)
        for i in db_data:
            query_day_state[i[1]] = i[2]
        db_cursor.close()
        db_connect.close()
    else:
        query_day_state = 0
    return query_day_state


def query_userlist(username,netkey):
    flag = 1
    try:
        db_connect = pymysql.connect(user='root', host='192.168.2.133', password='1qwertyui', db='myhtml',
                                     charset="utf8", port=3306)
    except Exception as e:
        flag = 0
    if flag == 1:
        db_cursor = db_connect.cursor()
        db_cursor.execute('select netkey from users where username = "%s"' % (username))
        db_netkey = db_cursor.fetchone()[0]
        if netkey == db_netkey:
            query_userlist_result = {}
            db_cursor.execute(
                'select username,name from users where project_group = (select project_group from users where username = "%s")' % (
                username))
            db_data = db_cursor.fetchall()
            for i in db_data:
                query_userlist_result[i[0]] = i[1]
        else:
            query_userlist_result = 0
        db_cursor.close()
        db_connect.close()
    else:
        query_userlist_result = 1
    return query_userlist_result