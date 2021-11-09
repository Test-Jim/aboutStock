import pymysql
import datetime
import baostock as bs
import configparser,json

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

#liangbi_zd游资机构共同参与的每天量比榜
def data_analysis_youzi(day1,day2):
    db = pymysql.connect("47.111.24.112", "root", "withme_321", "test")
    cursor = db.cursor()
    get_K = get_Kline()
    day_code="SELECT DISTINCT date from liangbi_zd where date>='%s' and date<='%s' ORDER BY date"%(day1,day2)
    cursor.execute(day_code)
    day_list = cursor.fetchall()
    success,fail,money,daylist,daylist2=0,0,50000,[],[]
    num1,num2=0,0
    for day in day_list:
        sql_code="SELECT date,code,stockname FROM liangbi_zd where code like'00%%'  and date='%s' ORDER BY liangbi desc limit 1"%day[0]
        cursor.execute(sql_code)
        code_list = cursor.fetchall()
        # code_list=list(code_list)
        # del code_list[0]
        for key in range(0,len(code_list)):
            code=code_list[key][1]
            name=code_list[key][2]
            trade_day=code_list[key][0]
            data_list = get_K.getKline(str(day[0]), str(day[0] + datetime.timedelta(15)), code)
            buy_day = data_list[1][0]  # 买的日期
            sell_day = data_list[2][0]  # 卖的日期
            # 5分钟为单位的K线
            data_list3 = get_K.testgetKline(sell_day, sell_day, code, '5')
            if data_list3 == []: continue
            if float(data_list[1][2]) < float(data_list[1][6]):
                buy_price = float(data_list[1][2])
            elif float(data_list[1][4]) <= float(data_list[1][6]) < float(data_list[1][3]):  # 今日最低<上一日收盘价<今日最高
                buy_price = float(data_list[1][6])  # 买价，T日开盘价
            else:break
            sell_price = float(data_list3[29][3])
            # sell_price=float(data_list[2][5])
            if sell_price > buy_price:
                success += 1
                print("在T日%s：%s操作成功。买价：%s    卖价%s" % (buy_day, name, buy_price, sell_price))
            else:
                fail += 1
                print("在T日%s：%s操作失败。买价：%s    卖价%s" % (buy_day, name, buy_price, sell_price))

            money = money * (1 + (sell_price - buy_price) / buy_price) * 0.9985
            syl = "%.2f%% " % ((sell_price - buy_price) / buy_price * 100)  # 收益率
            print(success, fail, syl, money)
            break
    cursor.close()
    get_K.bs_close()

data_analysis_youzi('2020-01-01','2021-08-06')

