import csvreader
import order_filter
import csv
import math
import matplotlib.pyplot as plt
import kmeans

K = 50
beta_d = 0.6
beta_h = 0.4
departure_radius = 10
lon_km = 111
lat_km = 96


def selection(re):
    dest_cnt = {}
    hotel_cnt = {}
    dat = order_filter.filter_night('../../CS214-CourseData/Projects/data/chengdu_order/order_20161105')
    departure_dat = csvreader.csv_reader_no_headers('../data/departure.csv')
    departure = [float(departure_dat[0][0]), float(departure_dat[0][1])]
    hotel_dat = csvreader.csv_reader_no_headers('../data/hotel_address_lat_lng.csv')

    # Analyze order destination.
    for line in dat:
        dest_longitude = float(line[5])
        dest_latitude = float(line[6])

        dest_brick_lon = int(dest_longitude * 500)
        dest_brick_lat = int(dest_latitude * 500)

        index = str(dest_brick_lon) + '.' + str(dest_brick_lat)
        if dest_cnt.get(index) is None:
            dest_cnt[index] = 1
        else:
            dest_cnt[index] += 1

    # Analyze hotel data
    valid_cnt = 0
    for line in hotel_dat:
        hotel_lat = float(line[0])
        hotel_lon = float(line[1])
        if hotel_lon < 103.9 or hotel_lon > 104.2 or hotel_lat < 30.55 or hotel_lat > 30.775:
            continue
        valid_cnt += 1
        hotel_brick_lon = int(hotel_lon * 500)
        hotel_brick_lat = int(hotel_lat * 500)
        index = str(hotel_brick_lon) + '.' + str(hotel_brick_lat)
        if hotel_cnt.get(index) is None:
            hotel_cnt[index] = 1
        else:
            hotel_cnt[index] += 1

    # Combine
    cnt = {}
    for key in dest_cnt.keys():
        res = dest_cnt[key]
        if res >= 50:
            res = 50
        cnt[key] = beta_d * res / 50

    for key in hotel_cnt.keys():
        if cnt.get(key) is None:
            cnt[key] = beta_h / (1 + math.exp(-hotel_cnt[key]))
        else:
            cnt[key] += beta_h / (1 + math.exp(-hotel_cnt[key]))

    dest = []
    for key in cnt.keys():
        brick_lon, brick_lat = key.split('.')
        dest.append([cnt[key], int(brick_lon), int(brick_lat)])

    dest.sort()

    pre_final_list = []

    for item in dest:
        if re and (lon_km * (departure[0] - item[1] / 500.0)) ** 2 + (lat_km * (departure[1] - item[2] / 500.0)) ** 2 <= departure_radius ** 2:
            continue
        if item[0] >= 0.4:
            pre_final_list.append([item[1], item[2]])
            print('longitude =', item[1] / 500.0, 'latitude =', item[2] / 500.0, 'count =', item[0])

    min_arg = [51975, 15275]
    max_arg = [52087, 15400]

    center, _ = kmeans.kmeans(K, 2, min_arg, max_arg, pre_final_list)

    dest_lon = []
    dest_lat = []

    with open('../data/destination.csv', 'w', newline='') as out:
        csv_write = csv.writer(out, dialect='excel')
        for item in center:
            print(item[0] / 500.0, item[1] / 500.0)
            dest_lon.append(item[0] / 500.0)
            dest_lat.append(item[1] / 500.0)
            csv_write.writerow([item[0] / 500.0, item[1] / 500.0])

    print('total', len(dest_lon), 'possible destinations.')

    plt.plot(dest_lon, dest_lat, 'o', markersize=2)
    plt.savefig('../data/destination.pdf', dpi=300)
    plt.show()


if __name__ == '__main__':
    selection(1)