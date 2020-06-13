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


def selection():
    dest_cnt = {}
    dat = order_filter.filter_night('../../CS214-CourseData/Projects/data/chengdu_order/order_20161105')

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

    dest = []
    for key in dest_cnt.keys():
        brick_lon, brick_lat = key.split('.')
        dest.append([dest_cnt[key], int(brick_lon), int(brick_lat)])

    dest.sort()
    dest.reverse()

    dest_lon = []
    dest_lat = []

    with open('../data/original_destination_k' + str(K) + '.csv', 'w', newline='') as out:
        csv_write = csv.writer(out, dialect='excel')
        for i in range(K):
            item = dest[i]
            print(item[1] / 500.0, item[2] / 500.0)
            dest_lon.append(item[1] / 500.0)
            dest_lat.append(item[2] / 500.0)
            csv_write.writerow([item[1] / 500.0, item[2] / 500.0])

    print('total', len(dest_lon), 'possible destinations.')

    plt.plot(dest_lon, dest_lat, 'o', markersize=2)
    plt.savefig('../data/original_destination_k' + str(K) + '.pdf', dpi=300)
    plt.show()


if __name__ == '__main__':
    selection()
