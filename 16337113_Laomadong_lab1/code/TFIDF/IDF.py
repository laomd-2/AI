import math
import collections


class IDF:

    def __init__(self, documents, sep=' '):
        # 按出现顺序存储每个单词的idf值，以便在对应tf矩阵每个元素
        self._idf = collections.OrderedDict()
        for i, document in enumerate(documents):
            for word in self._to_words(document, sep):
                # 存储每个单词所出现的文本的集合（不重复）
                self._idf.setdefault(word, set())
                self._idf[word].add(i)
        i += 1
        # idf计算公式
        for word, exists in self._idf.items():
            self._idf[word] = math.log(i / (1 + len(exists)))

    @staticmethod
    def _to_words(document, sep):
        return document.split(sep)

    def get_tf_idf(self, document, sep=' '):
        counter = collections.Counter()
        words = self._to_words(document, sep)
        # 统计每个单词在document文本中出现的次数
        for word in words:
            counter[word] += 1
        total = len(words)
        # tf-idf计算公式
        for word in counter:
            if word in self._idf:
                counter[word] = counter[word] / total * self._idf[word]
            else:
                # 用0.000001是防止出现零向量（余弦距离不支持）
                counter[word] = 0.000001
        return counter

    @property
    def words(self):
        return self._idf.keys()
