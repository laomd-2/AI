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
        # (余弦距离，label)二元组的最小堆
        k_neighbors = PriorityQueue()
        for other_x, y in self._trained_datas:
            dis = self._distance_policy(test_x, other_x)
            if math.fabs(dis - self._distance_policy(other_x, other_x)) < 0.000001:
                return y
            k_neighbors.put((dis, y))
            # 至多存储k个邻居
            if len(k_neighbors) > self._k:
                k_neighbors.get()
        # 从k个最近邻居中决定测试样本的label的策略，用户代码中自定义
        # 好处在于可以针对不同类型问题（如分类和回归），不同加权方法得到label
        label = self._label_policy(k_neighbors)
        return label
