#此文件功能：从daban表里查找需要的游资股票，然后丰富股票数据
import pymysql
import baostock as bs
import datetime
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

db = pymysql.connect("47.111.24.112", "root", "withme_321", "test")
cursor = db.cursor()
get_K = get_Kline()

def every_day():
    date=datetime.date.today()
    sql_code = "select DISTINCT code from daban WHERE date='%s' and  code not like '300___'  and  code not like '688___' and code not like '9%%'"%date
    cursor.execute(sql_code)
    code_list = cursor.fetchall()
    for index in code_list:
        begin_date=str(date)
        end_date=str(date)
        code=index[0]
        #print(code)
        data_list=get_K.getKline(begin_date,end_date,code)
        # print(data_list)
        amount=str(float(data_list[0][8])//10000)+'万'
        updown='%.3f' % float(data_list[0][10])
        data_tup=(data_list[0][0],code,updown,data_list[0][2] , data_list[0][3], data_list[0][4], data_list[0][5], data_list[0][9],amount)
        sql_data="INSERT INTO t_stock VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%data_tup
        # print(sql_data)
        cursor.execute(sql_data)
        db.commit()
    get_K.bs_close()
    db.close()

every_day()
