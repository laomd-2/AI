from treelib import Tree
from collections import Counter
from utils import *
import numpy as np
import math

__all__ = ["entropy", "gini_index", "DecisionTreeClassifier"]


def entropy(vector):
    count = Counter()
    for x in vector:
        count[x] += 1
    n = len(vector)
    h = 0
    for x, cnt in count.items():
        p = (cnt / n)
        h += -p * math.log2(p)
    return h


def gini_index(vector):
    count = Counter()
    for x in vector:
        count[x] += 1
    g = 0
    l = len(vector)
    for p in count.values():
        p /= l
        g += p * (1 - p)
    return g


class DecisionTreeClassifier(Tree):

    def __init__(self, property_select_policy=gini_index, punish=False):
        super(DecisionTreeClassifier, self).__init__()
        self._M = property_select_policy
        self._punish = punish
        self._X, self._y = None, None

    def fit(self, X, y):
        self._X, self._y = np.asarray(X), np.asarray(y).flatten()
        m, n = self._X.shape
        rows = list(range(m))
        cols = list(range(n))
        self._build_tree(rows, cols, self.root, "root")

    def get_params(self, deep=False):
        return {"property_select_policy": self._M,
                "punish": self._punish}

    def _build_tree(self, rows, cols, parent, branch):
        if rows:
            y = self._y[rows]
            if cols:
                if is_same(y):  # 所有样本属于同一类
                    self.create_node(tag=(branch, None, y[0]),
                                     parent=parent)
                else:
                    score_best, feature_best = None, None
                    score_y = self._M(y)
                    # col为特征编号
                    for col in cols:
                        score_j = 0
                        # 根据特征划分数据集并计算得分（频率*指标得分的和）
                        for sub_rows in divide_on_discrete_feature(self._X, col, rows).values():
                            score_j += len(sub_rows) / len(rows) \
                                       * self._M(self._y[sub_rows])
                        score_j = score_y - score_j
                        # 处理有惩罚的指标，如信息增益率
                        if self._punish:
                            feature = self._X[rows, col]
                            score_j /= self._M(feature)
                        # 找出得分最高的属性
                        if score_best is None or score_j > score_best:
                            score_best = score_j
                            feature_best = col
                    # 删除最优属性
                    cols.remove(feature_best)
                    # 根据所选属性创建新内部节点，其label根据多数投票原则得到
                    root = self.create_node(tag=(branch,
                                                 feature_best,
                                                 mode(y)),
                                            parent=parent)
                    for branch, sub_rows in divide_on_discrete_feature(self._X, feature_best, rows).items():
                        self._build_tree(sub_rows, cols[:], root, branch)
            else:  # 属性为空，多数投票的label作为叶节点label
                self.create_node(tag=(branch, None, mode(y)),
                                 parent=parent)
        else:  # 训练集为空，父节点label作为叶节点的label
            label = None
            if parent is not None:
                label = parent.tag[2]
            self.create_node(tag=(branch, None, label),
                             parent=parent)

    def predict(self, X):
        tmp = []
        cnt = 0
        for x in X:
            label, is_leaf = self._predict(x, self.root)
            tmp.append(label)
            cnt += not is_leaf
        # print(cnt)
        tmp = np.asarray(tmp)
        return tmp

    def _predict(self, test_data, node_id):
        while True:
            node = self.get_node(node_id)
            # tag[1]存储划分属性
            pro = node.tag[1]
            # 到了叶节点
            if pro is None:
                break
            # 取测试数据某一属性的值
            condition = test_data[pro]
            # 匹配当前节点的每个子节点
            for child in self.children(node_id):
                if child.tag[0] == condition:
                    node_id = child.identifier
                    break
            else:
                break
        return node.tag[2], node.is_leaf()
