import numpy as np
import math
import tsp
import copy
import datahelper


class ODRPOptSolver(object):
    n = 0                  # The number of orders.
    dest = []              # The destination of orders.
    p = np.array([])       # The price of orders
    coordinates = []       # The coordinates of stations.
    m = 0                  # The number of buses.
    k = 51                 # The number of **stations** (destination + departure) (departure id: 0).
    L = 50                 # The limit of buses.
    dist = np.array([])    # The distance between two destinations.
    b = np.array([])       # The order dispatch plan.
    B = []                 # The passenger on bus j.
    D = []                 # The destination of bus j.
    cr = 0                 # The fixed cost per bus
    cb = 0                 # The fuel cost
    pb = 0                 # price parameter.
    pc = 0                 # price parameter.
    best_profit = -1e20    # best profit.
    best_b = np.array([])  # best order dispatch plan.
    best_route = []        # best TSP route.
    LL = 0                 # The limit of buses (lower bound)

    def __init__(self, n, m, k, L, dest, coordinates, pb, pc, cr, cb):
        self.n = n
        self.m = m
        self.k = k
        self.L = L
        self.LL = int(cr / 20)
        self.dest = dest
        self.coordinates = coordinates
        self.dist = np.zeros((k, k))
        self.calcDistance()
        self.pb = pb
        self.pc = pc
        self.cr = cr
        self.cb = cb
        self.p = np.zeros(n)
        self.calcPrice()
        self.b = np.zeros(n)
        for i in range(m + 1):
            self.B.append([])
            self.D.append([])

    def calcDistance(self):
        for i in range(self.k):
            for j in range(self.k):
                self.dist[i][j] = math.sqrt((self.coordinates[i][0] - self.coordinates[j][0]) ** 2 +
                                            (self.coordinates[i][1] - self.coordinates[j][1]) ** 2)

    def enumerateOrder(self, i, cur_j):
        if i == self.n:
            for j in range(1, cur_j):
                if len(self.B[j]) < self.LL:
                    return
            profit, route = self.calcProfit(cur_j)
            if profit > self.best_profit:
                self.best_profit = profit
                self.best_b = np.copy(self.b)
                self.best_route = copy.deepcopy(route)
            return
        for j in range(1, min(cur_j + 1 + 1, self.m + 1)):
            if len(self.B[j]) == self.L:      # already full
                continue
            self.b[i] = j
            self.B[j].append(i)
            if j == cur_j + 1:
                self.enumerateOrder(i + 1, cur_j + 1)
            else:
                self.enumerateOrder(i + 1, cur_j)
            self.B[j].pop()
        self.b[i] = 0
        self.B[0].append(i)
        self.enumerateOrder(i + 1, cur_j)
        self.B[0].pop()

    def calcProfit(self, bus_num):
        profit = 0
        for i in range(self.n):
            if self.b[i] != 0:
                profit += self.p[i]
        profit -= bus_num * self.cr
        coord = []
        route = []
        for j in range(1, bus_num + 1):
            for passenger in self.B[j]:
                if self.dest[passenger] not in self.D[j]:
                    self.D[j].append(self.dest[passenger])
            coord.clear()
            coord.append(self.coordinates[0])
            for destination in self.D[j]:
                coord.append(self.coordinates[destination])
            bus_length, bus_route = tsp.tsp_coordinates(len(coord), coord)
            profit -= bus_length * self.cb
            for i, item in enumerate(bus_route):
                if item != 0:
                    bus_route[i] = self.D[j][item - 1]
            route.append(bus_route)
        return profit, route

    def calcPrice(self):
        for i in range(self.n):
            self.p[i] = self.pb + self.pc * self.dist[self.dest[i], 0]

    def solver(self):
        self.enumerateOrder(0, 0)
        return self.best_profit, self.best_route


def solver(n, m, k, L, dest, coordinates, pb, pc, cr, cb):
    odrp = ODRPOptSolver(n, m, k, L, dest, coordinates, pb, pc, cr, cb)
    profit, route = odrp.solver()
    return profit, route


if __name__ == '__main__':
    _n, _m, _k, _L, _dest, _coordinates, _pb, _pc, _cr, _cb = datahelper.load_json('../data/order_data.json')
    Profit, Route = solver(_n, _m, _k, _L, _dest, _coordinates, _pb, _pc, _cr, _cb)
    print('Profit =', Profit)
    print('Route =', Route)
