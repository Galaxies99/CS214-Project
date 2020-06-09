import tsp_dp
import tsp_gene
import numpy as np
import math

D = 18


def tsp(n, dist):
    if n <= D:
        return tsp_dp.TSP_solver(n, dist)
    else:
        return tsp_gene.TSP_solver(n, dist, False)


def tsp_coordinates(n, coordinates):
    dist = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            dist[i][j] = math.sqrt((coordinates[i][0] - coordinates[j][0]) ** 2 +
                                   (coordinates[i][1] - coordinates[j][1]) ** 2)

    if n <= D:
        return tsp_dp.TSP_solver(n, dist)
    else:
        return tsp_gene.TSP_solver(n, dist, False)


def tsp_lat_lng(n, lat, lng):
    dist = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            dist[i][j] = math.sqrt((lat[i] - lat[j]) ** 2 + (lng[i] - lng[j]) ** 2)

    if n <= D:
        return tsp_dp.TSP_solver(n, dist)
    else:
        return tsp_gene.TSP_solver(n, dist, False)


if __name__ == '__main__':
    pass
