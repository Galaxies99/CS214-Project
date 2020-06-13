import csv
import order_filter


if __name__ == '__main__':
    txt_file = '../../CS214-CourseData/Projects/data/haikou_order/dwv_order_make_haikou_8.txt'
    csv_file = '../../CS214-CourseData/Projects/data/haikou_order/order_20171011_20171014.csv'

    in_txt = csv.reader(open(txt_file, "r"), delimiter='\t')
    out_csv = csv.writer(open(csv_file, 'w', newline=''), dialect='excel')

    next(in_txt)
    for item in in_txt:
        depart_time = item[12]
        arrive_time = item[11]

        # Invalid orders
        if item[12] == '0000-00-00 00:00:00' or item[11] == '0000-00-00 00:00:00':
            continue
        if order_filter.datetime_timestamp(depart_time) > order_filter.datetime_timestamp(arrive_time):
            continue

        date = depart_time[:10]
        time = depart_time[11:]

        # Not our parts
        if date < '2017-10-11' or date > '2017-10-14':
            continue

        # Not night
        if '06:00:00' <= time < '23:00:00':
            continue

        row = [item[15], order_filter.datetime_timestamp(depart_time), order_filter.datetime_timestamp(arrive_time),
               float(item[19]), float(item[20]), float(item[17]), float(item[18])]
        out_csv.writerow(row)
