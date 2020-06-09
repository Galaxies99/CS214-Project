import order_filter
import csv
from pyecharts.charts import HeatMap
from pyecharts import options as opts


if __name__ == '__main__':
    departure_cnt = {}
    dat = order_filter.filter_night("../../CS214-CourseData/Projects/data/chengdu_order/order_20161105")
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

    x_axis = []
    y_axis = []
    for i in range(10380, 10430, 2):
        x_axis.append(i / 100.0)
    for j in range(3040, 3100, 2):
        y_axis.append(j / 100.0)

    data = [[i, j, 0] for i in range(len(x_axis)) for j in range(len(y_axis))]

    for item in departure:
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
        .render("../data/heatmap.html")
    )
