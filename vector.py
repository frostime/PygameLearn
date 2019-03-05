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

    def rotate2D(self, theta):
        """2D向量逆时针旋转theta度"""
        if self.dim != 2:
            raise Exception("Not 2D!")
        # 角度转为弧度
        theta = (theta * np.pi) / 180
        c = np.cos(theta)
        s = np.sin(theta)
        a, b = self[0], self[1]
        x = a * c - b * s
        y = a * s + b * c
        return Vector([x, y])

    def angle(self, v):
        """同向量v之间的角度"""
        return Vector.AngleBetween(self, v)

    def __str__(self):
        s = []
        for ele in self:
            v = '{:.2f}'.format(ele)
            s.append(v)
        return '(' + ', '.join(s) + ')'

    def __mul__(self, v):
        """内积"""
        return Vector.InnerProd(self, v)

    @staticmethod
    def InnerProd(v1, v2):
        res = np.multiply(v1, v2)
        return sum(res)

    @staticmethod
    def AngleBetween(v1, v2):
        """计算两个向量夹角, 返回单位为度"""
        cos = (v1 * v2) / (v1.norm() * v2.norm())
        return np.arccos(cos) * 180 / np.pi
