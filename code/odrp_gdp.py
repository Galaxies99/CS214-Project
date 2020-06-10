import math
import tsp
import datahelper
import numpy as np


class ODRPGDPSolver(object):
    n = 0                  # The number of orders.
    dest = []              # The destination of orders.
    p = np.array([])       # The price of orders
    coordinates = []       # The coordinates of stations.
    m = 0                  # The number of buses.
    k = 51                 # The number of **stations** (destination + departure) (departure id: 0).
    L = 50                 # The limit of buses.
    dist = np.array([])    # The distance between two destinations.
    cr = 0                 # The fixed cost per bus
    cb = 0                 # The fuel cost
    pb = 0                 # price parameter.
    pc = 0                 # price parameter.
    pole = np.array([])    # Polar coordinates

    def __init__(self, n, m, k, L, dest, coordinates, pb, pc, cr, cb):
        self.n = n
        self.m = m
        self.k = k
        self.L = L
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

    def calcDistance(self):
        for i in range(self.k):
            for j in range(self.k):
                self.dist[i][j] = math.sqrt((self.coordinates[i][0] - self.coordinates[j][0]) ** 2 +
                                            (self.coordinates[i][1] - self.coordinates[j][1]) ** 2)

    def coordinatesConvert(self):
        center_x = self.coordinates[0][0]
        center_y = self.coordinates[0][1]
        self.pole = np.zeros((self.k - 1, 3), dtype=np.float)
        for i in range(1, self.k):
            x = self.coordinates[i][0], y = self.coordinates[i][1]
            self.pole[i - 1][0] = np.arctan((y - center_y) / (x - center_x)) * 180 / np.pi
            self.pole[i - 1][1] = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
            self.pole[i - 1][2] = i
        self.pole = np.lexsort(self.pole[::-1, :])
        for i in range(self.n):
            for j in range(self.k - 1):
                if self.pole[j][2] == self.dest[i]:
                    self.dest[i] = j
        self.dest, self.p = zip(*sorted(zip(self.dest, self.p)))

    def calcPrice(self):
        for i in range(self.n):
            self.p[i] = self.pb + self.pc * self.dist[self.dest[i], 0]

    def solver(self):
        coord = []
        dp = np.zeros(self.n)
        tr = np.zeros(self.n, dtype=np.int)
        pf = np.zeros((self.n, self.n))
        for i in range(self.n):
            dp[i] = -1e20
            tr[i] = -1
            income_t = 0
            coord.clear()
            coord.append(self.coordinates[0])
            for j in range(i, max(i - self.L, -1), -1):
                print('Status: ', i, j)
                if self.coordinates[self.dest[j]] not in coord:
                    coord.append(self.coordinates[self.dest[j]])
                income_t = income_t + self.p[j]
                bus_length, bus_route = tsp.tsp_coordinates(len(coord), coord)
                pf[j][i] = income_t - self.cr - self.cb * bus_length
                pre_dp = 0
                if j != 0:
                    pre_dp = dp[j - 1]
                if pre_dp + pf[j][i] > dp[i]:
                    dp[i] = pre_dp + pf[j][i]
                    tr[i] = j - 1
        cur = self.n - 1
        bus_profit = []
        while cur != -1:
            lst = tr[cur]
            bus_profit.append(pf[lst + 1][cur])
            cur = lst
        print(len(bus_profit))
        if len(bus_profit) > self.m:
            bus_profit.sort()
            bus_profit.reverse()
            bus_profit = bus_profit[:self.m]
        total_profit = np.sum(bus_profit)
        return total_profit


def solver(n, m, k, L, dest, coordinates, pb, pc, cr, cb):
    odrp = ODRPGDPSolver(n, m, k, L, dest, coordinates, pb, pc, cr, cb)
    profit = odrp.solver()
    print(profit)


if __name__ == '__main__':
    _n, _m, _k, _L, _dest, _coordinates, _pb, _pc, _cr, _cb = datahelper.load_json('../data/order_data.json')
    solver(_n, _m, _k, _L, _dest, _coordinates, _pb, _pc, _cr, _cb)

