from collections import Counter
from treelib import Tree

__all__ = ["DecisionTreeClassifier"]


class DecisionTreeClassifier(Tree):

    def __init__(self, train_datas, property_select_policy):
        super(DecisionTreeClassifier, self).__init__()
        self._train_datas = train_datas
        rows = set(range(len(train_datas)))
        cols = set(range(len(train_datas[0]) - 1))
        self._build_tree(rows, cols, property_select_policy)

    def get_col(self, col, rows):
        if col is None:
            return None
        return [self._train_datas[row][col] for row in rows]

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
        if rows:
            y = self.get_col(-1, rows)
            if cols:
                # 所有样本属于同一类
                if self._is_same(y):
                    self.create_node(tag=(branch, None, y[0]), parent=parent)
                else:
                    properties = [(col, self.get_col(col, rows)) for col in cols]
                    best_pro = property_select_policy(properties, y)
                    cols.remove(best_pro)

                    self.create_node(tag=(branch, best_pro, self.vote(y)),
                                     identifier=best_pro,
                                     parent=parent)

                    branches = dict()
                    best_col = self.get_col(best_pro, rows)
                    for x, row in zip(best_col, rows):
                        branches.setdefault(x, set())
                        branches[x].add(row)

                    for branch, brc_rows in branches.items():
                        self._build_tree(brc_rows, cols, property_select_policy, best_pro, branch)
            else:
                self.create_node(tag=(branch, None, self.vote(y)), parent=parent)

    def vote(self, vector):
        count = Counter()
        max_num = 0
        res = None
        for x in vector:
            count[x] += 1
            if count[x] > max_num:
                max_num = count[x]
                res = x
        return res

    def predict(self, test_data):
        pro = self.root
        node = None
        path = []
        while pro:
            node = self.get_node(pro)
            path.append(pro)
            condition = test_data[pro]
            for child in self.children(pro):
                if child.tag[0] == condition:
                    pro = child.tag[1]
                    node = child
                    break
            else:
                break
        return node.tag[2], path
