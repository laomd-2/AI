import math
import collections


class IDF:

    def __init__(self, documents, sep=' '):
        self._idf = collections.OrderedDict()
        for i, document in enumerate(documents):
            for word in self._to_words(document, sep):
                self._idf.setdefault(word, set())
                self._idf[word].add(i)
        i += 1
        for word, exists in self._idf.items():
            self._idf[word] = math.log(i / (1 + len(exists)))

    @staticmethod
    def _to_words(document, sep):
        return document.split(sep)

    def get_tf_idf(self, document, sep=' '):
        counter = collections.Counter()
        words = self._to_words(document, sep)
        for word in words:
            counter[word] += 1
        total = len(words)
        for word in counter:
            if word in self._idf:
                counter[word] = counter[word] / total * self._idf[word]
            else:
                counter[word] = 0.000001
        return counter

    @property
    def words(self):
        return self._idf.keys()
