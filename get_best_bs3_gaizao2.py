from gupiao import *
import warnings
warnings.filterwarnings("ignore")
#T日，买价，T-1日收盘价*0.99，买不进就不操作。卖价：T+1日，2点56接近收盘价
def get_best_choice(begin_day,end_day):
    get_K = get_Kline()
    db = pymysql.connect("47.111.24.112", "root", "withme_321", "test")
    cursor = db.cursor()
    success, fail, money,k = 0, 0, 100000,0,
    sql_date="SELECT DISTINCT date from bs where date>='%s' and date<='%s' ORDER BY date"%(begin_day,end_day)
    cursor.execute(sql_date)
    num_days = cursor.fetchall()
    for day in num_days:
        sql_buy ="select  date,name,code from bs where type =1 and date='%s' and code like '60%%'"%day[0]
        cursor.execute(sql_buy)
        tup_buy = cursor.fetchall()
        new_buy=[]
        for index in tup_buy:
            if '贵州茅台'==index[1]:continue
            if '银行' in index[1]:continue
            if '中国平安' ==index[1]:continue#不买中国平安
            if '证券'in index[1]:continue#不买证券
            if '华友钴业'==index[1]:continue
            new_buy.append(index)
        length=len(new_buy)
        if length==0:
            print('没有.sh的股票')
            continue
        cj,moneyS = 0,0
        for stock in new_buy:
            money0=money/length#计算当天要做几笔，均分交易的钱
            name=stock[1]
            code=stock[2]
            #获取K线数据
            data_list=get_K.getKline(str(day[0]),str(day[0]+datetime.timedelta(15)),code)
            if float(data_list[1][2])<float(data_list[1][6])*0.989:
                buy_price=float(data_list[1][2])
                k+=1
            elif float(data_list[1][4])<=float(data_list[1][6])*0.989<float(data_list[1][3]):#   今日最低<上一日收盘价<今日最高
                buy_price = float(data_list[1][6])*0.989# 买价，T日开盘价
            else:continue
            buy_day = data_list[1][0]  # 买的日期
            sell_day=data_list[2][0]
            data_list2=get_K.testgetKline(sell_day,sell_day,code,'5')
            sell_price = float(data_list2[24][3])
            cj+=1#计算当天成交了几笔
            moneyX = money0*(1+(sell_price-buy_price)/buy_price)*0.9985#每一笔计算后的钱
            trade_ls="在%s以%s价格买入%s，在%s以%s价格卖出,结算金额：%s"%(buy_day,buy_price,name,sell_day,sell_price,moneyX)
            print(trade_ls)
            moneyS+=moneyX#当天账户总额
        if cj == 0: continue  # 当天没有成交一笔时，直接去第二天
        x=length - cj  # 当日没有成交的笔数
        print('当天还有%s笔没交易，余额%s'%(x,(money/length)*x))
        moneyS=moneyS+(money/length)*x#当天计算后的总和
        money=moneyS
        print('计划当天买%s笔，实际买了%s笔，账户总余额%s'%(length,cj,moneyS))
    db.close()
    get_K.bs_close()
get_best_choice('2020-01-01','2021-01-01')#end_day是前一个交易日，可以给出今天的买入建议
