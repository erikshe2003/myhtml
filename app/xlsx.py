# -*- coding: utf-8 -*-

import time, datetime, xlsxwriter, random

class data2xlsx():
    def __init__(self, data, day_state):
        self.data = data
        self.day_state = day_state
        self.date = time.strftime('%Y%m%d', time.localtime())
        self.month = time.strftime('%m', time.localtime())
        self.year = time.strftime('%Y', time.localtime())
        self.day = time.strftime('%H%M%S', time.localtime())
        # 取得当前时间的时间戳
        self.today_seconds = time.time()

    def writeAttendanceSheet_lastWeek(self):
        # 行码
        rowNum = 0
        # 列码
        colNum = 0
        # 判断周统计表宽度,计算第一行最右位置单元格的x轴英语代码
        i = 3 * len(self.data) + 1
        if i < 26:
            # 如果i小于26,则直接给出字母
            merge_string = chr(i + 64)
        else:
            # 如果i大于26,则需要将i/26算出第一位(一个项目组人数不会很多)
            n = i // 26
            i = i - n * 26
            merge_string = chr(n + 64) + chr(i + 64)
        # 合并单元格并写入第一行项目组名称
        self.sheet_lastWeek.merge_range('A1:'+ merge_string + '1', 'Tv游戏测试人员考勤统计', self.lastWeek_title_format)
        # 合并单元格并写入第二/三行注
        self.sheet_lastWeek.merge_range('A2:' + merge_string + '4', '注：工作时间及加班时间都以h为单位\n    加班时间需除去吃饭时间\n    黄色为考勤异常,请及时确认', self.lastWeek_tips_format)
        # 调整A列宽度
        self.sheet_lastWeek.set_column('A:A', len('xxxx-xxxx'))
        # 写A4"考勤统计"
        rowNum = 4
        self.sheet_lastWeek.write(rowNum, colNum, '考勤统计', self.lastWeek_leftColumn_format)
        # 写A5"统计时间"
        # 返回昨天的struct_time
        yesterday_seconds = self.today_seconds - 86400
        yesterday_struct_time = time.localtime(yesterday_seconds)
        # 返回昨天的格式日期
        yesterday = time.strftime('%m%d',yesterday_struct_time)
        yesterday_day = time.strftime('%w',yesterday_struct_time)
        # 返回7天前日期的struct_time
        firstday_seconds = yesterday_seconds - 518400
        firstday_struct_time = time.localtime(firstday_seconds)
        # 返回8天前的格式日期
        firstday = time.strftime('%m%d', firstday_struct_time)
        rowNum = 5
        self.sheet_lastWeek.write(rowNum, colNum, firstday + '-' + yesterday, self.lastWeek_leftColumnTitle_format)
        # 写日期列
        days = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
        j = 0
        while j < 7:
            self.sheet_lastWeek.write(rowNum + j + 1, colNum, days[int(yesterday_day) - 6 + j], self.lastWeek_leftColumn_formatc)
            j += 1
        # 写"总计"
        self.sheet_lastWeek.write(rowNum + 8, colNum, '总计', self.lastWeek_leftColumn_formatc)
        # 写每个人的上周考勤
        self.lastWeek_everyone(position_left='B5', position_x=1, position_y=5, data=self.data)

    # 给定每个人上周的考勤;从最左边的开始位置,也就是B5;调用lastWeek_everyone方法向右写
    def lastWeek_everyone(self, position_left, position_x, position_y, data):
        lastWeek_data = self.lastWeek_data(data)
        p_left = position_left
        p_x = position_x
        p_y = position_y
        # 返回7天前日期的struct_time
        firstday_seconds = self.today_seconds - 604800
        for name in lastWeek_data:
            rowNum = p_y
            colNum = p_x
            theday_seconds = firstday_seconds
            everyone_data = lastWeek_data[name]
            # 根据给定的position计算最右位置单元格的x轴英语代码,如果position=B4,则输出D4;如果position=Z4,则输出AB4
            position_char = p_left[:-1]
            # 如果字母为两位(员工没多少,不需要考虑三位)
            if len(position_char) > 1:
                # 判断第二位字母是否是Y以上的
                if ord(position_char[1]) > 88:
                    #如果是,则字母第一位+1,字母第二位-24
                    position_char_right = chr(ord(position_char[0]) + 1) + chr(ord(position_char[1]) - 24)
                else:
                    #如果不是,则字母第一位不变,字母第二位+2
                    position_char_right = position_char[0] + chr(ord(position_char[1]) + 2)
            #如果字母为一位
            else:
                # 判断字母是否Y以上
                if ord(position_char) > 88:
                    #如果是,则字母第一位写A,字母第二位+3-26
                    position_char_right = 'A' + chr(ord(position_char) - 24)
                else:
                    # 如果不是,则字母+2
                    position_char_right = chr(ord(position_char) + 2)
            position_right = position_char_right + p_left[-1]
            # 合并单元格并写入姓名
            self.sheet_lastWeek.merge_range(p_left + ':' + position_right, name.split('/')[1],
                                            self.lastWeek_name_format)
            # 向右依次写'上班时间','下班时间','加班时间'
            for string in ['上班时间', '下班时间', '加班时间']:
                self.sheet_lastWeek.write(rowNum, colNum, string, self.lastWeek_leftColumnTitle_format)
                colNum += 1
            # 行数+1,列数重置
            rowNum += 1
            colNum = p_x
            # 按照lastWeek_data[name]中数据的顺序,依次向右写内容
            # 往前一天,写数据
            for x in everyone_data:
                # 如果是双休日,则上/下/加班时间单独计算
                theday_day = time.strftime('%w', time.localtime(theday_seconds))
                if theday_day == '0' or theday_day == '6':
                    # 写上班时间
                    clockin_time = x[1]
                    self.sheet_lastWeek.write(rowNum, colNum, clockin_time, self.lastWeek_clock_format)
                    # 列数+1
                    colNum += 1
                    # 写下班时间
                    clockout_time = x[2]
                    self.sheet_lastWeek.write(rowNum, colNum, clockout_time, self.lastWeek_clock_format)
                    # 列数+1
                    colNum += 1
                    # 写加班时间.
                    overtime = ''
                    if clockout_time == '-':
                        self.sheet_lastWeek.write(rowNum, colNum, '-', self.lastWeek_overtime_format)
                    else:
                        clockout_h = clockout_time.split(':')[0]
                        clockout_m = clockout_time.split(':')[1]
                        clockin_h = clockin_time.split(':')[0]
                        clockin_m = clockin_time.split(':')[1]
                        # 需要判断当天状态,是正常/休息/还是上班.
                        # 若当天需要上班
                        if self.day_state[x[0]] == 2:
                            # 若上班时间早于9点,则加班时间 = 下班时间分钟数 - 9点分钟数 - 9h
                            if int(clockin_h) < 9:
                                overtime_m = int(clockout_h) * 60 + int(clockout_m) - 9 * 60 - 9 * 60
                            # 若上班时间9-10点,则加班时间 = 下班时间分钟数 - 上班时间分钟数 - 9h
                            elif 540 <= int(clockin_h) * 60 + int(clockin_m) <= 600:
                                overtime_m = int(clockout_h) * 60 + int(clockout_m) - int(clockin_h) * 60 - int(clockin_m) - 9 * 60
                            # 若上班时间晚于10点,则加班时间 = 下班时间分钟数 - 10点分钟数 - 9h
                            elif 600 < int(clockin_h) * 60 + int(clockin_m):
                                overtime_m = int(clockout_h) * 60 + int(clockout_m) - 10 * 60 - 9 * 60
                            if overtime_m <= 0:
                                overtime = 0
                            else:
                                overtime_h = overtime_m // 60
                                if overtime_m - overtime_h * 60 > 30:
                                    overtime = overtime_h + 0.5
                                else:
                                    overtime = overtime_h
                        # 若当天放假或节假日
                        else:
                            overtime_m = int(clockout_h) * 60 + int(clockout_m) - int(clockin_h) * 60 - int(clockin_m)
                            overtime_h = overtime_m // 60
                            if overtime_m - overtime_h * 60 > 30:
                                overtime = overtime_h + 0.5
                            else:
                                overtime = overtime_h
                        self.sheet_lastWeek.write(rowNum, colNum, overtime, self.lastWeek_overtime_format)
                else:
                    # 写上班时间
                    clockin_time = x[1]
                    if clockin_time == '-':
                        self.sheet_lastWeek.write(rowNum, colNum, clockin_time, self.lastWeek_clock_format)
                    elif int(clockin_time.split(':')[0]) >= 9 and int(clockin_time.split(':')[1]) > 0:
                        self.sheet_lastWeek.write(rowNum, colNum, clockin_time, self.lastWeek_clock_format)
                    else:
                        self.sheet_lastWeek.write(rowNum, colNum, clockin_time, self.lastWeek_clock_format)
                    # 列数+1
                    colNum += 1
                    # 写下班时间
                    clockout_time = x[2]
                    if clockout_time == '-':
                        self.sheet_lastWeek.write(rowNum, colNum, clockout_time, self.lastWeek_clock_format)
                    elif int(clockout_time.split(':')[0]) < 18:
                        self.sheet_lastWeek.write(rowNum, colNum, clockout_time, self.lastWeek_clock_format)
                    else:
                        self.sheet_lastWeek.write(rowNum, colNum, clockout_time, self.lastWeek_clock_format)
                    # 列数+1
                    colNum += 1
                    # 写加班时间
                    # 由于上班时间9-10点,所以此处需要考虑上班时间早于9点和上班时间9-10点,上班时间10点以后的情况
                    overtime = ''
                    if clockout_time == '-':
                        self.sheet_lastWeek.write(rowNum, colNum, '-', self.lastWeek_overtime_format)
                    else:
                        clockin_h = clockin_time.split(':')[0]
                        clockin_m = clockin_time.split(':')[1]
                        clockout_h = clockout_time.split(':')[0]
                        clockout_m = clockout_time.split(':')[1]
                        # 需要判断当天状态,是正常/休息/还是上班.
                        # 若当天为节假日
                        if self.day_state[x[0]] == 1:
                            overtime_m = int(clockout_h) * 60 + int(clockout_m) - int(clockin_h) * 60 - int(clockin_m)
                            overtime_h = overtime_m // 60
                            if overtime_m - overtime_h * 60 > 30:
                                overtime = overtime_h + 0.5
                            else:
                                overtime = overtime_h
                        else:
                            # 若上班时间早于9点,则加班时间 = 下班时间分钟数 - 9点分钟数 - 9h
                            if int(clockin_h) < 9:
                                overtime_m = int(clockout_h) * 60 + int(clockout_m) - 9 * 60 - 9 * 60
                            # 若上班时间9-10点,则加班时间 = 下班时间分钟数 - 上班时间分钟数 - 9h
                            elif 540 <= int(clockin_h) * 60 + int(clockin_m) <= 600:
                                overtime_m = int(clockout_h) * 60 + int(clockout_m) - int(clockin_h) * 60 - int(
                                    clockin_m) - 9 * 60
                            # 若上班时间晚于10点,则加班时间 = 下班时间分钟数 - 10点分钟数 - 9h
                            elif 600 < int(clockin_h) * 60 + int(clockin_m):
                                overtime_m = int(clockout_h) * 60 + int(clockout_m) - 10 * 60 - 9 * 60
                            if overtime_m <= 0:
                                overtime = 0
                            else:
                                overtime_h = overtime_m // 60
                                if overtime_m - overtime_h * 60 > 30:
                                    overtime = overtime_h + 0.5
                                else:
                                    overtime = overtime_h
                        self.sheet_lastWeek.write(rowNum, colNum, overtime, self.lastWeek_overtime_format)
                theday_seconds += 86400
                # 行数+1,列数重置
                rowNum += 1
                colNum = p_x
            # 写"总计",包括两个空白内容单元格和一个统计加班时间单元格
            self.sheet_lastWeek.write(rowNum, colNum, '', self.lastWeek_leftColumn_formatc)
            colNum += 1
            self.sheet_lastWeek.write(rowNum, colNum, '', self.lastWeek_leftColumn_formatc)
            colNum += 1
            self.sheet_lastWeek.write_formula(rowNum, colNum, '=SUM(' + position_char_right  + '7:'+ position_char_right + '13)', self.lastWeek_total_format)
            # 行数+1,列数重置
            rowNum += 1
            colNum = p_x
            p_x += 3
            # 推出下一位的姓名所使用的单元格起始位置
            # 如果position_char_right字母为两位
            if len(position_char_right) > 1:
                # 判断第二位字母是否是Z以上的
                if ord(position_char_right[1]) > 89:
                    # 如果是,则字母第一位+1,字母第二位A
                    position_next_left = chr(ord(position_char_right[0]) + 1) + 'A'
                else:
                    # 如果不是,则字母第一位不变,字母第二位+1
                    position_next_left = position_char_right[0] + chr(ord(position_char_right[1]) + 1)
            # 如果字母为一位
            else:
                # 判断字母是否z以上
                if ord(position_char_right) > 89:
                    # 如果是,则字母第一位写A,字母第二位A
                    position_next_left = 'AA'
                else:
                    # 如果不是,则字母+1
                    position_next_left = chr(ord(position_char_right) + 1)
            p_left = position_next_left + p_left[-1]

    # 从data中取出每个人上周的考勤
    def lastWeek_data(self, data):
        # 取得当前时间的时间戳
        self.today_seconds = time.time()
        self.today_seconds_2 = self.today_seconds
        lastWeek_data = {}
        # 遍历data
        for j in data:
            # 初始化数据
            i = 7
            lastWeek_data[j] = []
            while i > 0:
                # 返回上一天的struct_time
                self.today_seconds_2 -= 86400
                theday_struct_time = time.localtime(self.today_seconds_2)
                # 返回上一天的具体日期
                theday_year = time.strftime('%Y', theday_struct_time)
                theday_month = time.strftime('%m', theday_struct_time)
                if theday_month[0] == '0':
                    theday_month = theday_month[1]
                theday_day = time.strftime('%d', theday_struct_time)
                if theday_day[0] == '0':
                    theday_day = theday_day[1]
                # 合并
                theday = theday_year + '-' + theday_month + '-' + theday_day
                try:
                    oneday_attendance = [theday,data[j][theday]['clockin_time'], data[j][theday]['clockout_time']]
                    lastWeek_data[j].insert(0, oneday_attendance)
                except Exception as e:
                    oneday_attendance = [theday, '-', '-']
                    lastWeek_data[j].insert(0, oneday_attendance)
                i -= 1
            self.today_seconds_2 = self.today_seconds
        return lastWeek_data

    def writeAttendanceSheet_thisMonth(self):
        # 合并单元格并写入第一行项目组名称
        self.sheet_thisMonth.merge_range('A1:K1', 'Tv游戏测试人员考勤统计', self.lastWeek_title_format)
        # 给定初始位置(A2),向下写每个人当月的考勤
        self.thisMonth_everyone(position_init='A2',data=self.data)

    def thisMonth_everyone(self, position_init, data):
        # 首先规定用户编号,从0开始
        user = 0
        # 规定指针坐标
        colNum = 0
        rowNum = 1
        # 调整列宽度
        while colNum < 11:
            self.sheet_thisMonth.set_column(chr(colNum + 65) + ':' + chr(colNum + 65), 10)
            colNum += 1
        # 重置指针
        colNum = 0
        # 判断本月第一周的第一天是礼拜几
        theday_flag = datetime.datetime(int(self.year),
                                   int(self.month), 1).strftime('%w')
        # 对于多个用户分批次处理.给予坐标
        for name in data:
            # 合并第一行,然后写姓名
            self.sheet_thisMonth.merge_range(position_init[0] + str(rowNum + 1) + ':K' + str(rowNum + 1), name.split('/')[1], self.thisMonth_name_format)
            # 第二行写标题,每写一格列数+1
            # 写月份
            rowNum += 1
            self.sheet_thisMonth.write(rowNum, colNum, self.month + '月', self.thisMonth_title_format)
            colNum += 1
            # 写其他
            for i in ['第1周', '加班小时数', '第2周', '加班小时数', '第3周', '加班小时数', '第4周', '加班小时数', '第5周', '加班小时数']:
                self.sheet_thisMonth.write(rowNum, colNum, i, self.thisMonth_title_format)
                colNum += 1
            colNum = 0
            rowNum += 1
            # 写'星期一'到'星期日'
            for i in ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']:
                self.sheet_thisMonth.write(rowNum, colNum, i, self.thisMonth_leftColumn_format)
                rowNum += 1
            # 计算当月天数
            if int(self.month) == 12:
                totalDays = (datetime.datetime((int(self.year) + 1), 1, 1) - datetime.datetime(int(self.year), 12, 1)).days
            else:
                totalDays = (datetime.datetime(int(self.year), (int(self.month) + 1), 1) - datetime.datetime(int(self.year), int(self.month), 1)).days
            # 从data中抽数据,从1号开始抽一直到最后一天
            theDay = 1
            # 先给个人区域所有原本应该填写时间的单元格全部写上空白数据
            colNum = 1
            rowNum = user * 11 + 3
            while colNum < 11:
                while rowNum < (user + 1) * 11:
                    self.sheet_thisMonth.write(rowNum, colNum, '', self.thisMonth_workTime_format)
                    colNum += 1
                    self.sheet_thisMonth.write(rowNum, colNum, '', self.thisMonth_overTime_format)
                    colNum -= 1
                    rowNum += 1
                rowNum = user * 11 + 3
                colNum += 2
            # 写数据
            rowNum = int(theday_flag) + 2 + user * 11
            colNum = 1
            while theDay < totalDays + 1:
                try:
                    # 取上班时间
                    clockin_time = data[name][self.year + '-' + str(int(self.month)) + '-' + str(theDay)]['clockin_time']
                    # 取下班时间
                    clockout_time = data[name][self.year + '-' + str(int(self.month)) + '-' + str(theDay)]['clockout_time']
                    clockin_h = clockin_time.split(':')[0]
                    clockin_m = clockin_time.split(':')[1]
                    clockout_h = clockout_time.split(':')[0]
                    clockout_m = clockout_time.split(':')[1]
                    # 判断是否周六日
                    isWeekend = datetime.datetime(int(self.year), int(self.month), theDay).weekday()
                    if isWeekend == 5 or isWeekend == 6:
                        # 需要判断当天状态,是正常/休息/还是上班.
                        # 若当天需要上班
                        if self.day_state[self.year + '-' + str(int(self.month)) + '-' + str(theDay)] == 2:
                            # 若上班时间早于9点
                            if int(clockin_h) < 9:
                                worktime_m = int(clockout_h) * 60 + int(clockout_m) - 9 * 60
                            # 若上班时间9-10点
                            elif 540 <= int(clockin_h) * 60 + int(clockin_m) <= 600:
                                worktime_m = int(clockout_h) * 60 + int(clockout_m) - int(clockin_h) * 60 - int(clockin_m)
                            # 若上班时间晚于10点
                            elif 600 < int(clockin_h) * 60 + int(clockin_m):
                                worktime_m = int(clockout_h) * 60 + int(clockout_m) - 10 * 60
                            worktime_h = worktime_m // 60
                            if worktime_m - worktime_h * 60 > 30:
                                worktime = worktime_h + 0.5
                            else:
                                worktime = worktime_h
                            overtime_m = worktime_m - 9 * 60
                            if overtime_m <= 0:
                                overtime = 0
                            else:
                                overtime_h = overtime_m // 60
                                if overtime_m - overtime_h * 60 > 30:
                                    overtime = overtime_h + 0.5
                                else:
                                    overtime = overtime_h
                        # 若当天放假或节假日
                        else:
                            worktime_m = int(clockout_h) * 60 + int(clockout_m) - int(clockin_h) * 60 - int(clockin_m)
                            worktime_h = worktime_m // 60
                            if worktime_m - worktime_h * 60 > 30:
                                worktime = worktime_h + 0.5
                            else:
                                worktime = worktime_h
                            overtime = worktime
                    else:
                        # 如果不是,根据爱奇艺的弹性上下班机制
                        # 需要判断当天状态,是正常/休息/还是上班.
                        # 若当天为节假日
                        if self.day_state[self.year + '-' + str(int(self.month)) + '-' + str(theDay)] == 1:
                            worktime_m = int(clockout_h) * 60 + int(clockout_m) - int(clockin_h) * 60 - int(clockin_m)
                            worktime_h = worktime_m // 60
                            if worktime_m - worktime_h * 60 > 30:
                                worktime = worktime_h + 0.5
                            else:
                                worktime = worktime_h
                            overtime = worktime
                        # 若当天正常上班
                        else:
                            # 若上班时间早于9点
                            if int(clockin_h) < 9:
                                worktime_m = int(clockout_h) * 60 + int(clockout_m) - 9 * 60
                            # 若上班时间9-10点
                            elif 540 <= int(clockin_h) * 60 + int(clockin_m) <= 600:
                                worktime_m = int(clockout_h) * 60 + int(clockout_m) - int(clockin_h) * 60 - int(
                                    clockin_m)
                            # 若上班时间晚于10点
                            elif 600 < int(clockin_h) * 60 + int(clockin_m):
                                worktime_m = int(clockout_h) * 60 + int(clockout_m) - 10 * 60
                            worktime_h = worktime_m // 60
                            if worktime_m - worktime_h * 60 > 30:
                                worktime = worktime_h + 0.5
                            else:
                                worktime = worktime_h
                            overtime_m = worktime_m - 9 * 60
                            if overtime_m <= 0:
                                overtime = 0
                            else:
                                overtime_h = overtime_m // 60
                                if overtime_m - overtime_h * 60 > 30:
                                    overtime = overtime_h + 0.5
                                else:
                                    overtime = overtime_h
                    self.sheet_thisMonth.write(rowNum, colNum, worktime, self.thisMonth_workTime_format)
                    colNum += 1
                    # 加班时间 = 上班时间 - 9h
                    self.sheet_thisMonth.write(rowNum, colNum, overtime, self.thisMonth_overTime_format)
                    colNum -= 1
                    rowNum += 1
                except Exception as e:
                    self.sheet_thisMonth.write(rowNum, colNum, '', self.thisMonth_workTime_format)
                    colNum += 1
                    self.sheet_thisMonth.write(rowNum, colNum, '', self.thisMonth_overTime_format)
                    colNum -= 1
                    rowNum += 1
                # 如果此时行数超出本人书写区域了,那就重置行数为本人书写区域的第3行,且列数+2
                if rowNum > (user + 1) * 11 - 2:
                    rowNum = user * 11 + 3
                    colNum += 2
                theDay += 1
            # 写'总计'行
            # '总计'
            colNum = 0
            rowNum = user * 11 + 10
            self.sheet_thisMonth.write(rowNum, colNum, '总计', self.thisMonth_leftColumn_format)
            colNum += 1
            while colNum < 11:
                # 第N周上班总计
                self.sheet_thisMonth.write_formula(rowNum, colNum,
                                                  '=SUM(' + str(chr(colNum + 65)) + str(rowNum - 6) + ':' + str(chr(colNum + 65)) + str(rowNum) + ')',
                                                  self.thisMonth_bottomTotal_format)
                colNum += 1
            # 写个人本月统计
            colNum = 0
            rowNum += 1
            # 合并AB列,写入文字:"本月工作小时数"
            self.sheet_thisMonth.merge_range('A' + str(rowNum + 1) + ':B' + str(rowNum + 1),
                                             '本月工作小时数：', self.thisMonth_totalworkTime_format)
            # 写本月工作小时数统计
            colNum = 2
            self.sheet_thisMonth.write_formula(rowNum, colNum,
                                               '=SUM(B' + str(rowNum) + ',D' + str(rowNum) + ',F' + str(rowNum) + ',H' + str(rowNum) + ',J' + str(rowNum) + ')',
                                               self.thisMonth_totalworkTime_format)
            # 合并DE列,写入文字:"本月加班小时数"
            self.sheet_thisMonth.merge_range('D' + str(rowNum + 1) + ':E' + str(rowNum + 1),
                                             '本月工作小时数：', self.thisMonth_totalworkTime_format)
            # 写本月工作小时数统计
            colNum = 5
            self.sheet_thisMonth.write_formula(rowNum, colNum,
                                               '=SUM(C' + str(rowNum) + ',E' + str(rowNum) + ',G' + str(rowNum) + ',I' + str(rowNum) + ',K' + str(rowNum) + ')',
                                               self.thisMonth_totalworkTime_format)
            # 写完所有后,重置指针,给下一个用
            colNum = 0
            user += 1
            rowNum = user * 11 + 1

    def create_xlsx(self):
        filename = 'D:\\python\\myhtml\\doc\\' +  '考勤统计' + self.date + '_' + self.day + str(random.randint(1,100)) + '.xlsx'
        self.myBook = xlsxwriter.Workbook(filename)
        # 格式准备
        self.lastWeek_title_format = self.myBook.add_format(
            {'font_name': '宋体', 'font_size': 20, 'align': 'left', 'valign': 'vcenter', 'bold': True})
        self.lastWeek_tips_format = self.myBook.add_format(
            {'font_name': '宋体', 'font_size': 11, 'align': 'left', 'valign': 'vcenter', 'text_wrap': 'auto'})
        self.lastWeek_name_format = self.myBook.add_format(
            {'font_name': '宋体', 'font_size': 11, 'align': 'center', 'valign': 'vcenter', 'text_wrap': 'auto',
             'border': 1})
        self.lastWeek_leftColumn_format = self.myBook.add_format(
            {'font_name': '宋体', 'font_size': 11, 'align': 'left', 'valign': 'vcenter', 'border': 1})
        self.lastWeek_leftColumnTitle_format = self.myBook.add_format(
            {'font_name': '宋体', 'font_size': 11, 'align': 'left', 'valign': 'vcenter', 'bg_color': '#538DD5',
             'border': 1})
        self.lastWeek_leftColumn_formatc = self.myBook.add_format(
            {'font_name': '宋体', 'font_size': 11, 'align': 'left', 'valign': 'vcenter', 'bg_color': '#B4C6E7',
             'border': 1})
        self.lastWeek_clock_format = self.myBook.add_format(
            {'font_name': '宋体', 'font_size': 10, 'align': 'right', 'valign': 'vcenter', 'bg_color': '#D9E1F2',
             'border': 1})
        self.lastWeek_overtime_format = self.myBook.add_format(
            {'font_name': '宋体', 'font_size': 10, 'align': 'right', 'valign': 'vcenter', 'bg_color': '#EDEDED',
             'border': 1})
        self.lastWeek_total_format = self.myBook.add_format(
            {'font_name': '宋体', 'font_size': 10, 'align': 'right', 'valign': 'vcenter', 'bg_color': '#B4C6E7',
             'border': 1})
        self.thisMonth_name_format = self.myBook.add_format(
            {'font_name': '宋体', 'font_size': 14, 'bold': True, 'align': 'left', 'valign': 'vcenter',
             'bg_color': '#C9C9C9', 'border': 1, 'border_color': '#FFFFFF'})
        self.thisMonth_title_format = self.myBook.add_format(
            {'font_name': '宋体', 'font_size': 11, 'align': 'left', 'valign': 'vcenter', 'bg_color': '#538DD5',
             'border': 1, 'border_color': '#FFFFFF'})
        self.thisMonth_leftColumn_format = self.myBook.add_format(
            {'font_name': '宋体', 'font_size': 11, 'align': 'left', 'valign': 'vcenter', 'bg_color': '#B4C6E7',
             'border': 1, 'border_color': '#FFFFFF'})
        self.thisMonth_bottomTotal_format = self.myBook.add_format(
            {'font_name': '宋体', 'font_size': 11, 'align': 'right', 'valign': 'vcenter', 'bg_color': '#B4C6E7',
             'border': 1, 'border_color': '#FFFFFF'})
        self.thisMonth_workTime_format = self.myBook.add_format(
            {'font_name': '宋体', 'font_size': 11, 'align': 'right', 'valign': 'vcenter', 'bg_color': '#D9E1F2',
             'border': 1, 'border_color': '#FFFFFF'})
        self.thisMonth_overTime_format = self.myBook.add_format(
            {'font_name': '宋体', 'font_size': 11, 'align': 'right', 'valign': 'vcenter', 'bg_color': '#EDEDED',
             'border': 1, 'border_color': '#FFFFFF'})
        self.thisMonth_totalworkTime_format = self.myBook.add_format(
            {'font_name': '宋体', 'font_size': 12, 'bold': True, 'align': 'right', 'valign': 'vcenter',
             'bg_color': '#C9C9C9'})
        self.sheet_lastWeek = self.myBook.add_worksheet('周统计')
        self.writeAttendanceSheet_lastWeek()
        self.sheet_thisMonth = self.myBook.add_worksheet(self.month + '月考勤统计')
        self.writeAttendanceSheet_thisMonth()
        self.myBook.close()
        return filename