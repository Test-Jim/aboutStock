import pymysql
import datetime
import baostock as bs
import openpyxl

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

#根据四天的量能来判断
def data_analysis_youzi():
    db = pymysql.connect("47.111.24.112", "root", "withme_321", "test")
    cursor = db.cursor()
    get_K = get_Kline()
    sql_code = "SELECT date,code,stockname,price,turn FROM daban_zd where model in ('左长') and date<='2021-08-20' "
    cursor.execute(sql_code)
    code_list = cursor.fetchall()
    h1,h2,h11,h22=0, 0,0,0
    for key in range(0,len(code_list)):
        day=code_list[key][0]
        code=code_list[key][1]
        # print(day,code)
        data_list = get_K.getKline(str(day+datetime.timedelta(-25)),str(day+datetime.timedelta(+25)), code)
        data_list2,t1,t2,t3=[],'','',''
        for index in data_list:
            if index[9] != '': data_list2.append(index)
        for ind,v in enumerate(data_list2):
            if v[0]==str(day):buy_index=ind+1

        if float(data_list2[buy_index-4][2])>float(data_list2[buy_index-4][5]):yanse4='绿'
        else:yanse4='红'
        if float(data_list2[buy_index-3][2])>float(data_list2[buy_index-3][5]):yanse3='绿'
        else:yanse3='红'
        if float(data_list2[buy_index-2][2])>float(data_list2[buy_index-2][5]):yanse2='绿'
        else:yanse2='红'
        yanse1='红'
        t4=float(data_list2[buy_index-4][7])
        t3=float(data_list2[buy_index-3][7])
        t2=float(data_list2[buy_index-2][7])
        t1=float(data_list2[buy_index-1][7])
        y_t = {yanse4: t4,yanse3: t3,yanse2: t2,yanse1: t1}
        h_s,l_s=0,0
        for k,v in y_t.items():
            if k=='红':h_s+=v
            else:l_s+=v

        sell_day = data_list2[buy_index+1][0]
        data_list3 = get_K.testgetKline(sell_day, sell_day, code, '5')
        sell_price = float(data_list3[47][3])
        try:
            if float(data_list2[buy_index][2]) < float(data_list2[buy_index][6]):
                buy_price = float(data_list2[buy_index][2])
            elif float(data_list2[buy_index][4]) <= float(data_list2[buy_index][6]) < float(data_list2[buy_index][3]):  # 今日最低<上一日收盘价<今日最高
                buy_price = float(data_list2[buy_index][6])  # 买价，T日开盘价
            syl =  ((sell_price - buy_price) / buy_price )
            if syl<=0:
                if h_s>l_s*3:h2+=1
                else:h22+=1
            else:
                if h_s>l_s*3:h1+=1
                else:h11+=1
        except:continue
        print(h1,h11,h2,h22)
    cursor.close()
    get_K.bs_close()

data_analysis_youzi()