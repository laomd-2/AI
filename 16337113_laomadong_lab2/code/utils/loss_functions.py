from __future__ import division
import numpy as np
from utils import accuracy_score


class Loss(object):

    def loss(self, y_true, y_pred):
        return NotImplementedError()


class MemorylessLoss(Loss):

    def loss(self, y_true, y_pred):
        return y_true - y_pred


class MemoryFulLoss(MemorylessLoss):

    def __init__(self, review_rate=0.01):
        super(MemoryFulLoss, self).__init__()
        self._last_loss = None
        self._review_rate = review_rate

    def loss(self, y_true, y_pred):
        cur_loss = super(MemoryFulLoss, self).loss(y_true, y_pred)
        if self._last_loss is not None:
            cur_loss = self._review_rate * self._last_loss \
                    + (1 - self._review_rate) * cur_loss
        self._last_loss = cur_loss
        return cur_loss
