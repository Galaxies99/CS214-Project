import numpy as np
import math


def TSP_solver(n, dist):
    state_num = 2 ** n
    dp = np.ones((state_num, n)) * 1e20
    path = np.zeros((state_num, n), dtype=np.int)
    dp[1][0] = 0
    for st in range(state_num):
        for i in range(n):
            if dp[st][i] != 1e20:
                for j in range(n):
                    if st & (1 << j):
                        continue
                    # s -~-> i -> j
                    new_st = st | (1 << j)
                    if dp[st][i] + dist[i][j] < dp[new_st][j]:
                        dp[new_st][j] = dp[st][i] + dist[i][j]
                        path[new_st][j] = i
    ans = 1e20
    cur = 0
    for i in range(n):
        if dp[state_num - 1][i] + dist[i][0] < ans:
            ans = dp[state_num - 1][i] + dist[i][0]
            cur = i
    route = [0]
    st = state_num - 1
    while st != 1:
        route.append(cur)
        i = path[st][cur]
        st = (st ^ (1 << cur))
        cur = i
    route.append(0)
    route.reverse()
    return ans, route


if __name__ == '__main__':
    n = 15 + 1

    cx = [2.5, 1.2, 8.7, 3.6, -5.5, -6.6, 0.18, 12.5, 22.5, 1.61, 2.1, 0, 9.2, -1, -5, 21]
    cy = [4.0, -2.4, 1.2, 12.1, 0.94, -12.6, 5.219, 14.3609, -5.26, 4.5, -5.6, 25, -32, 7, -8, 35]

    dist = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            dist[i][j] = math.sqrt((cx[i] - cx[j]) ** 2 + (cy[i] - cy[j]) ** 2)

    ans, route = TSP_solver(n, dist)

    print('ans =', ans)
    print('route =', route)