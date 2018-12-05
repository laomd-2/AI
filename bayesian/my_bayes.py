from pomegranate import *


def auto_complete(probability_table):
    for i in range(len(probability_table)):
        v = probability_table[i].copy()
        v[-2] = '-' + v[-2]
        v[-1] = 1.0 - v[-1]
        probability_table.append(v)
    return probability_table


def last_index(l, v):
    for i, vv in enumerate(reversed(l)):
        if vv == v:
            return -i - 1
    raise ValueError(str(v) + " not found")


class MyBayesianNetwork(BayesianNetwork):
    
    def probability(self, *args, **kargs):
        try:
            values = list(args[0])
            i = last_index(values, None)
            p = 0
            for v in self.states[i].distribution.keys():
                values[i] = v
                p += self.probability(values, *args[1:], **kargs)
            return p
        except ValueError:
            return super(BayesianNetwork, self).probability(*args, **kargs)
        