import pyecharts.options as opts
from pyecharts.charts import Kline,Line
import baostock as bs
import pymysql
import datetime
from pyecharts.charts import Page,Grid

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

def create_Kline_Image(day1,day2):
    Pa = Page()
    # Gd=Grid(init_opts=opts.InitOpts(width="700px",height='700px'))
    db = pymysql.connect("47.111.24.112", "root", "withme_321", "test")
    cursor = db.cursor()
    get_K = get_Kline()
    day_code = "SELECT DISTINCT date from daban_zd where date>='%s' and date<='%s' ORDER BY date" % (day1, day2)
    cursor.execute(day_code)
    day_list = cursor.fetchall()
    money=100000
    daylist = []
    syl_list = []  # 收益率
    yue_list = []  # 余额
    for day in day_list:
        sql_code = "SELECT date,code,stockname,price FROM daban_zd where updown>0 and code like'00%%' and date='%s' ORDER BY turn desc limit 1" % \
                   day[0]
        cursor.execute(sql_code)
        code_list = cursor.fetchall()
        # code_list=list(code_list)
        # del code_list[0]

        for stock in code_list:
            code = stock[1]
            name = stock[2]
            # trade_day=stock[0]
            # if str(trade_day) not in ['2020-02-14','2020-02-17','2020-02-27','2020-03-03','2020-03-09','2020-04-03','2020-04-17','2020-04-22','2020-05-14','2020-05-27','2020-06-05','2020-06-11','2020-06-29','2020-07-20','2020-07-29','2020-07-30','2020-08-03','2020-08-06','2020-08-07','2020-09-18','2020-11-13','2020-11-16','2020-12-16','2020-12-24','2021-01-12','2021-02-26','2021-03-15','2021-04-28','2021-04-30','2021-05-13','2021-05-26','2021-05-27']:continue
            # data_list1 = get_K.getKline(str(day[0]+datetime.timedelta(-15)),str(day[0]), code)
            data_list2=get_K.getKline(str(day[0]),str(day[0]+datetime.timedelta(15)), code)

            if float(data_list2[1][2]) < float(data_list2[1][6]) * 0.989:
                buy_price = float(data_list2[1][2])
            elif float(data_list2[1][4]) <= float(data_list2[1][6]) < float(data_list2[1][3]):  # 今日最低<上一日收盘价<今日最高
                buy_price = float(data_list2[1][6])  # 买价，T日开盘价
            else:break
            if float(data_list2[2][3]) > float(data_list2[2][6]) * 1.095:sell_price = float(data_list2[2][3])
            else:sell_price = float(data_list2[2][5])  # 挂涨停价，没卖掉就收盘价卖
            # buy_close=float(data_list2[1][5])#买那天的收盘价
            # if buy_price>buy_close:string1='先跌'
            # else:string1='先涨'
            # if buy_close>sell_price:string2='再跌'
            # else:string2='再涨'
            # syl="%.2f%% "%((sell_price-buy_price)/buy_price*100)#收益率
            # syl =str(((sell_price - buy_price) / buy_price*100 ))[0:5]  # 收益率
            money = money * (1 + (sell_price - buy_price) / buy_price) * 0.9985

            yue_list.append(money)
            daylist.append(data_list2[2][0])


    print(yue_list)
    c=(
            Line()
            # Kline(init_opts=opts.InitOpts(width="500px",height='500px'))
            .add_xaxis(daylist)
            .add_yaxis('余额',
                       yue_list,
                       itemstyle_opts=opts.ItemStyleOpts(
                       color="#ec0000",
                       color0="#00da3c",
                       border_color="#8A0000",
                       border_color0="#008F28",
                       # borderWidth="10px",
                )
            )
            .set_global_opts(
                xaxis_opts=opts.AxisOpts(is_scale=True),
                yaxis_opts=opts.AxisOpts(
                    is_scale=True,
                    splitarea_opts=opts.SplitAreaOpts(
                        is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=0.5)
                    ),
                ),
                title_opts=opts.TitleOpts(title='余额折线图'),
            )
    )
    Pa.add(c)
    Pa.render('yueline.html')
    cursor.close()
    get_K.bs_close()

create_Kline_Image('2020-01-22','2021-02-02')


