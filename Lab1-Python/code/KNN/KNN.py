from knn_collections import PriorityQueue
from collections import Counter

__all__ = ["KNN"]


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
            k_neighbors.put((dis, y))
            if len(k_neighbors) > self._k:
                k_neighbors.get()
        label = self._label_policy(k_neighbors)
        self.add(test_x, label)
        return label
