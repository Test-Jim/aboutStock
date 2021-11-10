import pymysql
import baostock as bs
import datetime
#T日，买价，T-1日收盘价*0.99，买不进就不操作。卖价：T+1日，2点56接近收盘价
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
def get_best_choice():
    get_K = get_Kline()
    db = pymysql.connect("47.111.24.112", "root", "withme_321", "test")
    cursor = db.cursor()

    oneday_sql = "select  DISTINCT date from bs  ORDER BY date DESC limit 1"
    cursor.execute(oneday_sql)
    ndays = cursor.fetchall()


    success, fail, money,k = 0, 0, 100000,0
    sql_date="SELECT DISTINCT date from bs where date>='%s' and date<='%s' ORDER BY date"%(str(ndays[0][0]),str(ndays[0][0]))
    cursor.execute(sql_date)
    num_days = cursor.fetchall()
    for day in num_days:
        sql_buy = "select  date,name,code from bs where type =1 and date='%s' ORDER BY date DESC LIMIT 10"%day[0]
        cursor.execute(sql_buy)
        tup_buy = cursor.fetchall()
        # print(tup_buy)
        for index in tup_buy:
            name=index[1]
            code=index[2]
            if code[0:2]!='60':continue
            if '贵州茅台'==name:continue#不买茅台
            if '银行' in name:continue#不买银行类
            if '中国平安' ==name:continue#不买中国平安
            if '证券'in name:continue#不买证券
            #获取K线数据
            data_list=get_K.getKline(str(day[0]),str(day[0]+datetime.timedelta(15)),code)
            #给出今天的建议买入的股票
            if str(day[0]) == str(ndays[0][0]):
                string_end='今天操作：买入%s，挂单价：%s   然后2点56全仓卖出昨日股票' % (name,float(data_list[0][5])*0.989)
                print(string_end)
                db.close()
                get_K.bs_close()
                return string_end
            try:#在买，卖价这边，最后两天会数组越界，所以加异常处理
                if float(data_list[1][2])<float(data_list[1][6])*0.99:buy_price=float(data_list[1][2])
                elif float(data_list[1][4])<=float(data_list[1][6])*0.99<float(data_list[1][3]):#   今日最低<上一日收盘价<今日最高
                    buy_price = float(data_list[1][6])*0.99# 买价，T日开盘价
                else:continue
                # buy_price = float(data_list[1][6])
                buy_day = data_list[1][0]  # 买的日期
                #卖价为开盘价
                sell_price=float(data_list[2][5])#卖价，T+1日开盘价
                if sell_price>buy_price:
                    success+=1
                    print("在T日%s：%s操作成功。买价：%s    卖价%s" % (buy_day,name,buy_price,sell_price))
                else:
                    fail+=1
                    print("在T日%s：%s操作失败。买价：%s    卖价%s" % (buy_day,name,buy_price,sell_price))
                money = money*(1+(sell_price-buy_price)/buy_price)*0.9985
                print(money, success, fail,k)
            except:
                print('数组越界')
            break
    db.close()
    get_K.bs_close()
# oneday_sql="select  DISTINCT date from bs  ORDER BY date DESC limit 1"
# cursor.execute(oneday_sql)
# num_days = cursor.fetchall()
# get_best_choice(str(num_days[0][0]),str(num_days[0][0]))#end_day是前一个交易日，可以给出今天的买入建议
