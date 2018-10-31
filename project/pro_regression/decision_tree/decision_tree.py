# coding=utf-8
import numpy as np
from time import time

class DecisionNode():
    """
    决策树的节点
    Parameters:
    -----------
    feature_i: int
        节点分支使用的特征
        Feature index which we want to use as the threshold measure.
    threshold: float
        分支阈值
        The value that we will compare feature values at feature_i against to
        determine the prediction.
    value: float
        叶子节点预测值
        The class prediction if classification tree, or float value if regression tree.
    left_branch: DecisionNode
        左子树
        Next decision node for samples where features value met the threshold. (>= threshold)
    right_branch: DecisionNode
        右子树
        Next decision node for samples where features value did not meet the threshold.(< threshold)
    """

    def __init__(self, feature_i=None, threshold=None,
                 value=None, left_branch=None, right_branch=None):
        self.feature_i = feature_i
        self.threshold = threshold
        self.value = value
        self.left_branch = left_branch
        self.right_branch = right_branch


class RegressionTree():
    """
    Parameters:
        min_samples: int
            节点的样本数小于此值时终止建树
            The minimum number of samples needed to make a split when building a tree.
        min_impurity: float
            节点不纯度小于此值时终止建树, (impurity = var(y))
            The minimum impurity required to split the tree further.
        max_depth: int
            树的深度大于此值时终止建树
            The maximum depth of a tree.
    """

    def __init__(self, min_samples=2, min_impurity=1e-7,
                 max_depth=np.inf):
        self.root = None  # Root node in decision tree

        self.min_samples = min_samples
        self.min_impurity = min_impurity
        self.max_depth = max_depth


    def fit(self, X, y, feature_use=[0]):
        """ 
        Build decision tree 
        X: dataset
        y: label
        feature_use: list, 选择用于预测的标签, fu[0]=0: 按GBDT进行;  fu[0]=1, 按随机森林进行
        """       
        if feature_use[0] == 0:
            self.root = self._build_tree(X, y)
        else:
            self.root = self._build_tree(X,y,feature_use=feature_use[1:])


    def divide_on_feature(self, X, feature_i, threshold):
        """ Divide dataset based on if sample value on feature index is larger than
            the given threshold """
        X = np.asarray(X)

        # split_func = None
        # if isinstance(threshold, int) or isinstance(threshold, float):
        split_func = lambda sample: sample >= threshold
        # else:
        #     split_func = lambda sample: sample == threshold

        # split_func_vec = np.vectorize(split_func)

        # 已经做了并行化处理，不过多数时间还是花在这个操作
        #indexs = split_func_vec(X[:,feature_i])  
        indexs = split_func(X[:,feature_i])
        X_1 = X[indexs]
        X_2 = X[~indexs]
        return np.array([X_1, X_2])


    def _build_tree(self, X, y, current_depth=0,feature_use=[0]):
        """
            Recursive method which builds out the decision tree and splits X and respective y
            on the feature of X which (based on impurity) best separates the data
            X: [[],[],..],  (size: n_samples * n_features)
            y: [],  (size: n_samples)
        """
        largest_impurity = -np.inf
        best_criteria = None  # Feature index and threshold
        best_sets = None      # Subsets of the dataSplit

        # calc:  var(y) - (p1*var(y1)+p2*var(y2))
        #      = ((yi-ymean)^2 - (y1i - y1mean)^2 - (y2i - y2mean)^2) / len(y)
        n = len(y)
        y_squareSum = np.sum((y-np.mean(y))**2)

        # 将X和y合并
        y = np.expand_dims(y, axis=1)  
        Xy = np.concatenate((X, y), axis=1)

        #判断是否要终止建树, 然后找出最佳特征划分数据
        n_samples, n_features = np.shape(X)

        # 当样本数目大于节点最小样本数，或树的深度还不够时，继续计算不纯度
        if n_samples >= self.min_samples and current_depth <= self.max_depth:

            # feature_use只有一个特征时，选择GBDT, 否则选用随机森林，取feature_use的特征集
            features = range(n_features)
            if len(feature_use)>1:
                features = feature_use

            for feature_i in features:
                # 取出数据集中相应特征的所有取值
                feature_values = np.expand_dims(X[:, feature_i], axis=1)

                # 连续特征离散化处理，大幅度减少时间开销
                feature_values.sort()

                k = 5
                sz = len(feature_values)
                sample_features_values = []
                for i in range(1,k):
                    sample_features_values.append(feature_values[int(i*sz/k)])
                unique_values = np.unique(sample_features_values)

                if len(unique_values)==2:  # 只有两个值，那么用一个较大值划分即可（划分函数为大于等于），对于tag特征可以加速很多
                    unique_values = unique_values[-1:] 
                elif len(unique_values)==1:  # 只有一个值，那么无需划分
                    continue

                # 对特征feature_i的每个值计算不纯度       
                for threshold in unique_values:
                    # Divide X and y depending on if the feature value of X at index feature_i
                    # meets the threshold
                    #tstart = time()
                    Xy1, Xy2 = self.divide_on_feature(Xy, feature_i, threshold)
                    #self.f_t += time() - tstart

                    if len(Xy1) > 0 and len(Xy2) > 0:
                        y1 = Xy1[:, -1]
                        y2 = Xy2[:, -1]                        

                        # 计算不纯度\信息增益
                        impurity = (y_squareSum - np.sum((y1-np.mean(y1))**2) - np.sum((y2-np.mean(y2))**2))/n

                        # If this threshold resulted in a higher information gain than previously
                        # recorded save the threshold value and the feature
                        # index
                        if impurity > largest_impurity:
                            largest_impurity = impurity
                            best_criteria = {"feature_i": feature_i, "threshold": threshold}
                            best_sets = {
                                "leftX": Xy1[:, :n_features],  # X of left subtree
                                "lefty": Xy1[:, -1],  # y of left subtree
                                "rightX": Xy2[:, :n_features],  # X of right subtree
                                "righty": Xy2[:, -1]  # y of right subtree
                            }

        # 当当前节点信息增益很小时就退出，设置子节点
        if largest_impurity > self.min_impurity:
            left_branch = self._build_tree(best_sets["leftX"], best_sets["lefty"], current_depth + 1)
            right_branch = self._build_tree(best_sets["rightX"], best_sets["righty"], current_depth + 1)
            return DecisionNode(feature_i=best_criteria["feature_i"], threshold=best_criteria[
                "threshold"], left_branch=left_branch, right_branch=right_branch)

        return DecisionNode(value=np.mean(y))


    def predict_value(self, x, tree=None):
        """ Do a recursive search down the tree and make a prediction of the data sample by the
            value of the leaf that we end up at """

        if tree is None:
            tree = self.root

        # If we have a value (i.e we're at a leaf) => return value as the prediction
        if tree.value is not None:
            return tree.value

        # Choose the feature that we will test
        feature_value = x[tree.feature_i]

        # Determine if we will follow left or right branch
        branch = tree.right_branch
        if isinstance(feature_value, int) or isinstance(feature_value, float):
            if feature_value >= tree.threshold:
                branch = tree.left_branch
        elif feature_value == tree.threshold:
            branch = tree.left_branch
            
        return self.predict_value(x, branch)

    def predict(self, X):
        """ Classify samples one by one and return the set of labels """
        return np.asarray([self.predict_value(x) for x in X])


# class DecisionTree(object):
#     """
#     Parameters:
#         min_samples: int
#             节点的样本数小于此值时终止建树
#             The minimum number of samples needed to make a split when building a tree.
#         min_impurity: float
#             节点纯度小于此值时终止建树, (impurity = var(y))
#             The minimum impurity required to split the tree further.
#         max_depth: int
#             树的深度大于此值时终止建树
#             The maximum depth of a tree.
#     """

#     def __init__(self, min_samples=2, min_impurity=1e-7,
#                  max_depth=np.inf):
#         self.root = None  # Root node in decision tree

#         self.min_samples = min_samples
#         self.min_impurity = min_impurity
#         self.max_depth = max_depth

#         # Function to calculate impurity (regressinon=>variance reduct.)
#         self._impurity_calculation = None
#         # Function to determine prediction of y at leaf(确定y的预测值))
#         #回归树：取所有值的平均值
#         self._leaf_value_calculation = None

#     def fit(self, X, y):
#         """ Build decision tree """
#         self.root = self._build_tree(X, y)

#     # hjhj
#     def divide_on_feature(self, X, feature_i, threshold):
#         """ Divide dataset based on if sample value on feature index is larger than
#             the given threshold """
#         X = np.asarray(X)

#         split_func = None
#         if isinstance(threshold, int) or isinstance(threshold, float):
#             split_func = lambda sample: sample >= threshold
#         else:
#             split_func = lambda sample: sample == threshold

#         split_func_vec = np.vectorize(split_func)

#         indexs = split_func_vec(X[:,feature_i])  # 已经做了并行化处理，不过多数时间还是花在这个操作

#         X_1 = X[indexs]
#         X_2 = X[~indexs]
#         return np.array([X_1, X_2])


#     def _build_tree(self, X, y, current_depth=0):
#         """
#             Recursive method which builds out the decision tree and splits X and respective y
#             on the feature of X which (based on impurity) best separates the data
#             X: [[],[],..],  (size: n_samples * n_features)
#             y: [],  (size: n_samples)
#         """
#         largest_impurity = -np.inf
#         best_criteria = None  # Feature index and threshold
#         best_sets = None      # Subsets of the dataSplit


#         # hjhj，先计算y的方差，减小时间复杂度
#         # calc: var(y) - (p1*var(y1)+p2*var(y2))
#         #      =((yi-ymean)^2 - (y1i - y1mean)^2 - (y2i - y2mean)^2) / len(y)
#         #val_y = np.var(y)
#         n = len(y)
#         y_squareSum = np.sum((y-np.mean(y))**2)

#         # Add y as last column of X
#         y = np.expand_dims(y, axis=1)  
#         Xy = np.concatenate((X, y), axis=1)


#         #判断是否要终止建树, 然后找出最佳特征划分数据
#         n_samples, n_features = np.shape(X)

#         # 当样本数目大于节点最小样本数，或树的深度还不够时，继续计算不纯度
#         if n_samples >= self.min_samples and current_depth <= self.max_depth:
#             for feature_i in range(n_features):
#                 # 取出数据集中相应特征的所有取值
#                 feature_values = np.expand_dims(X[:, feature_i], axis=1)

#                 # 连续特征离散化处理，大幅度减少时间开销
#                 feature_values.sort()
#                 k = 5
#                 sz = len(feature_values)
#                 sample_features_values = []
#                 for i in range(1,k):
#                     sample_features_values.append(feature_values[int(i*sz/k)])
#                 unique_values = np.unique(sample_features_values)

#                 # hjhj
#                 if len(unique_values)==2:  # 只有两个值，那么用一个较大值划分即可（划分函数为大于等于），对于tag特征可以加速很多
#                     unique_values = unique_values[-1:] 
#                 elif len(unique_values)==1:  # 只有一个值，那么无需划分
#                     continue

#                 # unique_values = np.unique(feature_values)

#                 # Iterate through all unique values of feature column i and
#                 # calculate the impurity
                
#                 for threshold in unique_values:
#                     # Divide X and y depending on if the feature value of X at index feature_i
#                     # meets the threshold

#                     # start = time()
#                     Xy1, Xy2 = self.divide_on_feature(Xy, feature_i, threshold)
#                     # self.f_t += time()-start


#                     if len(Xy1) > 0 and len(Xy2) > 0:
#                         # Select the y-values of the two sets
#                         # y1 = Xy1[:, n_features:]
#                         # y2 = Xy2[:, n_features:]

#                         # hjhj，变成一个行向量，而不是一个列矩阵。。
#                         y1 = Xy1[:, -1]
#                         y2 = Xy2[:, -1]                        


#                         # Calculate impurity
#                         #impurity = self._impurity_calculation(y1, y2, val_y, n)
#                         impurity = (y_squareSum - np.sum((y1-np.mean(y1))**2) - np.sum((y2-np.mean(y2))**2))/n

#                         # If this threshold resulted in a higher information gain than previously
#                         # recorded save the threshold value and the feature
#                         # index
#                         if impurity > largest_impurity:
#                             largest_impurity = impurity
#                             best_criteria = {"feature_i": feature_i, "threshold": threshold}
#                             best_sets = {
#                                 "leftX": Xy1[:, :n_features],  # X of left subtree
#                                 "lefty": Xy1[:, -1],  # y of left subtree
#                                 "rightX": Xy2[:, :n_features],  # X of right subtree
#                                 "righty": Xy2[:, -1]  # y of right subtree
#                             }

#         # 当节点不纯度不够小时，继续分类
#         if largest_impurity > self.min_impurity:
#             left_branch = self._build_tree(best_sets["leftX"], best_sets["lefty"], current_depth + 1)
#             right_branch = self._build_tree(best_sets["rightX"], best_sets["righty"], current_depth + 1)
#             return DecisionNode(feature_i=best_criteria["feature_i"], threshold=best_criteria[
#                 "threshold"], left_branch=left_branch, right_branch=right_branch)

#         # 计算叶子节点值
#         #leaf_value = self._leaf_value_calculation(y)
#         #return DecisionNode(value=leaf_value)
#         return DecisionNode(value=np.mean(y))

#     def predict_value(self, x, tree=None):
#         """ Do a recursive search down the tree and make a prediction of the data sample by the
#             value of the leaf that we end up at """

#         if tree is None:
#             tree = self.root

#         # If we have a value (i.e we're at a leaf) => return value as the prediction
#         if tree.value is not None:
#             return tree.value

#         # Choose the feature that we will test
#         feature_value = x[tree.feature_i]

#         # Determine if we will follow left or right branch
#         branch = tree.right_branch
#         if isinstance(feature_value, int) or isinstance(feature_value, float):
#             if feature_value >= tree.threshold:
#                 branch = tree.left_branch
#         elif feature_value == tree.threshold:
#             branch = tree.left_branch
            
#         return self.predict_value(x, branch)

#     def predict(self, X):
#         """ Classify samples one by one and return the set of labels """
#         return np.asarray([self.predict_value(x) for x in X])

#     def print_tree(self, tree=None, indent=" "):
#         """ Recursively print the decision tree """
#         if not tree:
#             tree = self.root

#         # If we're at leaf => print the label
#         if tree.value is not None:
#             print(tree.value)
#         # Go deeper down the tree
#         else:
#             # Print test
#             print("%s:%s? " % (tree.feature_i, tree.threshold))
#             # Print the true scenario
#             print("%sT->" % (indent), end="")
#             self.print_tree(tree.left_branch, indent + indent)
#             # Print the false scenario
#             print("%sF->" % (indent), end="")
#             self.print_tree(tree.right_branch, indent + indent)



# # def calculate_variance(X):
# #     """ Return the variance of the features in dataset X """
# #     mean = np.ones(np.shape(X)) * X.mean(0)
# #     n_samples = np.shape(X)[0]
# #     variance = (1 / n_samples) * np.diag((X - mean).T.dot(X - mean))
    
# #     return variance


# class RegressionTree(DecisionTree):
#     # hjhj
#     def _calculate_variance_reduction(self, y1, y2, val_y, n):
#         '''计算纯度变化'''
#         # var_tot = calculate_variance(y)
#         # var_1 = calculate_variance(y1)
#         # var_2 = calculate_variance(y2)
#         frac_1 = len(y1) / n
#         frac_2 = len(y2) / n

#         # # Calculate the variance reduction
#         # variance_reduction = var_tot - (frac_1 * var_1 + frac_2 * var_2)

#         # return sum(variance_reduction)

#         # 直接这样不就ok了。。。
#         return val_y-(np.var(y1)*frac_1 + np.var(y2)*frac_2)


#     def _mean_of_y(self, y):
#         return np.mean(y)

#     def fit(self, X, y):
#         self._impurity_calculation = self._calculate_variance_reduction
#         self._leaf_value_calculation = self._mean_of_y
#         # self.f_t = 0
#         super(RegressionTree, self).fit(X, y)
