from knn_collections import PriorityQueue
from collections import Counter
import math


class KNN:

    def __init__(self, distance):
        self._distance = distance
        self._trained_datas = []

    def add(self, trained_x, trained_y):
        self._trained_datas.append((trained_x, trained_y))

    def predict(self, test_x, k=0):
        if k <= 0:
            k = math.sqrt(len(self._trained_datas))
        k_neighbors = PriorityQueue()
        for other_x, y in self._trained_datas:
            dis = self._distance(test_x, other_x)
            if dis == 0:
                self.add(test_x, y)
                return y
            k_neighbors.put((dis, y))
            if len(k_neighbors) > k:
                k_neighbors.get()
        label = None
        cur_max = 0
        counter = Counter()
        while k_neighbors:
            neighbor, the_label = k_neighbors.get()
            counter[the_label] += 1
            if counter[the_label] > cur_max:
                cur_max = counter[the_label]
                label = the_label
        self.add(test_x, label)
        return label
