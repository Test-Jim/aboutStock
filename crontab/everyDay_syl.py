#此文件功能：下载daban_zd表里中小盘股票的‘算法上的’收益率
import baostock as bs
import datetime
import pymysql
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

def syl_ruku():
    db = pymysql.connect("47.111.24.112", "root", "withme_321", "test")
    cursor = db.cursor()
    get_K = get_Kline()
    sql0="SELECT DISTINCT date FROM daban_zd  ORDER BY date desc limit 3"
    cursor.execute(sql0)
    day_list = cursor.fetchall()
    sql1="SELECT date,code from daban_zd WHERE updown >0 and code like'00%%' and date='%s'"%str(day_list[2][0])
    cursor.execute(sql1)
    end_list = cursor.fetchall()
    for index in end_list:
        code=index[1]
        day=index[0]
        data_list = get_K.getKline(str(day), str(day + datetime.timedelta(15)), code)
        # print(data_list)
        sell_day = data_list[2][0]  # 卖的日期

        data_list3 = get_K.testgetKline(sell_day, sell_day, code, '5')
        if data_list3 == []: continue
        sell_price=float(data_list3[29][3])

        if float(data_list[1][2]) < float(data_list[1][6]):
            buy_price = float(data_list[1][2])
        elif float(data_list[1][4]) <= float(data_list[1][6]) < float(data_list[1][3]):  # 今日最低<上一日收盘价<今日最高
            buy_price = float(data_list[1][6])  # 买价，T日开盘价
        else:continue  # 找不到买价就退出循环
        syl = "%.2f%% " % ((sell_price - buy_price) / buy_price * 100)  # 收益率
        print(syl,code,day)
        sql2="update daban_zd set syl='%s' where date='%s'and code='%s'"%(syl,day,code)
        cursor.execute(sql2)
        db.commit()

    get_K.bs_close()
    db.close()
syl_ruku()
