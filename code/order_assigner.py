import order_filter
import datahelper
import csvreader


departure_radius = 10
lon_km = 111
lat_km = 96


def assign(filename, time_l, time_r, m, L, pb, pc, cr, cb):
    dat = order_filter.filter_time(filename, time_l, time_r)
    dest_dat = csvreader.csv_reader_no_headers('../data/destination.csv')
    departure_dat = csvreader.csv_reader_no_headers('../data/departure.csv')
    coordinates = [[float(departure_dat[0][0]), float(departure_dat[0][1])]]
    for line in dest_dat:
        coordinates.append([float(line[0]), float(line[1])])
    for line in coordinates:
        line[0] *= lon_km
        line[1] *= lat_km
    k = len(coordinates)
    dest = []
    for line in dat:
        departure_longitude = float(line[3]) * lon_km
        departure_latitude = float(line[4]) * lat_km
        dest_longitude = float(line[5]) * lon_km
        dest_latitude = float(line[6]) * lat_km
        if (departure_longitude - coordinates[0][0]) ** 2 + (departure_latitude - coordinates[0][1]) ** 2 > departure_radius ** 2:
            continue
        min_dis, pos = 1e20, 0
        for j in range(1, k):
            cur_dis = (dest_longitude - coordinates[j][0]) ** 2 + (dest_latitude - coordinates[j][1]) ** 2
            if cur_dis < min_dis:
                min_dis, pos = cur_dis, j
        dest.append(pos)

    n = len(dest)

    datahelper.dump_json('../data/order_data.json', n, m, k, L, dest, coordinates, pb, pc, cr, cb)


if __name__ == '__main__':
    assign('../../CS214-CourseData/Projects/data/chengdu_order/order_20161105', '00:00:00', '00:09:59', 70, 20, 9.12, 0.56, 150, 1.8)
