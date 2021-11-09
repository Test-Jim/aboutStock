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
def beishang():
    response = s.get(url='http://data.eastmoney.com/hsgtcg/list.html', headers={'Content-Type': 'application/json',
                                                                               'User-Agent': 'IHexin/10.70.60 (iPhone; iOS 14.0.1; Scale/2.00)'})
    soup = BeautifulSoup(response.content, 'lxml')
    end=soup.find_all('script',type="text/javascript",text=re.compile('pagedata'))
    # print(str(end))
    date = re.findall('"HdDate": "(.*?)"', str(end), re.M | re.I)[0:10]
    name=re.findall('"SName": "(.*?)"',str(end),re.M|re.I)[0:10]
    gushu_jiajian = re.findall('"ShareHold_Chg_One": (.*?),', str(end), re.M | re.I)[0:10]
    shizhi_jiajian=re.findall('"Zdf": (.*?),',str(end),re.M|re.I)[0:10]
    dict_={}
    for index in range(1,11):
        dict_[index]=[date[index-1],name[index-1],str(float(gushu_jiajian[index-1])//10000)+'万',shizhi_jiajian[index-1]]
    return dict_
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
    # for index in start:
    #     start_list=[]
    #     for k,v in index.items():
    #         start_list.append(v)
    #     start_list[2]=str(float(start_list[2])//10000)+'万'
    #     start_dict[i]=start_list
    #     i+=1
    #
    # for index in end:
    #     end_list=[]
    #     for k,v in index.items():
    #         end_list.append(v)
    #     end_list[2]=str(float(end_list[2])//10000)+'万'
    #     end_dict[j]=end_list
    #     j+=1
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
    # #使用 fetchone() 方法获取单条数据.
    # data = cursor.fetchone()
    db.commit()
    db.close()

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

beishang2()
