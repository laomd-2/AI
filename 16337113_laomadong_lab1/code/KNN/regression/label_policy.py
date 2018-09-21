def regression_label_policy(k_neighbors):
    y = [0.0] * 6
    y_sum = 0
    while k_neighbors:
        dis, the_label = k_neighbors.get()
        for i in range(len(the_label)):
            tmp = the_label[i] / (-dis + 1 + 0.000001)
            y[i] += tmp
            y_sum += tmp
    for i in range(len(y)):
        y[i] /= y_sum
    return tuple(y)
