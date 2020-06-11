import tsp_dp
import tsp_gene
import numpy as np
import datahelper
import math

D = 12


def tsp(n, dist):
    if n <= D:
        return tsp_dp.TSP_solver(n, dist)
    else:
        return tsp_gene.TSP_solver(n, dist, False)


def tsp_coordinates_id(n, coordinates_id):
    t_dist = datahelper.get_dist()

    dist = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            dist[i][j] = t_dist[coordinates_id[i]][coordinates_id[j]]

    if n <= D:
        return tsp_dp.TSP_solver(n, dist)
    else:
        return tsp_gene.TSP_solver(n, dist, False)


def tsp_coordinates_id_opt(n, coordinates_id):
    t_dist = datahelper.get_dist()

    dist = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            dist[i][j] = t_dist[coordinates_id[i]][coordinates_id[j]]

    return tsp_dp.TSP_solver(n, dist)


if __name__ == '__main__':
    pass
