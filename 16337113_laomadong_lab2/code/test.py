import numpy as np


if __name__ == '__main__':
    # for l1, l2 in zip(open("16337113_laomadong_Car2.csv"), open("16337113_laomadong_Car.csv")):
    #     if l1 != l2:
    #         print("llala")
    #         break
    arr = np.asarray([[0, 1, 2], [2, 3, 4], [5, 6, 7]])
    for row in arr.take((0, 2), 1).take((1, 2), 0).T:
        print(row)
