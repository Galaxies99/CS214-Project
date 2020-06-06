import csvreader
import matplotlib.pyplot as plt


if __name__ == '__main__':
    dest_cnt = {}
    dat = csvreader.csv_reader_no_headers("../data/chengdu_order/order_20161105")
    for line in dat:
        dest_longitude = float(line[3])
        dest_latitude = float(line[4])

        dest_brick_lon = int(dest_longitude * 500)
        dest_brick_lat = int(dest_latitude * 500)

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
        if item[0] > 100:
            dest_lon.append(item[1] / 500.0)
            dest_lat.append(item[2] / 500.0)

        print('longitude =', item[1] / 500.0, 'latitude =', item[2] / 500.0, 'count =', item[0])

    print(len(dest_lon))

    plt.plot(dest_lon, dest_lat, 'r.')
    plt.show()

