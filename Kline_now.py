#画一般的K线的地方
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
    for day in day_list:
        sql_code = "SELECT date,code,stockname,price,highdays FROM daban_zd where updown>0 and code like'00%%' and date='%s' ORDER BY turn desc limit 2" % \
                   day[0]
        cursor.execute(sql_code)
        code_list = cursor.fetchall()
        code_list=list(code_list)
        del code_list[0]
        for stock in code_list:
            code = stock[1]
            name = stock[2]
            highdays=stock[4]
            # trade_day=stock[0]
            # if str(trade_day) not in ['2019-01-28','2019-02-14','2019-06-27','2019-08-19','2019-08-23','2019-09-05','2019-10-15','2019-10-28','2019-11-04','2020-02-03','2020-02-07','2020-02-10','2020-06-02','2021-07-01']:continue
            data_list1 = get_K.getKline(str(day[0]+datetime.timedelta(-15)),str(day[0]), code)
            data_list2=get_K.getKline(str(day[0]),str(day[0]+datetime.timedelta(15)), code)
            # print(stock)
            try:
                day00=data_list1[-4][0]
                open00=float('%.2f' % float(data_list1[-4][2]))
                high00=float('%.2f' % float(data_list1[-4][3]))
                low00=float('%.2f' % float(data_list1[-4][4]))
                close00=float('%.2f' % float(data_list1[-4][5]))
            except:
                day00 =0
                open00=0
                high00=0
                low00=0
                close00=0
            try:
                day0=data_list1[-3][0]
                open0=float('%.2f' % float(data_list1[-3][2]))
                high0=float('%.2f' % float(data_list1[-3][3]))
                low0=float('%.2f' % float(data_list1[-3][4]))
                close0=float('%.2f' % float(data_list1[-3][5]))
            except:
                day0=0
                open0=0
                high0=0
                low0=0
                close0=0
            day1=data_list1[-2][0]
            open1=float('%.2f' % float(data_list1[-2][2]))
            high1=float('%.2f' % float(data_list1[-2][3]))
            low1=float('%.2f' % float(data_list1[-2][4]))
            close1=float('%.2f' % float(data_list1[-2][5]))
            day2=data_list2[0][0]
            open2=float('%.2f' % float(data_list2[0][2]))
            high2=float('%.2f' % float(data_list2[0][3]))
            low2=float('%.2f' % float(data_list2[0][4]))
            close2=float('%.2f' % float(data_list2[0][5]))
            day3=data_list2[1][0]
            open3=float('%.2f' % float(data_list2[1][2]))
            high3=float('%.2f' % float(data_list2[1][3]))
            low3=float('%.2f' % float(data_list2[1][4]))
            close3=float('%.2f' % float(data_list2[1][5]))
            day4=data_list2[2][0]
            open4=float('%.2f' % float(data_list2[2][2]))
            high4=float('%.2f' % float(data_list2[2][3]))
            low4=float('%.2f' % float(data_list2[2][4]))
            close4=float('%.2f' % float(data_list2[2][5]))
            data=[[open00,close00,low00,high00],[open0,close0,low0,high0],[open1,close1,low1,high1],[open2,close2,low2,high2],[open3,close3,low3,high3],[open4,close4,low4,high4]]
            # data=[close00,close0,close1,close2,close3,close4]
            daylist=[day00,day0,day1,day2,day3,day4]

            if float(data_list2[1][2]) < float(data_list2[1][6]):
                buy_price = float(data_list2[1][2])
            elif float(data_list2[1][4]) <= float(data_list2[1][6]) < float(data_list2[1][3]):  # 今日最低<上一日收盘价<今日最高
                buy_price = float(data_list2[1][6])  # 买价，T日开盘价
            else:
                break
            sell_day=data_list2[2][0]
            # if float(data_list2[2][3]) > float(data_list2[2][6]) * 1.095:sell_price = float(data_list2[2][3])
            # else:sell_price = float(data_list2[2][5])  # 挂涨停价，没卖掉就收盘价卖
            data_list3 = get_K.testgetKline(sell_day, sell_day, code, '5')
            if data_list3 == []: continue
            sell_price = float(data_list3[29][3])  # 13点25分开盘价作为卖价

            buy_close=float(data_list2[1][5])#买那天的收盘价
            if buy_price>buy_close:string1='先跌'
            else:string1='先涨'
            if buy_close>sell_price:string2='再跌'
            else:string2='再涨'
            syl="%.2f%% "%((sell_price-buy_price)/buy_price*100)#收益率

            c=(
                    # Line(init_opts=opts.InitOpts(width="500px",height='500px'))
                    Kline(init_opts=opts.InitOpts(width="500px",height='500px'))
                    .add_xaxis(daylist)
                    .add_yaxis(name,
                               data,
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
                        title_opts=opts.TitleOpts(title=str(syl)+(string1+string2)+highdays),
                    )
            )
            Pa.add(c)
    Pa.render('ccc.html')
    cursor.close()
    get_K.bs_close()
create_Kline_Image('2021-07-27','2021-08-09')