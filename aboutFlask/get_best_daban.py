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

#daban_zd游资机构共同参与的每天涨停板/跌停板,目前最好的策略了
def data_analysis_youzi():
    #yesterday = datetime.date.today() + datetime.timedelta(-1)
    #day1=str(yesterday)
    #day2=str(yesterday)
    db = pymysql.connect("47.111.24.112", "root", "withme_321", "test")
    cursor = db.cursor()
    get_K = get_Kline()
    day_code="SELECT DISTINCT date from daban_zd  ORDER BY date desc limit 1"
    cursor.execute(day_code)
    day_list = cursor.fetchall()
    success,fail,money,x=0,0,100000,0
    for day in day_list:
        sql_code="SELECT date,code,stockname,price,shizhi,orderamount,highdays,limittype FROM daban_zd where updown>0 and code like'00%%' and date='%s' ORDER BY turn desc limit 1"%day[0]
        cursor.execute(sql_code)
        code_list = cursor.fetchall()
        for stock in code_list:
            code=stock[1]
            name=stock[2]
            # 给出今天的建议买入的股票
            data_list = get_K.getKline(str(day[0]), str(day[0] + datetime.timedelta(15)), code)
            string_end = '今天操作：早盘竞价阶段挂涨停价卖昨日打板票；买入%s，开盘价小于%s，则以开盘价买入，否则以%s价格挂单'%(name,float(data_list[0][5])*0.989,float(data_list[0][5]))
            print(string_end)
            return string_end
            
