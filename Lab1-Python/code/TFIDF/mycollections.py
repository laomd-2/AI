import collections


class NumberOrderedDict(collections.OrderedDict):
    def __getitem__(self, k):
        try:
            return super().__getitem__(k)
        except KeyError:
            return 0

    def __setitem__(self, k, v):
        if not isinstance(v, int) and not isinstance(v, float):
            raise TypeError("value type should be int or float")
        super().__setitem__(k, v)
