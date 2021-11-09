import pymysql
import datetime
import random,string
import requests
import warnings

warnings.filterwarnings("ignore")

def download_liangbi():
    db = pymysql.connect("47.111.24.112", "root", "withme_321", "test")
    cursor = db.cursor()
    S=requests.session()
    my_headers = [
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWeKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) ApplWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/2010101 Firefox/30.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWeKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Wn64; x64; Trident/6.0)",
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8..11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.; U; en)',
        'Mozilla/4.0 (compatible; MIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i66; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SL-MM/1.4.1 GNUTLS/1.2.9',
        "Mozilla/5.0 (X11; Linux i686) AppleWbKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/2010101 Firefox/10.0 "
    ]
    my_v=['',
          '',
          '',
          '',
          '']
    date_temp = datetime.datetime.strptime('2019-12-10', '%Y-%m-%d').date()

    for i in range(-1,-25,-1):
        id1 = ''.join(random.sample(string.digits + string.ascii_letters, 42))
        id2 = ''.join(random.sample(string.digits + string.ascii_letters, 32))

        headers = {'User-Agent': '%s' % random.choice(my_headers),
                   'Content-Type': 'application/json',
                   'Cookie': 'cid=%s; ComputerID=%s; WafStatus=0; PHPSESSID=%s; iwencaisearchquery=12345; v=%s' % (id1, id1, id2,random.choice(my_v))}


        num_day = datetime.timedelta(i)
        day_use = date_temp + num_day
        url_00 = "http://www.iwencai.com/stockpick/load-data?typed=1&preParams=&ts=1&f=1&qs=result_rewrite&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w=%s量比榜前5,中小板&queryarea="%str(day_use)
        url_60 = "http://www.iwencai.com/stockpick/load-data?typed=1&preParams=&ts=1&f=1&qs=result_rewrite&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w=%s量比榜前5,60开头&queryarea="%str(day_use)

        response=S.get(url=url_00,headers=headers)
        data=response.json()['data']
        end=data['result']['result']
        date=data['parse']['natConds'][0]['natSent'][0:10].replace('年','-').replace('月','-')

        #为了数据库去重
        sql_data="SELECT distinct date from liangbi_zd where date='%s'"%date
        cursor.execute(sql_data)
        date_days = cursor.fetchall()
        if date_days!=():continue

        for index in end:
            code=index[0][0:6]
            name=index[1]
            price=index[2]
            updown=index[3]
            if price=='--':price='0.0'
            if updown=='--':updown='0.0'
            liangbi=index[4][0:4]
            mingci=index[6]
            turn=index[9][0:4]
            tup_data=(date,code,name,price,updown,liangbi,mingci,turn)
            day_code = "insert into  liangbi_zd VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" % tup_data
            cursor.execute(day_code)

        response=S.get(url=url_60,headers=headers)
        data=response.json()['data']
        end=data['result']['result']
        date=data['parse']['natConds'][0]['natSent'][0:10].replace('年','-').replace('月','-')
        for index in end:
            code=index[0][0:6]
            name=index[1]
            price=index[2]
            updown=index[3]
            if price=='--':price='0.0'
            if updown=='--':updown='0.0'
            liangbi=index[4][0:4]
            mingci=index[6]
            turn=index[8][0:4]
            tup_data = (date, code, name, price, updown, liangbi, mingci, turn)
            day_code = "insert into  liangbi_zd VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" % tup_data
            cursor.execute(day_code)
        print(date)
        db.commit()

    cursor.close()
    db.close()
download_liangbi()