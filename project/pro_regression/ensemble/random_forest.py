from decision_tree.decision_tree import RegressionTree
import numpy as np
import progressbar


class RandomForest:
    
    def __init__(self, n_estimators=100, max_depth=7, feat_size=9):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.feat_size = feat_size
        self.model_gather = []
        bar_widgets = [
            'Training: ', progressbar.Percentage(), ' ', progressbar.Bar(marker="-", left="[", right="]"),
            ' ', progressbar.ETA()
        ]
        self.bar = progressbar.ProgressBar(widgets=bar_widgets)
    
    def get_params(self, deep=False):
        return {
            "n_estimators": self.n_estimators,
            "max_depth": self.max_depth,
            "feat_size": self.feat_size
        }
    
    def fit(self, X, y, **kargs):
        n_samples, n_features = np.shape(X)

        #随机生成多棵树
        for _treeCnt in self.bar(range(self.n_estimators)):
            #有放回抽样数据集
            slicex = np.array(range(n_samples))
            slicex = np.random.choice(slicex,size=n_samples,replace = True)
            _X = X[slicex,:]
            _y = y[slicex]
            #抽样特征
            feature_use = np.random.choice(range(0,n_features),replace=False,size = self.feat_size)
            feature_use = np.concatenate(([1],feature_use))
            model = RegressionTree(max_depth=self.max_depth)
            model.fit(_X, _y,feature_use)
            self.model_gather.append(model)    #将多个决策树加到model_gather中
    
    def predict(self, X):
        #存放所有预测的值，最后取平均值
        y_pred = np.zeros(X.shape[0])
        for model in self.model_gather:
            y_pred = model.predict(X) + y_pred #直接进行验证
        return y_pred/self.n_estimators    #多棵决策树进行预测