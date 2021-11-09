import pyecharts.options as opts
from pyecharts.charts import Kline,Line
import baostock as bs
import pymysql
import datetime
from pyecharts.charts import Page
Pa=Page()
# data=[[15,15.9,14.8,15.3],[16,16.8,14.6,15.9]]
data=[[15,15.3,14.8,15.9],[16,15.9,14.6,16.8]]
c=(
        Kline()
        .add_xaxis(['2020-01-02','2020-01-03'])
        .add_yaxis("kline",
                   data,
                   itemstyle_opts=opts.ItemStyleOpts(
                   color="#ec0000",
                   color0="#00da3c",
                   border_color="#8A0000",
                   border_color0="#008F28",
            )
        )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(is_scale=True),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
            title_opts=opts.TitleOpts(title="K-line"),
        )
)

Pa.add(c)
Pa.render('cc.html')



