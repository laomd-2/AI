from heapq import *


class PriorityQueue:

    def __init__(self):
        self.queue = []

    def __len__(self):
        return len(self.queue)

    def put(self, item):
        heappush(self.queue, item)

    def get(self):
        return heappop(self.queue)
