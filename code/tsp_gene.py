import numpy as np
import math


class TSP(object):
    n = 15
    dist = np.array([])
    pop = np.array([])
    fitness = np.array([])
    pop_size = 50
    c_rate = 0.7
    m_rate = 0.05
    epoch_num = 200
    best_dis = -1
    best_gen = np.array([])

    def __init__(self, n, dist, c_rate, m_rate, pop_size, epoch_num):
        self.n = n
        self.dist = dist
        self.pop_size = pop_size
        self.c_rate = c_rate
        self.m_rate = m_rate
        self.epoch_num = epoch_num
        self.fitness = np.zeros(self.pop_size)

    def init(self):
        pop_t = []
        for i in range(self.pop_size):
            gene = np.arange(self.n)
            np.random.shuffle(gene)
            pop_t.append(gene)
        self.pop = np.array(pop_t)
        self.fitness = self.calc_fitness(self.pop)

    def calc_dist(self, gene):
        dis = 0.0
        for i in range(self.n):
            dis += self.dist[gene[i - 1]][gene[i]]
        return dis

    def calc_fitness(self, pop):
        res = np.array([])
        for i in range(pop.shape[0]):
            dis = self.best_dis / self.calc_dist(pop[i])
            res = np.append(res, dis)
        return res

    def mutate(self, gene):
        if np.random.rand() > self.m_rate:
            return gene
        index1 = np.random.randint(0, self.n)
        index2 = np.random.randint(index1, self.n)
        new_gene = []
        for i in range(self.n):
            if index1 <= i < index2:
                new_gene.append(gene[index2 - i + index1 - 1])
            else:
                new_gene.append(gene[i])
        return np.array(new_gene)

    def cross(self, gene1, gene2):
        if np.random.rand() > self.c_rate:
            return gene1
        index1 = np.random.randint(0, self.n)
        index2 = np.random.randint(index1, self.n)
        t_gene = gene2[index1:index2]
        new_gene = []
        glen = 0
        for g in gene1:
            if glen == index1:
                new_gene.extend(t_gene)
            if g not in t_gene:
                new_gene.append(g)
            glen += 1
        return np.array(new_gene)

    def select_pop(self, pop, fitness):
        best_index = np.argmax(fitness)
        med = np.median(fitness, axis=0)
        for i in range(self.pop_size):
            if i != best_index and fitness[i] < med:
                new_gene = self.cross(pop[best_index], pop[i])
                new_gene = self.mutate(new_gene)
                pop[i, :] = new_gene[:]
        return pop

    def calc_local_fitness(self, gene, i):
        di = self.dist[gene[i]][gene[i - 1]]
        od = []
        for j in range(self.n):
            if i != j:
                od.append(self.dist[gene[i]][gene[i - 1]])
        mind = np.min(od)
        loc_fitness = di - mind
        return loc_fitness

    def EO(self, gene):
        local_fitness = []
        for i in range(self.n):
            local_fitness.append(self.calc_local_fitness(gene, i))
        max_i = np.argmax(local_fitness)
        max_gene = np.copy(gene)
        for j in range(int(max_i)):
            k = max_i
            while k < self.n:
                t_gene = np.copy(max_gene)
                gene[j], gene[k] = gene[k], gene[j]
                dis_max = self.calc_dist(max_gene)
                dis_t = self.calc_dist(t_gene)
                if dis_max > dis_t:
                    max_gene = gene[:]
                k += 1
        return max_gene

    def evolution(self, output):
        for epoch in range(self.epoch_num):
            best_index = np.argmax(self.fitness)
            worst_index = np.argmin(self.fitness)
            local_best_gen = self.pop[best_index]
            local_best_dis = self.calc_dist(local_best_gen)

            if epoch == 0:
                self.best_dis = local_best_dis
                self.best_gen = local_best_gen

            if local_best_dis < self.best_dis:
                self.best_dis = local_best_dis
                self.best_gen = local_best_gen
            else:
                self.pop[worst_index] = self.best_gen

            if output:
                print('epoch =', epoch)
                print('|-- best dist =', self.best_dis)
                print('|-- best gen =', self.best_gen)

            self.pop = self.select_pop(self.pop, self.fitness)
            self.fitness = self.calc_fitness(self.pop)

            for i in range(self.pop_size):
                j = np.random.randint(self.pop_size)
                if i != j:
                    self.pop[i] = self.cross(self.pop[i], self.pop[j])
                    self.pop[i] = self.mutate(self.pop[i])

            self.best_gen = self.EO(self.best_gen)
            self.best_dis = self.calc_dist(self.best_gen)


def TSP_solver(n, dist, output):
    tsp = TSP(n, dist, 0.6, 0.1, 100, 200)
    tsp.init()
    tsp.evolution(output)
    t_route = list(tsp.best_gen)
    pos = t_route.index(0)
    res_route = t_route[pos:] + t_route[:pos]
    res_route.append(0)
    return tsp.best_dis, res_route


if __name__ == '__main__':
    N = 15 + 1

    cx = [2.5, 1.2, 8.7, 3.6, -5.5, -6.6, 0.18, 12.5, 22.5, 1.61, 2.1, 0, 9.2, -1, -5, 21]
    cy = [4.0, -2.4, 1.2, 12.1, 0.94, -12.6, 5.219, 14.3609, -5.26, 4.5, -5.6, 25, -32, 7, -8, 35]

    Dist = np.zeros((N, N))

    for ii in range(N):
        for jj in range(N):
            Dist[ii][jj] = math.sqrt((cx[ii] - cx[jj]) ** 2 + (cy[ii] - cy[jj]) ** 2)

    ans, route = TSP_solver(N, Dist, True)

    print('ans =', ans)
    print('route =', route)