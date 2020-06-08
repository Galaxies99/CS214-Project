import tsp_dp
import tsp_gene
import numpy as np
import math

D = 18


def tsp(n, cities):
    dist = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            dist[i][j] = math.sqrt((cities[i][0] - cities[j][0]) ** 2 + (cities[i][1] - cities[j][1]) ** 2)

    if n <= D:
        return tsp_dp.TSP_solver(n, dist)
    else:
        return tsp_gene.TSP_solver(n, dist)


def tsp_lat_lng(n, lat, lng):
    dist = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            dist[i][j] = math.sqrt((lat[i] - lat[j]) ** 2 + (lng[i] - lng[j]) ** 2)

    if n <= D:
        return tsp_dp.TSP_solver(n, dist)
    else:
        return tsp_gene.TSP_solver(n, dist)


if __name__ == '__main__':
    pass