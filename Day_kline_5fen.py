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

def create_Kline_Image(codes,days):
    Pa = Page()
    # Gd=Grid(init_opts=opts.InitOpts(width="700px",height='700px'))
    get_K = get_Kline()

    for num in range(0,len(codes)):
        time_list, data_list = [], []
        datalist0=get_K.getKline(days[num],days[num],codes[num])
        datalist=get_K.testgetKline(days[num],days[num],codes[num],'5')
        for index in datalist:
            time_list.append(index[1][8:12])
            data_list.append(index[3][0:5])
            c=(
                    # Line(init_opts=opts.InitOpts(width="500px",height='500px'))
                    Line()
                    .add_xaxis(time_list)
                    .add_yaxis(codes[num],
                               data_list,
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
                        title_opts=opts.TitleOpts(title=datalist0[0][6]),
                    )
            )
        Pa.add(c)
    Pa.render('2020-02-01'+'.html')

    get_K.bs_close()
create_Kline_Image(['000908','000155','002455'],['2021-04-30','2021-05-10','2021-07-26'])