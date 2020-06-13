import order_filter
import csv
import json


if __name__ == '__main__':
    departure_cnt = {}
    dat = order_filter.filter_night("../../CS214-CourseData/Projects/data/chengdu_order/order_20161105")

    for line in dat:
        departure_longitude = float(line[3])
        departure_latitude = float(line[4])

        departure_brick_lon = int(departure_longitude * 100)
        departure_brick_lat = int(departure_latitude * 100)

        index = str(departure_brick_lon) + '.' + str(departure_brick_lat)
        if departure_cnt.get(index) is None:
            departure_cnt[index] = 1
        else:
            departure_cnt[index] += 1

    heat_t = []
    for key in departure_cnt.keys():
        departure_brick_lon, departure_brick_lat = key.split('.')
        if departure_cnt[key] >= 3:
            heat_t.append({'lng': int(departure_brick_lon) / 100.0, 'lat': int(departure_brick_lat) / 100.0, 'count': departure_cnt[key]})

    t_dict = {'point': heat_t}
    with open('../data/heatmap_data.dat', 'w') as file:
        json.dump(t_dict, file)

    # goto http://lbsyun.baidu.com/jsdemo.htm#c1_15 to generate heatmap.
