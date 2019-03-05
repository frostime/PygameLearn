"""
向量类
"""
import numpy as np


class Vector(np.ndarray):
    def __new__(cls, input_array):
        obj = np.asarray(input_array, dtype=float).view(cls)
        obj.dim = len(input_array)
        if obj.dim <= 3:
            obj.x = input_array[0]
            obj.y = input_array[1]
            if obj.dim == 3:
                obj.z = input_array[2]
        return obj

    def normalize(self):
        norm = self.norm()
        return self / norm

    def norm(self):
        norm = np.linalg.norm(self)
        return norm
