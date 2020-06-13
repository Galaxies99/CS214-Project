import csvreader
import json
import numpy as np
import time
from urllib.request import urlopen


if __name__ == '__main__':
    dest_dat = csvreader.csv_reader_no_headers('../data/destination.csv')
    departure_dat = csvreader.csv_reader_no_headers('../data/departure.csv')

    ak = '??????????????????' # Please fill in your AK code

    coordinates = [[float(departure_dat[0][0]), float(departure_dat[0][1])]]

    for line in dest_dat:
        coordinates.append([float(line[0]), float(line[1])])

    K = len(coordinates)

    new_coordinates = []

    dist = np.zeros((K, K))

    for i in range(K):
        for j in range(K):
            print(i, j)
            if i == j:
                dist[i][j] = 0
            else:
                uri = 'http://api.map.baidu.com/routematrix/v2/driving?output=json&origins=' + str(coordinates[i][1]) + ',' + \
                    str(coordinates[i][0]) + '&destinations=' + str(coordinates[j][1]) + ',' + str(coordinates[j][0]) + '&ak=' + ak
                uh = urlopen(uri)
                data = uh.read().decode()
                js = json.loads(data)
                print(uri)
                print(js)
                if js['status'] != 0:
                    time.sleep(5)
                    uh = urlopen(uri)
                    data = uh.read().decode()
                    js = json.loads(data)

                dist[i][j] = js['result'][0]['distance']['value'] / 1000

    dist_dict = {'dist': dist.tolist()}
    with open('../data/dist.json', 'w') as file:
        json.dump(dist_dict, file)

