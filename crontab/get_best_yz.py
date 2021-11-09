from gupiao3 import *

db = pymysql.connect("47.111.24.112", "root", "withme_321", "test")
cursor = db.cursor()
get_K = get_Kline()
def download_data_first():
    sql_code="select   DISTINCT code,GROUP_CONCAT(date) from daban WHERE code not like '300___'  and  code not like '688___' and code not like '900__'GROUP BY code"
    cursor.execute(sql_code)
    code_list = cursor.fetchall()
    # print(code_list)
    for index in code_list:
        begin_date=index[1][-10::1]
        end_date=index[1][0:10]
        code=index[0]
        print(code)
        data_list=get_K.getKline(begin_date,end_date,code)
        for j in data_list:
            amount=str(float(j[8])//10000)+'万'
            updown='%.3f' % float(j[10])
            data_tup=(j[0],code,updown,j[2] , j[3], j[4], j[5], j[9],amount)
            sql_data="INSERT INTO t_stock VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%data_tup
            # print(sql_data)
            cursor.execute(sql_data)
        db.commit()
    get_K.bs_close()
    db.close()
    # testgetKline

def every_day():
    date=datetime.date.today()
    sql_code = "select DISTINCT code from daban WHERE date='%s' and  code not like '300___'  and  code not like '688___' and code not like '9%%'"%date
    cursor.execute(sql_code)
    code_list = cursor.fetchall()

    for index in code_list:
        begin_date=str(date)
        end_date=str(date)
        code=index[0]
        #print(code)
        data_list=get_K.getKline(begin_date,end_date,code)
        # print(data_list)
        amount=str(float(data_list[0][8])//10000)+'万'
        updown='%.3f' % float(data_list[0][10])
        data_tup=(data_list[0][0],code,updown,data_list[0][2] , data_list[0][3], data_list[0][4], data_list[0][5], data_list[0][9],amount)
        sql_data="INSERT INTO t_stock VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%data_tup
        # print(sql_data)
        cursor.execute(sql_data)
        db.commit()
    get_K.bs_close()
    db.close()

every_day()
