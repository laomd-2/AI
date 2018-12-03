class Point(tuple):

    @staticmethod
    def __new__(cls, *args):
        return super(Point, cls).__new__(cls, *args)

    def __add__(self, other):
        return self.__new__(Point, (a + b for a, b in zip(self, other)))

    def __radd__(self, other):
        return self + other