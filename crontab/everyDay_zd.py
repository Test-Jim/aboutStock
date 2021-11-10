#此文件功能：下载每天涨停/跌停的股票到daban_zd表内
import requests
import pymysql
import datetime
s=requests.session()
#下载每天涨停、跌停的股票数据
def download_days_zhangdie():
    import time
    db = pymysql.connect("47.111.24.112", "root", "withme_321", "test")
    cursor = db.cursor()
    #date = datetime.datetime.strptime('2021-03-17', '%Y-%m-%d').date()
    today = datetime.date.today()
    for i in range(1,2):
        #num_day = datetime.timedelta(i)
        #oldday = date + num_day
        timetemp=int(time.time() * 1000)
        tup_canshu=(str(today).replace("-",""),str(timetemp))
        url='https://data.10jqka.com.cn/dataapi/limit_up/limit_up_pool?page=1&limit=100&field=199112,10,9001,330323,330324,330325,9002,330329,133971,133970,1968584,3475914,9003,9004&filter=HS&date=%s&order_field=330324&order_type=0&_=%s'%tup_canshu
        url_2='https://data.10jqka.com.cn/dataapi/limit_up/lower_limit_pool?page=1&limit=15&field=199112,10,330333,330334,1968584,3475914,9004&filter=HS&date=%s&order_field=330334&order_type=0&_=%s'%tup_canshu
        response = s.get(url=url, headers={'Content-Type': 'application/json',
                    'User-Agent': 'Mo Chrome/861.0.4240./537.36'},verify=False)
        zt_list = response.json()["data"]["info"]
        #涨停
        for index in zt_list:
            if '退' in index['name']:continue
            updown = index['change_rate']
            code = index['code']
            highdays = index['high_days']
            price = index['latest']
            limittype = index['limit_up_type']
            stockname = index['name']
            turn = index['turnover_rate']
            reason = index['reason_type']
            orderamount = index['order_amount']
            shizhi=float(index['currency_value']) / 100000000

            data_tup = (today, code, stockname, float(price), updown,float(turn), shizhi, highdays, limittype, reason,orderamount)
            sql = "INSERT INTO daban_zd (date,code,stockname,price,updown,turn,shizhi,highdays,limittype,reason,orderamount) VALUES('%s','%s','%s','%f','%s','%f','%s','%s','%s','%s','%s')" % data_tup
            cursor.execute(sql)
        db.commit()
        #跌停
        response = s.get(url=url_2, headers={'Content-Type': 'application/json',
                    'User-Agent': 'Mo Chrome/861.0.4240./537.36'},verify=False)
        dt_list = response.json()["data"]["info"]
        for index in dt_list:
            updown = index['change_rate']
            code = index['code']
            price = index['latest']
            stockname = index['name']
            turn = index['turnover_rate']
            shizhi = float(index['currency_value'])/100000000
            data_tup = (today, code, stockname, float(price), updown, float(turn), shizhi, 0, 0, 0,0)
            sql = "INSERT INTO daban_zd (date,code,stockname,price,updown,turn,shizhi,highdays,limittype,reason,orderamount) VALUES('%s','%s','%s','%f','%s','%f','%s','%s','%s','%s','%s')" % data_tup
            cursor.execute(sql)
        db.commit()
    db.close()
download_days_zhangdie()
