from collections import Counter
from treelib import Tree
import numpy as np
from property_select_policy import *


__all__ = ["DecisionTreeClassifier"]


class DecisionTreeClassifier(Tree):

    def __init__(self, property_select_policy=gini_policy):
        super(DecisionTreeClassifier, self).__init__()
        self._M = property_select_policy
        self._X, self._y = None, None

    def fit(self, X, y):
        self._X, self._y = np.asarray(X), np.asarray(y).flatten()
        m, n = self._X.shape
        rows = list(range(m))
        cols = list(range(n))
        self._build_tree(rows, cols)

    @staticmethod
    def _is_same(iterable):
        last = None
        for x in iterable:
            if last:
                if last != x:
                    return False
            last = x
        return last is not None

    def _build_tree(self, rows, cols, parent=None, branch="root"):
        # 训练集为空或者属性为空
        if rows:
            y = self._y.take(rows, 0)
            # print(y)
            if cols:
                # 所有样本属于同一类
                if self._is_same(y):
                    root = self.create_node(tag=(branch, None, y[0]), parent=parent)
                else:
                    score_best = None
                    feature_best = None
                    for col in cols:
                        score_j = 0
                        for sub_rows in self._divide(col, rows).values():
                            score_j += len(sub_rows) / len(rows) \
                            * self._M(y, self._y.take(sub_rows, 0), 
                                      self._X.take(rows, 0).take((col, ), 1).T)
                        if score_best is None or score_j > score_best:
                            score_best = score_j
                            feature_best = col
                    root = self.create_node(tag=(branch, feature_best, self._vote(y)), parent=parent)
                    cols.remove(feature_best)
                    for branch, sub_rows in self._divide(feature_best, rows).items():
                        sub_tree = self._build_tree(sub_rows, cols, root, branch)
                        root.add_children(sub_tree)
            else:
                root = self.create_node(tag=(branch, None, self._vote(y)), parent=parent)
        else:
            root = self.create_node(tag=(branch, None, parent.tag[2]), parent=parent)
        return root

    def _divide(self, feature, rows):
        res = dict()
        for row in rows:
            branch = self._X[row, feature]
            res.get(branch, []).append(row)
        return res
    
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
        # print(cnt)
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
