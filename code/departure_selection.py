import order_filter
import csv
import json


if __name__ == '__main__':
    departure_cnt = {}
    dat = order_filter.filter_night("../../CS214-CourseData/Projects/data/haikou_order/order_20171011_20171014.csv")

    for line in dat:
        departure_longitude = float(line[3])
        departure_latitude = float(line[4])


        departure_brick_lon = int(departure_longitude * 50)
        departure_brick_lat = int(departure_latitude * 50)

        index = str(departure_brick_lon) + '.' + str(departure_brick_lat)
        if departure_cnt.get(index) is None:
            departure_cnt[index] = 1
        else:
            departure_cnt[index] += 1

    departure = []
    for key in departure_cnt.keys():
        departure_brick_lon, departure_brick_lat = key.split('.')
        departure.append([departure_cnt[key], int(departure_brick_lon), int(departure_brick_lat)])

    departure.sort()
    departure.reverse()

    with open('../data/departure.csv', 'w', newline='') as out:
        csv_write = csv.writer(out, dialect='excel')
        for item in departure:
            print('longitude =', item[1] / 50.0, 'latitude =', item[2] / 50.0, 'count =', item[0])
            csv_write.writerow([item[1] / 50.0, item[2] / 50.0, item[0]])

