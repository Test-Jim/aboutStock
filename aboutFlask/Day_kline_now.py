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

def create_Kline_Image():
    Pa = Page()
    # Gd=Grid(init_opts=opts.InitOpts(width="700px",height='700px'))
    db = pymysql.connect("47.111.24.112", "root", "withme_321", "test")
    cursor = db.cursor()
    get_K = get_Kline()
    day_sql="SELECT DISTINCT date from daban_zd  ORDER BY date DESC limit 1"
    cursor.execute(day_sql)
    day_list = cursor.fetchall()
    for day in day_list:
        sql_code = "SELECT date,code,stockname,price FROM daban_zd where updown>0 and code like'00%%' and date='%s' ORDER BY turn desc limit 3" % \
                   day[0]
        cursor.execute(sql_code)
        code_list = cursor.fetchall()
        for stock in code_list:
            code = stock[1]
            name = stock[2]
            # trade_day=stock[0]
            # if str(trade_day) not in ['2020-02-14','2020-02-17','2020-02-27','2020-03-03','2020-03-09','2020-04-03','2020-04-17','2020-04-22','2020-05-14','2020-05-27','2020-06-05','2020-06-11','2020-06-29','2020-07-20','2020-07-29','2020-07-30','2020-08-03','2020-08-06','2020-08-07','2020-09-18','2020-11-13','2020-11-16','2020-12-16','2020-12-24','2021-01-12','2021-02-26','2021-03-15','2021-04-28','2021-04-30','2021-05-13','2021-05-26','2021-05-27']:continue
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

            data=[[open00,close00,low00,high00],[open0,close0,low0,high0],[open1,close1,low1,high1],[open2,close2,low2,high2]]
            # data=[close00,close0,close1,close2,close3,close4]
            daylist=[day00,day0,day1,day2]


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
                        title_opts=opts.TitleOpts(title=data_list2[0][9][0:5]+'遵守纪律'),
                    )
            )
            Pa.add(c)
    Pa.render('templates/threeImage.html')
    cursor.close()
    get_K.bs_close()




