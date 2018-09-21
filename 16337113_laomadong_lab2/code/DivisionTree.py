from collections import Counter

__all__ = ["DivisionTree"]


class TreeNode:
    def __init__(self, property, condition, label, children):
        self.property = property
        self.condition = condition
        self.label = label
        self.children = children


class Tree:

    @staticmethod
    def _pre_order(root, end):
        if root:
            print("(", root.condition, root.property, root.label, ")")
            end += '\t'
            for child in root.children:
                print(end, end='')
                Tree._pre_order(child, end)

    def pre_order(self):
        self._pre_order(self.root, '')


class DivisionTree(Tree):

    def __init__(self, train_datas, property_select_policy):
        super(DivisionTree, self).__init__()
        self._train_datas = train_datas
        rows = set(range(len(train_datas)))
        cols = set(range(len(train_datas[0]) - 1))
        self.root = self._build_tree(rows, cols, property_select_policy)

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

    def _build_tree(self, rows, cols, property_select_policy):
        # 训练集为空或者属性为空
        if not rows:
            return None
        y = self.get_col(-1, rows)
        if not cols:
            return TreeNode(None, None, self.vote(y), [])

        # 所有样本属于同一类
        if self._is_same(y):
            return TreeNode(None, None, y[0], [])

        properties = [(col, self.get_col(col, rows)) for col in cols]
        best_pro = property_select_policy(properties, y)
        root = TreeNode(best_pro, None, self.vote(y), [])

        if best_pro is None:
            return root
        cols.remove(best_pro)

        branches = dict()
        best_col = self.get_col(best_pro, rows)
        for x, row in zip(best_col, rows):
            branches.setdefault(x, set())
            branches[x].add(row)

        for branch, brc_rows in branches.items():
            child = self._build_tree(brc_rows, cols, property_select_policy)
            if child:
                child.condition = branch
                root.children.append(child)
        return root

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
        node = self.root
        path = []
        while node and node.property:
            path.append(node.property)
            condition = test_data[node.property]
            for child in node.children:
                if child.condition == condition:
                    node = child
                    break
            else:
                break
        return node.label, path
