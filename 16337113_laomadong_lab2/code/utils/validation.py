from sklearn.metrics import r2_score, mean_squared_error
from utils import train_test_split
import numpy as np


def validate(model, x_train, y_train, shuffle=True):
    X_train, X_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.2, shuffle=shuffle)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # mse = mean_squared_error(y_test, y_pred)
    acc = (y_test == y_pred).astype(float).sum() / y_test.size
    # corr = np.corrcoef(y_test, y_pred)[0, 1]
    return acc