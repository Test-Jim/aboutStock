#此文件功能：下载每天龙虎榜数据到daban表内
import requests
import re
import pymysql
import datetime
import baostock as bs
s=requests.session()
#K线接口类
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
                                          frequency="d", adjustflag="3")
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        # print(data_list)
        return data_list
    def bs_close(self):
        bs.logout()
def testgetKline(beginDate,endDate,code):
    import pandas as pd
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    # print('login respond error_code:' + lg.error_code)
    # print('login respond  error_msg:' + lg.error_msg)
    #### 获取沪深A股历史K线数据 ####
    # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
    # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
    # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
    if code[0:2]=='00':
        code="sz."+code
    if code[0:2]=='60':
        code='sh.'+code
    if code[0:2]=='30':
        code='sz.'+code
    if code[0:2]=='68':
        code = 'sh.' + code
    if code[0:2]=='20':
        code = 'sz.' + code
    if code[0:1]=='9':
        code = 'sh.' + code
    rs = bs.query_history_k_data_plus(code,
                                      "date,code,open,high,low,close,preclose,volume,amount,turn,pctChg",
                                          start_date=beginDate, end_date=endDate,
                                          frequency="d", adjustflag="3")
    # print('query_history_k_data_plus respond error_code:' + rs.error_code)
    # print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)
    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    # result = pd.DataFrame(data_list, columns=rs.fields)
    # print(result)
    #### 结果集输出到csv文件 ####
    # result.to_csv("D:\\history_A_stock_k_data.csv", index=False)
    for index in data_list:
        print(index)
    bs.logout()
    return data_list
#下载龙虎榜数据
def daban():
    db = pymysql.connect("47.111.24.112", "root", "withme_321", "test")
    cursor = db.cursor()
    # date = datetime.datetime.strptime('2021-01-22', '%Y-%m-%d').date()
    today = datetime.date.today()
    get_K = get_Kline()
    for i in range(1,2):
        # num_day = datetime.timedelta(i)
        # yesterday = date + num_day
        # yesterday = yesterday.strftime('%Y-%m-%d')
        response = s.get(url='https://eq.10jqka.com.cn/lhbclient/data/method/indexData/date/%s'%today, headers={'Content-Type': 'application/json',
                    'User-Agent': 'Mozill0.75 Safari/537.36'},verify=False)
        date_ = response.json()["data"]["all"]["date"]
        stock_list = response.json()["data"]["all"]["list"]
        # print(date_,stock_list)
        for index in stock_list:
            name=index['stockName']
            money = str(float(index['inflow'])//10000)+'万'
            updown = index['rise']
            code = index['stockCode']
            capitalIcon_buy,capitalIcon_sell = [],[]
            departmentIcon = str(index['departmentIcon']).replace("'","")
            isThree=index['isThree']
            reasonList=index['reasonList']
            response2 = s.get(url="https://eq.10jqka.com.cn/lhbclient/data/method/stockDateData/stockCode/%s/date/%s"%(code,date_),
                             headers={'Content-Type': 'application/json','User-Agent': '4hjhk56IH232.00)'}, verify=False)
            buy_list=response2.json()["data"]["dateList"][0]["buyData"]["list"]
            # print(buy_list)
            for i in buy_list:
                capitalIcon_buy.append(i['capitalIcon'])
            sale_list=response2.json()["data"]["dateList"][0]["saleData"]["list"]
            for j in sale_list:
                capitalIcon_sell.append(j['capitalIcon'])
            capitalIcon='买：'+str(capitalIcon_buy)+'卖：'+str(capitalIcon_sell)
            capitalIcon=capitalIcon.replace("'","").replace(",","").replace("[","").replace("]","")
            tup_end=(date_,name,money,updown,code,capitalIcon,departmentIcon,isThree,reasonList,index['inflow'])
            sql="INSERT INTO daban VALUES ('%s','%s','%s','%s','%s','%s','%s','%d','%s','%s','0','0')"%tup_end
            # print(sql)
            cursor.execute(sql)
            db.commit()
    sql1 = "select  date,code from daban where date='%s'"%today
    cursor.execute(sql1)
    end_list = cursor.fetchall()
    for index in end_list:
        try:
            print(index[0], index[1])
            data_list = get_K.getKline(str(index[0]), str(index[0]), index[1])
            price = data_list[0][5]
            sql2 = "UPDATE  daban set price='%s', turn='%s' WHERE date='%s' and code='%s' " % (price,data_list[0][9] ,str(index[0]), index[1])
            cursor.execute(sql2)
            db.commit()
        except:
            continue
    get_K.bs_close()
    db.close()
daban()
