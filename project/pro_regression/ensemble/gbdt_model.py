# coding=utf-8
# from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from decision_tree.decision_tree import RegressionTree
import numpy as np
import progressbar


# 暂时用sklearn的CART树做测试
# class RegressionTree(DecisionTreeRegressor):

#     def __init__(self, min_samples=2, min_impurity=1e-7,
#                  max_depth=float("inf")):
#         super(RegressionTree, self).__init__(max_depth=max_depth,
#                                              min_samples_split=min_samples,
#                                              min_impurity_decrease=min_impurity)


class GBDTRegressor:
    """ Uses a collection of CART models that trains on predicting the gradient
        of the loss function.

        Parameters:
        -----------
        # n_estimators: int
            至多使用的树的数量
            The number of regression trees that at most are used.
        learning_rate: float
            残差的学习率
            The shrinkage step length that will be taken to correct the residual error
        min_samples: int
            每棵子树的节点的最小数目（小于后不继续切割）
            The minimum number of samples needed to make a split when building a tree.
        min_impurity: float
            每颗子树的最小纯度（小于后不继续切割）
            The minimum impurity required to split the tree further.
        max_depth: int
            每颗子树的最大层数（大于后不继续切割）
            The maximum depth of a tree.
        loss_func:
            残差计算公式
            function to calculate residual error
        """

    def __init__(self, n_estimators=200, learning_rate=0.5, min_samples=2,
                 min_impurity=1e-5, max_depth=4, with_bar=True):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.min_samples = min_samples
        self.min_impurity = min_impurity
        self.max_depth = max_depth
        self.weighted_trees = []
        self.bar = None
        if with_bar:
            bar_widgets = [
                'Training: ', progressbar.Percentage(), ' ', 
                progressbar.Bar(marker="-", left="[", right="]"),
                ' ', progressbar.ETA()
            ]
            self.bar = progressbar.ProgressBar(widgets=bar_widgets)
    
    def get_params(self, deep=False):
        return {"n_estimators": self.n_estimators,
                "learning_rate": self.learning_rate,
                "min_samples": self.min_samples,
                "min_impurity": self.min_impurity,
                "max_depth": self.max_depth,
                }
    
    def set_params(self, **kargs):
        for k, v in kargs.items():
            self.__dict__[k] = v
        self.weighted_trees = []

    # with_bar 控制是否显示进度条
    def fit(self, X, y, with_bar=False):
        it_est = range(self.n_estimators)
        if self.bar is not None:
            it_est = self.bar(range(self.n_estimators))
        
        errors = []
        residual_error = y.copy()
        for i in range(self.n_estimators):
#             self.weighted_trees.append(RegressionTree(min_samples=self.min_samples,
#                                                       min_impurity=self.min_impurity,
#                                                       max_depth=self.max_depth))
            self.weighted_trees.append(LinearRegression())
            # GDBT模型每棵树训练的label实际上残差
            # 残差Ri = y - sum(y_predict_k), k=0,1,2,...,i-1
            errors.append(residual_error.copy())
            self.weighted_trees[-1].fit(X, residual_error)
            y_pred = self.weighted_trees[-1].predict(X)
            # 对于残差学习出来的结果，只累加一小部分（learning_rate）逐步逼近目标
            # 即每次只纠正一点点错误而不是一步纠正，有效避免过拟合
            residual_error -= self.learning_rate * y_pred
        return errors

    def predict(self, X):
        y_pred_res = np.zeros((X.shape[0], ))
        # 由于训练的时候只取训练结果的一小部分，预测的时候也要乘learning_rate
        for y_pred in map(lambda t: self.learning_rate * t.predict(X), self.weighted_trees):
            y_pred_res += y_pred
        return y_pred_res
