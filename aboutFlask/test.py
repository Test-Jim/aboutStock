# 导入Flask类
from flask import Flask
from flask import render_template
import get_best_bs3_gaizao
import os

from gupiao import *
# 实例化，可视为固定格式
app = Flask(__name__)
from datetime import timedelta

# 自动重载模板文件
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

# 设置静态文件缓存过期时间
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(minutes=720)


# route()方法用于设定路由；类似spring路由配置
@app.route('/get.html')
def get_html():
    result_dir = os.path.abspath('') + '/templates'
    l = os.listdir(result_dir)
    l.sort(key=lambda fn: os.path.getmtime(result_dir + '/' + fn) if not os.path.isdir(result_dir + '/' + fn) else 0)
    print(l[-1])
    # 使用render_template()方法重定向到templates文件夹下查找get.html文件
    return render_template(l[-1])

@app.route('/hotPoints')
def get_hotPoints():
    import requests, json
    import get_best_daban
    s = requests.Session()
    response = s.get(url="https://m.0033.com/listv4/hs/1A0001_1.json", verify=False,
                     headers={'Content-Type': 'application/json',
                              'User-Agent': 'IHexin/10.70.60 (iPhone; iOS 14.0.1; Scale/2.00)'})
    end_dict={}
    end = response.json()["data"]["pageItems"]
    # print(end)
    num=1
    for index in end:
        end_list=[]
        # print(index['source'], index['title'], index['url'], )
        end_list.append(index['source'])
        end_list.append(index['title'])
        end_list.append(index['url'])
        end_dict[num]=end_list
        num+=1
    # end_dict=json.dumps(end_dict, indent=4)
    yjygdic=yjyg()
    yjkbdic=yjkb()
    yjggdic=yjgg()
    bszj_buy,bszj_sell=selectBS()
    buy=get_best_bs3_gaizao.get_best_choice()
    daban=get_best_daban.data_analysis_youzi()

    return render_template('redia.html',end_dict=end_dict,buy=buy,yjygdic=yjygdic,yjkbdic=yjkbdic,
                           yjggdic=yjggdic,bszj_buy=bszj_buy,bszj_sell=bszj_sell,daban=daban)


@app.route('/threeImage')
def get_threeImage():
    import Day_kline_now
    Day_kline_now.create_Kline_Image()
    return render_template('threeImage.html')

@app.route('/bestChoice/<beginDate>/<endDate>/<code>')
def get_bestChoice():
    pass



if __name__ == '__main__':
    # app.run(host, port, debug, options)
    # 默认值：host="127.0.0.1", port=5000, debug=False
    app.run(host="0.0.0.0", port=5000)
