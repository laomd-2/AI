from collections import Counter
from treelib import Tree
import numpy as np
from property_select_policy import *


__all__ = ["DecisionTreeClassifier"]


class DecisionTreeClassifier(Tree):

    def __init__(self):
        super(DecisionTreeClassifier, self).__init__()
        self._X, self._y = None, None

    def fit(self, X, y, property_select_policy=gini_policy):
        self._X, self._y = np.asarray(X), np.asarray(y).flatten()
        m, n = self._X.shape
        rows = list(range(m))
        cols = list(range(n))
        self._build_tree(rows, cols, property_select_policy)

    @staticmethod
    def _is_same(iterable):
        last = None
        for x in iterable:
            if last:
                if last != x:
                    return False
            last = x
        return last is not None

    def _build_tree(self, rows, cols, property_select_policy, parent=None, branch="root"):
        # 训练集为空或者属性为空
        # print(rows)
        if rows:
            y = self._y.take(rows, 0)
            # print(y)
            if cols:
                # 所有样本属于同一类
                if self._is_same(y):
                    self.create_node(tag=(branch, None, y[0]), parent=parent)
                else:
                    properties = self._X.take(rows, 0).take(cols, 1).T
                    tmp = property_select_policy(properties, y)
                    best_pro = cols[tmp]
                    best_col = properties[tmp]
                    # cols.pop(tmp)

                    root = self.create_node(tag=(branch, best_pro, self._vote(y)),
                                            parent=parent)

                    branches = dict()
                    for x, row in zip(best_col, rows):
                        branches.setdefault(x, [])
                        branches[x].append(row)

                    for branch, brc_rows in branches.items():
                        self._build_tree(brc_rows, cols, property_select_policy, root.identifier, branch)
            else:
                self.create_node(tag=(branch, None, self._vote(y)), parent=parent)

    def _vote(self, vector):
        count = Counter()
        max_num = 0
        res = None
        for x in vector:
            count[x] += 1
            if count[x] > max_num:
                max_num = count[x]
                res = x
        return res

    def predict(self, X):
        tmp = []
        cnt = 0
        for x in X:
            label, is_leaf = self._predict(x, self.root)
            tmp.append(label)
            cnt += not is_leaf
        print(cnt)
        return np.asarray(tmp)

    def _predict(self, test_data, node_id):
        while True:
            node = self.get_node(node_id)
            pro = node.tag[1]
            if pro is None:
                break
            condition = test_data[pro]
            for child in self.children(node_id):
                if child.tag[0] == condition:
                    node_id = child.identifier
                    break
            else:
                break
        return node.tag[2], node.is_leaf()
