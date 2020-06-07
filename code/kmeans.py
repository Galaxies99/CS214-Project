import csvreader
import random


def kmeans_step(K, D, data, bel, center, min_arg, max_arg):
    loss = 0
    # Calculate current total loss.
    for i, item in enumerate(data):
        # Choose the nearest center.
        min_loss, pos = 1e9, 0
        for j in range(0, K):
            dis = 0
            for d in range(D):
                dis += (center[j][d] - item[d]) ** 2
            if dis < min_loss:
                min_loss, pos = dis, j
        bel[i] = pos
        loss += min_loss

    num = []
    for i in range(K):
        for d in range(D):
            center[i][d] = 0
        num.append(0)

    # Calculate new center.
    for i in range(len(data)):
        for d in range(D):
            center[bel[i]][d] += data[i][d]
        num[bel[i]] += 1

    for i in range(0, K):
        if num[i] != 0:
            for d in range(D):
                center[i][d] /= num[i]
        else:
            for d in range(D):
                center[i][d] = random.randint(min_arg[d], max_arg[d])

    return loss


def kmeans(K, D, min_arg, max_arg, data):
    # Randomly choose K centers.
    center = []
    for i in range(0, K):
        x = []
        for d in range(D):
            x.append(random.randint(min_arg[d], max_arg[d]))
        center.append(x)

    bel = []
    for item in data:
        bel.append(0)

    ori_loss = kmeans_step(K, D, data, bel, center, min_arg, max_arg)
    while True:
        loss = kmeans_step(K, D, data, bel, center, min_arg, max_arg)
        if abs(loss - ori_loss) < 1e-3:
            break
        ori_loss = loss

    return center, bel


if __name__ == '__main__':
    pass