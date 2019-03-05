"""
向量类
"""
import numpy as np


class Vector(np.ndarray):
    def __new__(cls, input_array):
        obj = np.asarray(input_array, dtype=float).view(cls)
        obj.dim = len(input_array)
        return obj

    def normalize(self):
        norm = self.norm()
        if norm != 0:
            return self / norm
        else:
            return norm.copy()

    def norm(self):
        norm = np.linalg.norm(self)
        return norm

    def __str__(self):
        s = []
        for ele in self:
            v = '{:.2f}'.format(ele)
            s.append(v)
        return '(' + ', '.join(s) + ')'
