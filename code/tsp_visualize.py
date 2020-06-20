import tsp
import datahelper
import csvreader
import matplotlib.pyplot as plt

if __name__ == '__main__':
    departure_dat = csvreader.csv_reader_no_headers('../data/departure.csv')
    dest_dat = csvreader.csv_reader_no_headers('../data/destination.csv')
    point = [[float(departure_dat[0][0]), float(departure_dat[0][1])]]
    for item in dest_dat:
        point.append([float(item[0]), float(item[1])])
    dist = datahelper.get_dist()
    dis, route = tsp.tsp(len(dist), dist)
    print(route)
    px, py = [], []
    for item in point:
        px.append(item[0])
        py.append(item[1])
    plt.plot(px[1:], py[1:], 'ro', markersize=5)
    plt.plot(px[:1], py[:1], 'go', markersize=10)
    for i in range(len(route) - 1):
        ax, ay = px[route[i]], py[route[i]]
        bx, by = px[route[i + 1]], py[route[i + 1]]
        plt.arrow(ax, ay, bx - ax, by - ay,
                  length_includes_head=True,
                  fc='blue', ec='blue')
    plt.savefig('../data/tsp.pdf', dpi=300)
    plt.show()
