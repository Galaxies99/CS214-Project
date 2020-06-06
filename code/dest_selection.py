import csvreader
import numpy as np
import matplotlib.pyplot as plt
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
    dat = csvreader.csv_reader_no_headers("../../CS214-CourseData/Projects/data/chengdu_order/order_20161105")
    
    for line in dat:
        dest_longitude = float(line[5])
        dest_latitude = float(line[6])

        dest_brick_lon = int(dest_longitude * 500)
        dest_brick_lat = int(dest_latitude * 500)

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

    dest_lon = []
    dest_lat = []

    for item in dest:
        if item[0] > 500:
            dest_lon.append(item[1] / 500.0)
            dest_lat.append(item[2] / 500.0)

        print('longitude =', item[1] / 500.0, 'latitude =', item[2] / 500.0, 'count =', item[0])

    print("total =" len(dest_lon))

    plt.plot(dest_lon, dest_lat, 'o', markersize=2)
    plt.show()
