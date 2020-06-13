import math
import tsp
import datahelper
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

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
    pole = []              # Polar coordinates
    ori = np.array([])     # The original destination

    def __init__(self, n, m, k, L, dest, coordinates, dist, pb, pc, cr, cb):
        self.n = n
        self.m = m
        self.k = k
        self.L = L
        self.dest = dest
        self.coordinates = coordinates
        self.dist = np.array(dist)
        self.pb = pb
        self.pc = pc
        self.cr = cr
        self.cb = cb
        self.p = np.zeros(n)
        self.calcPrice()
        self.ori = np.zeros(self.k, dtype=np.int)
        for i in range(self.k):
            self.ori[i] = i

    def coordinatesConvert(self):
        center_x = self.coordinates[0][0]
        center_y = self.coordinates[0][1]
        for i in range(1, self.k):
            x = self.coordinates[i][0]
            y = self.coordinates[i][1]
            angle = np.arctan((y - center_y) / (x - center_x)) * 180 / np.pi
            radius = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
            t = 0
            if radius > 12:
                t = 1
            self.pole.append((t, angle, i))
        self.pole.sort()
        for i in range(self.n):
            for j in range(self.k - 1):
                if int(self.pole[j][2]) == self.dest[i]:
                    self.ori[j + 1] = self.dest[i]
                    self.dest[i] = j + 1
                    break
        self.dest, self.p = zip(*sorted(zip(self.dest, self.p)))

    def calcPrice(self):
        for i in range(self.n):
            self.p[i] = self.pb + self.pc * self.dist[0, self.dest[i]]

    def solver(self):
        self.coordinatesConvert()
        coord_id = []
        dp = np.zeros(self.n)
        tr = np.zeros(self.n, dtype=np.int)
        pf = np.zeros((self.n, self.n))
        for i in range(self.n):
            dp[i] = -1e20
            tr[i] = -1
            income_t = 0
            coord_id.clear()
            coord_id.append(0)
            for j in range(i, max(i - self.L, -1), -1):
                if self.ori[self.dest[j]] not in coord_id:
                    coord_id.append(self.ori[self.dest[j]])
                income_t = income_t + self.p[j]
                bus_length, bus_route = tsp.tsp_coordinates_id(len(coord_id), coord_id)
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
        bus_profit.sort()
        bus_profit.reverse()
        while len(bus_profit) > 0 and bus_profit[len(bus_profit) - 1] < 0:
            bus_profit.pop()
        return bus_profit


def solver(n, m, k, L, dest, coordinates, dist, pb, pc, cr, cb):
    odrp = ODRPGDPSolver(n, m, k, L, dest, coordinates, dist, pb, pc, cr, cb)
    bus_profit = odrp.solver()
    list_m = []
    while len(bus_profit) > 0:
        list_m.append([len(bus_profit), sum(bus_profit)])
        bus_profit.pop()
    return list_m


if __name__ == '__main__':
    _n, _m, _k, _L, _dest, _coordinates, _dist, _pb, _pc, _cr, _cb = datahelper.load_json('../data/order_data.json')
    m_list = solver(_n, _m, _k, _L, _dest, _coordinates, _dist, _pb, _pc, _cr, _cb)
    m_list.reverse()
    while len(m_list) < 200:
        m_list.append([len(m_list) + 1, m_list[len(m_list) - 1][1]])
    m_list.reverse()
    m_list.append([0, 0])
    m_list.reverse()

    tx = []
    ty = []
    for item in m_list:
        tx.append(item[0])
        ty.append(item[1])
    x = np.array(tx)
    y = np.array(ty)
    xnew = np.linspace(x.min(), x.max(), 1000)
    func = interpolate.interp1d(x, y, kind='cubic')
    smooth = func(xnew)
    plt.plot(xnew, smooth)
    plt.savefig('../data/analyze_m.pdf', dpi=300)
    plt.show()

