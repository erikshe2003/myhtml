# -*- coding: utf-8 -*-

from app.myhtml import myhtml
from app.models import Users
from app.xlsx import data2xlsx
import flask, re, time, json, app.db, os


@myhtml.route('/')
@myhtml.route('/index')
def index():
    user_agent = flask.request.headers.get('User-Agent')
    result = re.search("Chrome", user_agent)
    if result:
        return flask.render_template("index.html")
    else:
        return flask.render_template("browserError.html")


@myhtml.route('/login', methods=['POST'])
def login():
    if flask.request.method == 'POST':
        flag = 1
        try:
            username = flask.request.get_json()['username']
            password = flask.request.get_json()['password']
            rememberMe = flask.request.get_json()['rememberMe']
        except Exception as e:
            flag = 0
        # 如果请求方法正确
        if flag == 1:
            theUser = Users(username=username,password=password,remember=rememberMe)
            # 如果用户名和密码填写了
            if username and password:
                user_valid = theUser.ifExists()
                # 如果用户存在
                if user_valid == 2:
                    passwd_valid = theUser.ifpassCorr()
                    # 如果密码正确
                    if passwd_valid == 2:
                        setCookieResult = theUser.setCookie(loginTime=time.strftime("%Y-%m-%d %X"))
                        if setCookieResult == 1:
                            setNetKey = theUser.setNetKey(loginTime=time.strftime("%Y-%m-%d %X"))
                            if setNetKey == 1:
                                returnDataDict = {"state":"4", "key":theUser.getCookie(), "name":theUser.getName(), "username":theUser.username,"netkey":theUser.getNetkey()}
                            else:
                                returnDataDict = {"state": "0", "key": "", "name": "", "username": ""}
                        else:
                            returnDataDict = {"state": "0", "key": "", "name": "", "username": ""}
                    # 如果密码错误
                    elif passwd_valid == 1:
                        returnDataDict = {"state": "3", "key": "", "name": "","username":""}
                    # 如果数据库连接失败
                    else:
                        returnDataDict = {"state": "0", "key": "", "name": "", "username": ""}
                # 如果用户不存在
                elif user_valid == 1:
                    returnDataDict = {"state": "2", "key": "", "name": "","username":""}
                # 如果数据库连接失败
                else:
                    returnDataDict = {"state": "0", "key": "", "name": "", "username": ""}
            # 如果用户名和密码未填写
            else:
                returnDataDict = {"state": "1", "key": "", "name": "", "username": ""}
            return json.dumps(returnDataDict)


@myhtml.route('/checkCookie', methods=['POST'])
def checkCookie():
    # 如果请求方法正确
    if flask.request.method == 'POST':
        flag = 1
        # 尝试检查请求内容
        try:
            username = flask.request.get_json()['username']
            cookie = flask.request.get_json()['cookie']
        except Exception as e:
            flag = 0
        # 如果请求内容完整，则执行查询
        if flag == 1:
            cookie_correct = app.db.checkcookie(username=username, cookie=cookie)
            if cookie_correct == 2:
                returnDataDict = {"state": '2', "name": '数据库无法连接'}
            elif cookie_correct == 1:
                name = app.db.returnname(username=username)
                if name == 0:
                    returnDataDict = {"state": '2', "name": '数据库无法连接'}
                else:
                    returnDataDict = {"state": '1', "name": name}
            else:
                returnDataDict = {"state": '0', "name": 'cookie不符合'}
        # 如果请求内容不完整，则返回错误
        else:
            returnDataDict = {"state": '3', "name": '请求内容错误'}
    # 如果请求方法错误
    else:
        returnDataDict = {"state": '4', "name": '请求方法错误'}
    returnData_JSON = json.dumps(returnDataDict)
    return returnData_JSON


@myhtml.route('/resetPassword', methods=['POST'])
def resetPassword():
    if flask.request.method == 'POST':
        flag = 1
        try:
            username = flask.request.get_json()['username']
            netkey = flask.request.get_json()['netkey']
            old_password = flask.request.get_json()['old']
            new_password = flask.request.get_json()['new']
        except Exception as e:
            flag = 0
        if flag == 1:
            reset_result = app.db.reset_password(username=username, netkey=netkey, old=old_password, new=new_password)
            if reset_result == 0:
                returnDataDict = {"state": '0', "data":"权限错误"}
            elif reset_result == 1:
                returnDataDict = {"state": '1', "data": "旧密码输入错误"}
            elif reset_result == 2:
                returnDataDict = {"state": '2', "data": "修改密码成功"}
            else:
                returnDataDict = {"state": '3', "data": "数据库无法连接"}
        else:
            returnDataDict = {"state": '4', "data": "请求内容错误"}
    else:
        returnDataDict = {"state": '5', "data": "请求方法错误"}
    returnData_JSON = json.dumps(returnDataDict)
    return returnData_JSON


@myhtml.route('/commitAttendance', methods=['POST'])
def commitAttendance():
    if flask.request.method == 'POST':
        flag = 1
        try:
            username = flask.request.get_json()['username']
            netkey = flask.request.get_json()['netkey']
            data = flask.request.get_json()['data']
            day_state = flask.request.get_json()['day_state']
        except Exception as e:
            flag = 0
        if flag == 1:
            commit_result = app.db.commit_attendance(username=username, netkey=netkey, data=data)
            if commit_result == 0:
                returnDataDict = {"state": '0', "data": "权限错误"}
            elif commit_result == 1:
                app.db.changeDay_state(data=day_state)
                returnDataDict = {"state": '1', "data": "考勤提交成功"}
            else:
                returnDataDict = {"state": '2', "data": "数据库连接失败"}
        else:
            returnDataDict = {"state": '3', "data": "请求内容错误"}
    else:
        returnDataDict = {"state": '4', "data": "请求方法错误"}
    returnData_JSON = json.dumps(returnDataDict)
    return returnData_JSON


@myhtml.route('/queryAttendance', methods=['POST'])
def queryAttendance():
    if flask.request.method == 'POST':
        flag = 1
        try:
            username = flask.request.get_json()['username']
            netkey = flask.request.get_json()['netkey']
            date = flask.request.get_json()['date']
            # print(date)
        except Exception as e:
            flag = 0
        if flag == 1:
            query_result = app.db.query_attendance(username=username, netkey=netkey, date=date, user=username)
            if query_result == 0:
                returnDataDict = {"state": '0', "data": "权限错误"}
            elif query_result == 1:
                returnDataDict = {"state": '2', "data": "数据库无法连接"}
            else:
                day_state = app.db.queryDay_state(date=date)
                returnDataDict = {"state": '1', "data": query_result, "day_state": day_state}
                # returnDataDict = {"state": '1', "data": query_result}
        else:
            returnDataDict = {"state": '3', "data": '请求内容错误'}
    else:
        returnDataDict = {"state": '4', "data": '请求方法错误'}
    returnData_JSON = json.dumps(returnDataDict)
    return returnData_JSON


@myhtml.route('/queryUserlist', methods=['POST'])
def queryUserlist():
    if flask.request.method == 'POST':
        flag = 1
        try:
            username = flask.request.get_json()['username']
            netkey = flask.request.get_json()['netkey']
        except Exception as e:
            flag = 0
        if flag == 1:
            query_result = app.db.query_userlist(username=username, netkey=netkey)
            if query_result == 0:
                returnDataDict = {"state": '0', "data": "权限错误"}
            elif query_result == 1:
                returnDataDict = {"state": '1', "data": "数据库无法连接"}
            else:
                returnDataDict = {"state": '2', "data": query_result}
        else:
            returnDataDict = {"state": '3', "data": '请求数据错误'}
    else:
        returnDataDict = {"state": '4', "data": '请求方法错误'}
    returnData_JSON = json.dumps(returnDataDict)
    return returnData_JSON


@myhtml.route('/exportAttendance', methods=['POST'])
def exportAttendance():
    if flask.request.method == 'POST':
        flag = 1
        try:
            # 二比flask.request.form方法居然是按照DOM的name来parse,也是醉了,渣渣中的渣渣,浪费我时间,艹
            # print(flask.request.form.get('username','none'))
            username = flask.request.form.get('username', 'none')
            netkey = flask.request.form.get('netkey', 'none')
            date = flask.request.form.get('date', 'none')
            userlist = flask.request.form.get('userlist', []).split(',')
        except Exception as e:
            flag = 0
        if flag == 1:
            query_result = {}
            day_state = {}
            if date[5:] == '1':
                date_previous = str(int(date[0:4]) - 1) + '-12'
            else:
                date_previous = date[0:4] + '-' + str(int(date[5:]) - 1)
            for i in userlist:
                name = app.db.returnname(i)
                query_result[i + '/' + name] = app.db.query_attendance(username=username, netkey=netkey, date=date, user=i)
                if query_result[i + '/' + name] == 0:
                    returnDataDict = {"state": '0', "data": '权限错误'}
                    return returnDataDict
                elif query_result[i + '/' + name] == 1:
                    returnDataDict = {"state": '1', "data": '数据库无法连接'}
                    return returnDataDict
                query_result[i + '/' + name].update(app.db.query_attendance(username=username, netkey=netkey, date=date_previous, user=i))
            day_state = app.db.queryDay_state(date=date)
            day_state.update(app.db.queryDay_state(date=date_previous))
            newXlsx = data2xlsx(data=query_result,day_state=day_state)
            xlsx_name = newXlsx.create_xlsx()
            response = flask.make_response(flask.send_file(xlsx_name, as_attachment=True, mimetype='application/vnd.ms-excel'))
            # response.headers["Content-Disposition"] = "attachment; filename=" + xlsx_name + ";"
            return response
        else:
            returnDataDict = {"state": '2', "data": '请求内容错误'}
            return returnDataDict
    else:
        returnDataDict = {"state": '3', "data": '请求方法错误'}
        return returnDataDict


@myhtml.route('/fileDownload', methods=['POST'])
def fileDownload():
    if flask.request.method == 'POST':
        flag = 1
        try:
            # 二比flask.request.form方法居然是按照DOM的name来parse,也是醉了,渣渣中的渣渣,浪费我时间,艹
            # print(flask.request.form.get('username','none'))
            filename = flask.request.form.get('filename')
        except Exception as e:
            flag = 0
        if flag == 1:
            response = flask.make_response(flask.send_file(filename + '.exe', as_attachment=True, mimetype='application/octet-stream'))
            return response
        else:
            returnDataDict = {"state": '0', "data": '请求内容错误'}
            return returnDataDict
    else:
        returnDataDict = {"state": '1', "data": '请求方法错误'}
        return returnDataDict

@myhtml.errorhandler(404)
def page_not_found(code):
    return flask.render_template("404.html")

    # if flask.request.method == 'GET':
    #     return flask.render_template("login.html",
    #                                  loginFormPage = forms.c_loginForm()
    #                                  )
    # if flask.request.method == 'POST':
    #     login_username = flask.request.form['username']
    #     login_password = flask.request.form['password']
    #     if login_username:
    #         if login_password:
    #             print(login_username,login_password)
    #             return flask.render_template("login.html",
    #                                  loginFormPage = forms.c_loginForm()
    #                                  )
    #     else:
    #         return flask.render_template("login.html",
    #                                      loginFormPage = forms.c_loginForm()
    #                                      )


@myhtml.route('/test', methods=['GET'])
def test():
    # userAgent = flask.request.headers.get('User-Agent')
    # getUA = re.compile('Chrome')
    # theAgent = re.findall(getUA,userAgent)
    # if theAgent:
    return flask.render_template('test.html')
    # else:
    #     return flask.render_template("notSupport.html")


@myhtml.route('/test_download', methods = ['GET', 'POST'])
def test_download():
    response = flask.make_response(flask.send_file("111.jpg"))
    response.headers["Content-Disposition"] = "attachment; filename=111.jpg;"
    return response

