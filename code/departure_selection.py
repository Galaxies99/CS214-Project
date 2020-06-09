import csvreader
import numpy as np
import matplotlib.pyplot as plt
from pyecharts.charts import HeatMap
from pyecharts import options as opts
import math
import time

def timestamp_datetime(value):
    format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(int(value))
    dt = time.strftime(format, value)
    return dt


def datetime_timestamp(dt):
    time.strptime(dt, '%Y-%m-%d %H:%M:%S')
    s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
    return int(s)

if __name__ == '__main__':
    dest_cnt = {}
    dat = csvreader.csv_reader_no_headers("D:\Algorithm and Complexity Group Project\order_20161105")
    for line in dat:
        dest_longitude = float(line[3])
        dest_latitude = float(line[4])

        dest_brick_lon = int(dest_longitude * 50)
        dest_brick_lat = int(dest_latitude * 50)

        s = timestamp_datetime(int(line[1]))
        s = s[11:]
        s1 = '23:00:00'
        s2 = '06:00:00'
        if s >= s1 or s <= s2:
            index = str(dest_brick_lon) + '.' + str(dest_brick_lat)
            if dest_cnt.get(index) is None:
                dest_cnt[index] = 1
            else:
                dest_cnt[index] += 1

    dest = []
    for key in dest_cnt.keys():
        dest_brick_lon, dest_brick_lat = key.split('.')
        dest.append([dest_cnt[key], int(dest_brick_lon), int(dest_brick_lat)])

    dest.sort()

    for item in dest:
        print('longitude =', item[1] / 50.0, 'latitude =', item[2] / 50.0, 'count =', item[0])

    x_axis = []
    y_axis = []
    for i in range(10380, 10430, 2):
        x_axis.append(i / 100.0)
    for j in range(3040, 3100, 2):
        y_axis.append(j / 100.0)

    data = [[i, j, 0] for i in range(len(x_axis)) for j in range(len(y_axis))]

    for item in dest:
        if item[0] < 5:
            continue
        ix = int((item[1] / 50.0 - 103.8) / 0.02)
        iy = int((item[2] / 50.0 - 30.4) / 0.02)
        for d_item in data:
            if d_item[0] == ix and d_item[1] == iy:
                d_item[2] = item[0]
                break

    Max = 0
    for item in data:
        Max = max(Max, item[2])

    for item in data:
        item[2] = int(item[2] / Max * 100)

    heat_map = (
        HeatMap()
        .add_xaxis(x_axis)
        .add_yaxis("HeatMap",
                   y_axis,
                   data,
                   label_opts=opts.LabelOpts(is_show=True, position="inside"),)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="HeatMap"),
            visualmap_opts=opts.VisualMapOpts(),
        )
        .render("heatmap.html")
    )
