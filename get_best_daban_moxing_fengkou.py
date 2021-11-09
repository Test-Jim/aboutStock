import pymysql
import datetime
import baostock as bs
from selenium import webdriver

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

#下载当日的风口
def ggg():
    import requests
    db = pymysql.connect("47.111.24.112", "root", "withme_321", "test")
    cursor = db.cursor()

    sql0="SELECT DISTINCT date FROM daban_zd  ORDER BY date desc limit 1"
    cursor.execute(sql0)
    day_list0 = cursor.fetchall()


    sql1="SELECT DISTINCT date from daban_zd   where date='%s' ORDER BY date desc"%str(day_list0[0][0])
    cursor.execute(sql1)
    day_list = cursor.fetchall()
    s=requests.session()
    for day in day_list:
        date=str(day[0]).replace('-','')
        resp=s.get(url='https://data.10jqka.com.cn/dataapi/limit_up/block_top?filter=HS&date=%s'%date,headers={'Content-Type': 'application/json',
                        'User-Agent': 'Mo Chrome/86.0.4240.75 Safari/537.36'},verify=False)
        end=resp.json()['data']
        fengkou0=end[0]['name']
        fengkou1=end[1]['name']
        fengkou2=end[2]['name']
        fengkou3=end[3]['name']
        fengkou=fengkou0+'|'+fengkou1+'|'+fengkou2+'|'+fengkou3
        print(fengkou)
        sql2 = "UPDATE  daban_zd set fengkou='%s' WHERE date='%s'  " %(fengkou,day[0])
        cursor.execute(sql2)
        db.commit()
    db.close()
ggg()

#写入主力流入流出资金到daban_zd
def data_analysis_youzi():
    db = pymysql.connect("47.111.24.112", "root", "withme_321", "test")
    cursor = db.cursor()

    sql0="SELECT DISTINCT date FROM daban_zd  ORDER BY date desc limit 2"
    cursor.execute(sql0)
    day_list0 = cursor.fetchall()


    day1,day2=str(day_list0[1][0]),str(day_list0[0][0])
    sql_code="SELECT DISTINCT code,GROUP_CONCAT(date) FROM daban_zd where date>='%s' and date<='%s'  and code like'00%%' and updown>0  GROUP BY code"%(day1,day2)
    cursor.execute(sql_code)
    code_list = cursor.fetchall()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(chrome_options=options)

    for code_day in code_list:
        code=code_day[0]
        all_day=code_day[1].replace("'","").split(',')
        # all_day=['2021-09-17','2021-09-22']
        driver.get('https://data.eastmoney.com/zjlx/%s.html' % code)
        # if code=='000876':continue

        if len(all_day)==1:
            if all_day[0]==day1:
                dde_buy=driver.find_element_by_css_selector('#table_ls > table > tbody > tr:nth-child(1) > td:nth-child(4) > span').text
                dde_buy_per=driver.find_element_by_css_selector('#table_ls > table > tbody > tr:nth-child(1) > td:nth-child(5) > span').text
                if '亿' in dde_buy:dde_buy=float(dde_buy[0:-1:1])*10000
                else:dde_buy=dde_buy[0:-1:1]
                dde_buy_per=dde_buy_per.replace('%','')
                sql2 = "UPDATE  daban_zd set dde_buyday='%s' ,dde_buyday_per='%s' WHERE code='%s'and date='%s' " % (dde_buy,dde_buy_per,code,day1)
                print(sql2)
                cursor.execute(sql2)
            else:
                dde_look=driver.find_element_by_css_selector('#table_ls > table > tbody > tr:nth-child(1) > td:nth-child(4) > span').text
                dde_look_per=driver.find_element_by_css_selector('#table_ls > table > tbody > tr:nth-child(1) > td:nth-child(5) > span').text
                dde_look_per=dde_look_per.replace('%','')
                if '亿' in dde_look:dde_look=float(dde_look[0:-1:1])*10000
                else:dde_look=dde_look[0:-1:1]
                sql2 = "UPDATE  daban_zd set dde_lookday='%s',dde_lookday_per='%s' WHERE code='%s'and date='%s' " % (dde_look,dde_look_per,code,day2)
                print(sql2)
                cursor.execute(sql2)
        else:
            if all_day[0]==day1:
                dde_buy = driver.find_element_by_css_selector('#table_ls > table > tbody > tr:nth-child(1) > td:nth-child(4) > span').text
                dde_buy_per = driver.find_element_by_css_selector('#table_ls > table > tbody > tr:nth-child(1) > td:nth-child(5) > span').text
                dde_buy_per=dde_buy_per.replace('%','')
                if '亿' in dde_buy:dde_buy = float(dde_buy[0:-1:1]) * 10000
                else:dde_buy = dde_buy[0:-1:1]
                sql2 = "UPDATE  daban_zd set dde_buyday='%s',dde_buyday_per='%s' WHERE code='%s'and date='%s' " % (dde_buy,dde_buy_per, code,day1)
                print(sql2)
                cursor.execute(sql2)
            if all_day[1]==day2:
                dde_look=driver.find_element_by_css_selector('#table_ls > table > tbody > tr:nth-child(1) > td:nth-child(4) > span').text
                dde_look_per=driver.find_element_by_css_selector('#table_ls > table > tbody > tr:nth-child(1) > td:nth-child(5) > span').text
                dde_look_per=dde_look_per.replace('%','')
                if '亿' in dde_look:dde_look=float(dde_look[0:-1:1])*10000
                else:dde_look=dde_look[0:-1:1]
                sql2 = "UPDATE  daban_zd set dde_lookday='%s',dde_lookday_per='%s' WHERE code='%s'and date='%s' " % (dde_look,dde_look_per,code,day2)
                print(sql2)
                cursor.execute(sql2)
        db.commit()
    db.close()
    driver.close()
    driver.quit()
data_analysis_youzi()
#把历史的dde百分比
def data_dde_per():

    db = pymysql.connect("47.111.24.112", "root", "withme_321", "test")
    cursor = db.cursor()
    sql_code="SELECT  date,code from daban_zd   where date>'2021-05-25' and code like '00%' and updown >0 "
    cursor.execute(sql_code)
    code_list = cursor.fetchall()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    try:
        for code_day in code_list:
            day=code_day[0]
            code=code_day[1]
            driver.get('https://data.eastmoney.com/zjlx/%s.html' % code)
            # if code=='000876':continue
            print(code,day)
            for num in range(2,102):
                # table_ls > table > tbody > tr:nth-child(2) > td:nth-child(1)
                try:
                    if str(day)==driver.find_element_by_css_selector('#table_ls > table > tbody > tr:nth-child(%s) > td:nth-child(1)'%num).text:
                        dde_look_per=driver.find_element_by_css_selector('#table_ls > table > tbody > tr:nth-child(%s) > td:nth-child(5) > span'%num).text
                        dde_buy_per=driver.find_element_by_css_selector('#table_ls > table > tbody > tr:nth-child(%s) > td:nth-child(5) > span'%(num-1)).text
                        dde_look_per=dde_look_per.replace('%','')
                        dde_buy_per=dde_buy_per.replace('%','')
                    else:continue
                except:continue
            sql2 = "UPDATE  daban_zd set dde_lookday_per='%s', dde_buyday_per='%s' WHERE code='%s'and date='%s' " % (dde_look_per,dde_buy_per,code,day)
            # print(sql2)
            cursor.execute(sql2)
            db.commit()
    finally:
        db.close()
        driver.close()
        driver.quit()
# data_dde_per()