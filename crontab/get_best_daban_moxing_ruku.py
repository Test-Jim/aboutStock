import pymysql
import datetime
import baostock as bs

class get_Kline(object):
    def __init__(self):
        self.lg = bs.login()
    def getKline(self,beginDate,endDate,code):
        if code[0] == '0':code = "sz." + code
        if code[0] == '6':code = 'sh.' + code
        if code[0] == '3':code = 'sz.' + code
        if code[0] == '2':code = 'sz.' + code
        if code[0] == '9':code = 'sh.' + code
        rs = bs.query_history_k_data_plus(code,
                                          "date,code,open,high,low,close,preclose,volume,amount,turn,pctChg",
                                          start_date=beginDate, end_date=endDate,
                                          frequency="d", adjustflag="2")
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        # print(data_list)
        return data_list

    def testgetKline(self,beginDate, endDate, code,k):
        if code[0] == '0':code = "sz." + code
        if code[0] == '6':code = 'sh.' + code
        if code[0] == '3':code = 'sz.' + code
        if code[0] == '2':code = 'sz.' + code
        if code[0] == '9':code = 'sh.' + code
        rs = bs.query_history_k_data_plus(code,
                                          "date,time,code,open,high,low,close,volume,amount",
                                          start_date=beginDate, end_date=endDate,
                                          frequency=k, adjustflag="2")
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        return data_list
    def bs_close(self):
        bs.logout()

#1、2、3换手 不过滤上影线 倍数1
def data_analysis_youzi(day1,day2):
    db = pymysql.connect("47.111.24.112", "root", "withme_321", "test")
    cursor = db.cursor()
    get_K = get_Kline()
    day_code="SELECT DISTINCT date from daban_zd where date>='%s' and date<='%s' ORDER BY date"%(day1,day2)
    cursor.execute(day_code)
    day_list = cursor.fetchall()


    for day in day_list:
        sql_code="SELECT date,code,stockname,price ,turn FROM daban_zd where updown>0 and code like'00%%' and date='%s' ORDER BY turn desc "%day[0]
        cursor.execute(sql_code)
        code_list = cursor.fetchall()
        for key in range(0,len(code_list)):
            code=code_list[key][1]
            price=code_list[key][3]
            turn=code_list[key][4]
            data_list = get_K.getKline(str(day[0]), str(day[0] + datetime.timedelta(15)), code)

            buy_day = data_list[1][0]  # 买的日期
            sell_day = data_list[2][0]  # 卖的日期
            #5分钟为单位的K线
            data_list3 = get_K.testgetKline(sell_day, sell_day, code, '5')
            if data_list3 == []: continue
            try:
                if float(data_list[1][2]) < float(data_list[1][6]):
                    buy_price = float(data_list[1][2])
                elif float(data_list[1][4]) <= float(data_list[1][6])< float(data_list[1][3]):  # 今日最低<上一日收盘价<今日最高
                    buy_price = float(data_list[1][6]) # 买价，T日开盘价
                else:continue#找不到买价就退出循环
                data_list2=[]
                data_list2_2 = get_K.getKline(str(day[0] + datetime.timedelta(-25)), str(day[0]), code)
                for index in data_list2_2:
                    if index[9]!='':data_list2.append(index)
                day_four = [round(float(data_list2[-1][2]),2), round(float(data_list2[-1][5]),2), round(float(data_list2[-1][4]),2),round(float(data_list2[-1][3]),2)]
                day_three = [round(float(data_list2[-2][2]),2), round(float(data_list2[-2][5]),2), round(float(data_list2[-2][4]),2),round(float(data_list2[-2][3]),2)]
                day_two = [round(float(data_list2[-3][2]),2), round(float(data_list2[-3][5]),2), round(float(data_list2[-3][4]),2),round(float(data_list2[-3][3]),2)]
                day_one = [round(float(data_list2[-4][2]),2), round(float(data_list2[-4][5]),2), round(float(data_list2[-4][4]),2),round(float(data_list2[-4][3]),2)]
                model = moxing(day_one, day_two, day_three, day_four)
                # sell_price = float(data_list3[29][3])  # 13点25分开盘价作为卖价
                # syl = "%.2f%% " % ((sell_price - buy_price) / buy_price * 100)  # 收益率
                updatesql="UPDATE daban_zd set model='%s' WHERE code='%s' and date='%s'"%(model,code,day[0])
                cursor.execute(updatesql)
                # print(updatesql)
            except:
                pass
        db.commit()
    cursor.close()
    get_K.bs_close()


def data_analysis_youzi_today_ruku():
    db = pymysql.connect("47.111.24.112", "root", "withme_321", "test")
    cursor = db.cursor()
    get_K = get_Kline()

    sql0="SELECT DISTINCT date FROM daban_zd  ORDER BY date desc limit 1"
    cursor.execute(sql0)
    day_list = cursor.fetchall()


    sql_code = "SELECT date,code,stockname,price ,turn FROM daban_zd where updown>0 and code like'00%%' and date='%s' order by turn desc" % str(day_list[0][0])
    cursor.execute(sql_code)
    code_list = cursor.fetchall()

    for stock in code_list:
        day=stock[0]
        code=stock[1]
        data_list2=[]
        data_list2_2= get_K.getKline(str(day + datetime.timedelta(-30)), str(day), code)

        for index in data_list2_2:
            if index[9] != '': data_list2.append(index)
        print(data_list2)
        day_four = [round(float(data_list2[-1][2]), 2), round(float(data_list2[-1][5]), 2),
                    round(float(data_list2[-1][4]), 2), round(float(data_list2[-1][3]), 2)]
        day_three = [round(float(data_list2[-2][2]), 2), round(float(data_list2[-2][5]), 2),
                     round(float(data_list2[-2][4]), 2), round(float(data_list2[-2][3]), 2)]
        day_two = [round(float(data_list2[-3][2]), 2), round(float(data_list2[-3][5]), 2),
                   round(float(data_list2[-3][4]), 2), round(float(data_list2[-3][3]), 2)]
        day_one = [round(float(data_list2[-4][2]), 2), round(float(data_list2[-4][5]), 2),
                   round(float(data_list2[-4][4]), 2), round(float(data_list2[-4][3]), 2)]

        model = moxing(day_one, day_two, day_three, day_four)
        updatesql = "UPDATE daban_zd set model='%s' WHERE code='%s' and date='%s'" % (model, code,day)
        cursor.execute(updatesql)
        db.commit()
    cursor.close()
    get_K.bs_close()
def moxing(one,two,three,four):
    open1=one[0]
    close1=one[1]
    low1=one[2]
    high1=one[3]
    open2=two[0]
    close2=two[1]
    low2=two[2]
    high2 = two[3]
    open3=three[0]
    close3=three[1]
    low3=three[2]
    high3 = three[3]
    open4=four[0]
    close4=four[1]
    low4=four[2]
    high4 = four[3]
    if open1==close1==low1==high1 and open2==close2==low2==high2 and open3==close3==low3==high3 and open4==close4==low4==high4:return('1234天一字')
    if open1 == close1 == low1==high1 and open2 == close2 == low2==high2 and open3 == close3 == low3==high3: return ('123天一字')
    if open1 == close1 == low1==high1 and open2 == close2 == low2==high2 and open4 == close4 == low4==high4: return ('124天一字')
    if open1 == close1 == low1==high1 and open3 == close3 == low3==high3 and open4 == close4 == low4==high4: return ('134天一字')
    if open3 == close3 == low3==high3 and open2 == close2 == low2==high2 and open4 == close4 == low4==high4: return ('234天一字')
    if open1 == close1 == low1==high1 and open2 == close2 == low2==high2: return ('12天一字')
    if open1 == close1 == low1==high1 and open3 == close3 == low3==high3: return ('13天一字')
    if open1 == close1 == low1==high1 and open4 == close4 == low4==high4: return ('14天一字')
    if open2 == close2 == low2==high2 and open3 == close3 == low3==high3: return ('23天一字')
    if open2 == close2 == low2==high2 and open4 == close4 == low4==high4: return ('24天一字')
    if open3 == close3 == low3==high3 and open4 == close4 == low4==high4: return ('34天一字')
    if open1==close1==low1==high1:return('1天一字')
    if open2 == close2 == low2==high2: return ('2天一字')
    if open3 == close3 == low3==high3: return ('3天一字')
    if open4 == close4 == low4==high4: return ('4天一字')
    x,y,z,s=one[0:2],two[0:2],three[0:2],four[0:2]
    x.sort()
    y.sort()
    z.sort()
    s.sort()
    # print(x,y,z,s)
    if min(open3, close3) > max(open2, close2) > max(open1, close1):
        if max(x[0], y[0]) > min(x[1], y[1]) and max(y[0], z[0]) > min(y[1], z[1]): return ('箱体阶梯上升')
    if max(x[0], y[0]) <= min(x[1], y[1]) and max(y[0], z[0]) <= min(y[1], z[1]) and max(x[0], z[0]) <= min(x[1], z[1]):
        if (close4 - open4) > abs(close1 - open1) * 3 and open4 < close3:
            return ('三横四阳,3倍超10')
        else:
            return ('三横四阳')
    if max(y[0], z[0]) <= min(y[1], z[1]) and max(z[0], s[0]) <= min(z[1], s[1]) and max(y[0], s[0]) <= min(y[1], s[1]):
        if max(x[0], z[0]) > min(x[1], z[1]) and y[1] > x[1]: return ('大厂型')
    if max(x[0], y[0]) <= min(x[1], y[1]) and y[0] < z[1]: return ('倒厂型')
    if max(y[0], z[0]) <= min(y[1], z[1]) and max(x[0], y[0]) > min(x[1], y[1]) and y[1] > x[1]: return ('梯形')
    if close1 > close2 > close3: return ('左长')
    if close1 > close2 >= close3 and x[1] > s[1]: return ('左长')
    if close4 > close3 > close2 and x[0] > y[1]: return ('右长')
    if close1 > close2 >= close3 and x[1] < s[1]: return ('右长')
    if y[1] > x[1] and y[0] > x[0] and max(y[0], z[0]) > min(y[1], z[1]) and y[0] > z[1]: return ('波动')
    # if max(x[0],y[0])>min(x[1],y[1]) and y[0]>x[1] and max(y[0],z[0])>min(y[1],z[1]) and y[0]>z[1]:return ('波动')
data_analysis_youzi_today_ruku()

# def one_year_zdNum():
#     db = pymysql.connect("47.111.24.112", "root", "withme_321", "test")
#     cursor = db.cursor()
#     get_K = get_Kline()
#     day_code="select date,code from daban_zd where model is not null"
#     cursor.execute(day_code)
#     stock_list = cursor.fetchall()
#     for stock in stock_list:
#         day=stock[0]
#         code=stock[1]
#         data_list = get_K.getKline(str(day+ datetime.timedelta(-365)), str(day), code)
#         banshu = 1
#         for data in data_list:
#             if float(data[10])>9.4:banshu+=1
#         updatesql="UPDATE daban_zd set zt_num='%s' WHERE code='%s' and date='%s'"%(banshu,code,day)
#         cursor.execute(updatesql)
#         db.commit()
#     cursor.close()
#     get_K.bs_close()
# one_year_zdNum()
