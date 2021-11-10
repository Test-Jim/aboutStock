#此文件功能：下载北上资金的股票到bs表内
import requests
import pymysql
import datetime
s=requests.session()

def beishang2():
    db = pymysql.connect("47.111.24.112", "root", "withme_321", "test")
    cursor = db.cursor()

    today = datetime.date.today()
    num_day=datetime.timedelta(-1)
    yesterday=today+num_day
    response = s.get(url='https://eq.10jqka.com.cn/hgt/data/method/inflowList/type/hs/date/%s'%yesterday, headers={'Content-Type': 'application/json', 'User-Agent': 'OS 14.0.1; Scale/2.00)'},verify=False)
    start_dict ,end_dict,i,j= {},{},1,1
    start = response.json()["one"]["start"]
    end=response.json()["one"]["end"]
    #入库
    for index in start:
        date=yesterday
        name=index['name']
        money=str(float(index['inflow'])//10000)+'万'
        updown=index['change']
        code=index['code']
        tup_start=(date,name,money,updown,1,code,1.1)
        sql="INSERT into bs values('%s','%s','%s','%s','%d','%s','%f')"%tup_start
        cursor.execute(sql)
    for index in end:
        date=yesterday
        name=index['name']
        code=index['code']
        money=str(float(index['inflow'])//10000)+'万'
        updown=index['change']
        tup_end=(date,name,money,updown,0,code,1.1)
        sql="INSERT into bs values('%s','%s','%s','%s','%d','%s','%f')"%tup_end
        cursor.execute(sql)
    db.commit()
    db.close()
beishang2()
