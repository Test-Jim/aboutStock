from bs4 import BeautifulSoup
import requests
import re
import pymysql
import datetime
s=requests.session()
def yjyg():
    response=s.get(url='http://data.10jqka.com.cn/financial/yjyg/',headers={'Content-Type': 'application/json',
                                  'User-Agent': 'IHexin/10.70.60 (iPhone; iOS 14.0.1; Scale/2.00)'})
    soup=BeautifulSoup(response.content,'lxml')
    end=soup.find_all('tr',limit=8)
    end.pop(0)
    gp_dic={}
    for index in end:
        gp_list=[]
        gp_name=index.find(class_="J_showCanvas")
        gp_td=index.find_all('td',text=True)
        gp_list.append(gp_name.string)
        for i in gp_td:
            gp_list.append(i.string.replace('\n','').replace(' ','').replace('\t',''))
        num=gp_list.pop(1)
        gp_dic[num]=gp_list
    return gp_dic
def yjkb():
    response=s.get(url='http://data.10jqka.com.cn/financial/yjkb/',headers={'Content-Type': 'application/json',
                                  'User-Agent': 'IHexin/10.70.60 (iPhone; iOS 14.0.1; Scale/2.00)'})
    soup=BeautifulSoup(response.content,'lxml')
    end = soup.find_all('tr', limit=15)
    end.pop(0)
    end.pop(0)
    gp_dic = {}
    k = 1
    for index in end:
        gp_list = []
        gp_name=index.find(class_="J_showCanvas")
        gp_td = index.find_all(class_=re.compile('c'))
        gp_list.append(gp_name.string)
        for i in gp_td:
            gp_list.append(i.string)
        gp_dic[k]=gp_list
        k+=1
    return gp_dic
def yjgg():

    response=s.get(url='http://data.10jqka.com.cn/financial/yjgg/',headers={'Content-Type': 'application/json',
                                  'User-Agent': 'IHexin/10.70.60 (iPhone; iOS 14.0.1; Scale/2.00)'})
    soup=BeautifulSoup(response.content,'lxml')
    end = soup.find_all('tr', limit=9)
    end.pop(0)
    end.pop(0)
    gp_dic = {}
    k = 1
    for index in end:
        gp_list = []
        gp_name=index.find(class_="J_showCanvas")
        gp_time=index.find_all(class_='tc')[1]
        gp_td = index.find_all(class_=re.compile('tr '))
        gp_list.append(gp_name.string)
        gp_list.append(gp_time.string)
        for i in gp_td:
            gp_list.append(i.string)
        gp_dic[k]=gp_list
        k+=1
    return gp_dic
def selectBS():
    db = pymysql.connect("47.111.24.112", "root", "withme_321", "test")
    cursor = db.cursor()
    sql_buy = "select  * from bs where type =1 ORDER BY date DESC LIMIT 50"
    sql_sell = "select  * from bs where type =0 ORDER BY date DESC LIMIT 50"

    cursor.execute(sql_buy)
    tup_buy = cursor.fetchall()
    cursor.execute(sql_sell)
    tup_sell=cursor.fetchall()
    # dic_buy,dic_sell={},{}
    db.close()
    return tup_buy,tup_sell

