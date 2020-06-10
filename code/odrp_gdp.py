import numpy as np
import math
import tsp
import copy
import datahelper
import numpy as np

'''
将经纬度转换为极坐标
'''

# 将直角坐标转换为极坐标，可以用坐标中最小的点为极点，也可以用(0,0)为极点
# 半径
def get_radius(x, y, x_min, y_min):
    r = np.sqrt((x - x_min) ** 2 + (y - y_min) ** 2)
    # r = np.sqrt((x **2+y **2))
    return r

# 角度
def get_angle(x, y, x_min, y_min):
    a = np.arctan((y - y_min) / (x - x_min)) * 180 / np.pi
    # a = np.arctan(y / x * 180 / np.pi)
    return a

class ODRPGDPSolver(object):
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
    pole = np.array([])

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

    def coordinate_convert(self):
        df = np.array(self.coordinates)

        # 纬度latitude，经度longitude
        loc_x = [x[0] for x in df]
        loc_y = [x[1] for x in df]


        # 将最小的点设为极点
        x_min = df[0][0]
        y_min = df[0][1]

        radius = []
        angle = []
        self.pole = np.zeros((3, len(loc_x) - 1), dtype=np.float)
        for i in range(0, len(loc_x) - 1):
            self.pole[2][i] = i + 1

        for x, y in zip(loc_x, loc_y):
            if x != x_min and y != y_min:
                radius.append(get_radius(x, y, x_min, y_min))
                angle.append(get_angle(x, y, x_min, y_min))

        radius = np.array(radius)
        angle = np.array(angle)

        # 保留小数点后8位
        self.pole[1] = radius.round(decimals=8)
        #print(radius.round(decimals=8));
        self.pole[0] = angle.round(decimals=8)
        #print(angle.round(decimals=8))
        self.pole = self.pole.T[np.lexsort(self.pole[::-1,:])].T
        for i in range(0,self.n):
            self.dest[i] = int(self.pole[2][self.dest[i] - 1])
        self.dest, self.p = zip(*sorted(zip(self.dest, self.p)))
        print(self.dest, self.p);
        return self.pole

    def calcPrice(self):
        for i in range(self.n):
            self.p[i] = self.pb + self.pc * self.dist[self.dest[i], 0]

    def solver(self):
        p = self.coordinate_convert()
        #print(p)

        coord = []
        dp = np.zeros((1, self.n + 1), dtype=np.int)
        pf = np.zeros((self.n + 1, self.n + 1), dtype=np.float)
        for i in range(1, self.n + 1):
            dp[0][i] = -100000
            for j in range(max(i-self.L, 0), i):
                print(i,j)
                coord.clear()
                coord.append(self.coordinates[0])
                for k in range(j + 1, i):
                    destination = self.dest[k]
                    if self.coordinates[destination] not in coord:
                        coord.append(self.coordinates[destination])
                    pf[i][j] += self.p[k]
                bus_length, bus_route = tsp.tsp_coordinates(len(coord), coord)
                pf[i][j] -= self.cr + self.cb * bus_length
                if dp[0][i] <= dp[0][j] + pf[i][j]:
                    dp[0][i] = dp[0][j] + pf[i][j]

        print(dp[0])
        print(pf)
        i = self.n
        num = 0
        Profit = []
        #Profit = np.zeros(self.n)
        bus = np.zeros(self.n + 1)
        while i > 0:
            for j in range(max(i-self.L, 0), i):
                print(i,j)
                coord.clear()
                coord.append(self.coordinates[0])
                pf = 0
                for k in range(j + 1, i):
                    destination = self.dest[k]
                    if self.coordinates[destination] not in coord:
                        coord.append(self.coordinates[destination])
                    pf += self.p[k]
                pf -= self.cr + self.cb * bus_length
                if(dp[0][i] == dp[0][j] + pf[i][j]):
                    bus[i] = j
                    i = j
                    Profit.append(dp[i]-dp[j])
                    num += 1
        Profit.sort()
        if num > m:
            Profit = Profit[:m]
        return Profit


def solver(n, m, k, L, dest, coordinates, pb, pc, cr, cb):
    odrp = ODRPGDPSolver(n, m, k, L, dest, coordinates, pb, pc, cr, cb)
    odrp.solver()
    #Profit = odrp.solver()
    #return Profit


if __name__ == '__main__':
    _n, _m, _k, _L, _dest, _coordinates, _pb, _pc, _cr, _cb = datahelper.load_json('../data/order_data.json')

    solver(_n, _m, _k, _L, _dest, _coordinates, _pb, _pc, _cr, _cb)
    # Profit = solver(_n, _m, _k, _L, _dest, _coordinates, _pb, _pc, _cr, _cb)
    # total_profit = 0
    # for i in range(0,len(Profit)):
    #     total_profit += Profit[i]
    # print(Profit)
    # print('total profit:',total_profit)
