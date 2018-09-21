from heapq import *
import math

__all__ = ["KNN"]


class PriorityQueue:

    def __init__(self):
        self.queue = []

    def __len__(self):
        return len(self.queue)

    def put(self, item):
        heappush(self.queue, item)

    def get(self):
        return heappop(self.queue)


class KNN:

    def __init__(self, k, distance_policy, label_policy):
        self._k = k
        self._distance_policy = distance_policy
        self._label_policy = label_policy
        self._trained_datas = []

    def add(self, trained_x, trained_y):
        self._trained_datas.append((trained_x, trained_y))

    def predict(self, test_x):
        k_neighbors = PriorityQueue()
        for other_x, y in self._trained_datas:
            dis = self._distance_policy(test_x, other_x)
            if math.fabs(dis - self._distance_policy(other_x, other_x)) < 0.000001:
                return y
            k_neighbors.put((dis, y))
            if len(k_neighbors) > self._k:
                k_neighbors.get()
        label = self._label_policy(k_neighbors)
        # self.add(test_x, label)
        return label
