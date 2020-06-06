import csvreader
import numpy as np
import matplotlib.pyplot as plt
import time

def timestamp_datetime(value):
    format = '%Y-%m-%d %H:%M:%S'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(int(value))
    ## 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt
def datetime_timestamp(dt):
    #dt为字符串
    #中间过程，一般都需要将字符串转化为时间数组
    time.strptime(dt, '%Y-%m-%d %H:%M:%S')
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
    #将"2012-03-28 06:53:40"转化为时间戳
    s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
    return int(s)

if __name__ == '__main__':
    dest_cnt = {}
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
    dat1 = csvreader.csv_reader_no_headers("D:\Algorithm and Complexity Group Project\order_20161105")
    dat2 = csvreader.csv_reader_no_headers("D:\Algorithm and Complexity Group Project\order_20161106")
    dat3 = csvreader.csv_reader_no_headers("D:\Algorithm and Complexity Group Project\order_20161107")
    dat = dat1 + dat2 + dat3
<<<<<<< Updated upstream
=======
=======
    dat = csvreader.csv_reader_no_headers("../../CS214-CourseData/Projects/data/chengdu_order/order_20161105")
>>>>>>> d81641c0e5cc6207abdcf6a008d2872513b37669
>>>>>>> Stashed changes
    for line in dat:
        dest_longitude = float(line[5])
        dest_latitude = float(line[6])

        dest_brick_lon = int(dest_longitude * 500)
        dest_brick_lat = int(dest_latitude * 500)

        s = timestamp_datetime(int(line[1]))
        s = s[11:]
        s1 = '23:00:00'
        s2 = '06:00:00'
        #d1 = datetime_timestamp('2016-11-05 23:00:00')
        #d2 = datetime_timestamp('2016-11-05 06:00:00')
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

    dest_lon = []
    dest_lat = []

    for item in dest:
        if item[0] > 500:
            dest_lon.append(item[1] / 500.0)
            dest_lat.append(item[2] / 500.0)

        print('longitude =', item[1] / 500.0, 'latitude =', item[2] / 500.0, 'count =', item[0])

    print(len(dest_lon))


    plt.plot(dest_lon, dest_lat, 'o', markersize=2.)
    plt.show()



