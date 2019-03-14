# pylint: disable=assignment-from-no-return
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
            return self.copy()

    def norm(self):
        norm = np.linalg.norm(self)
        return norm

    def rotate2D(self, degree):
        """2D向量逆时针旋转degree度"""
        if self.dim != 2:
            raise Exception("Not 2D!")
        # 角度转为弧度
        radian = np.deg2rad(degree)
        c = np.cos(radian)
        s = np.sin(radian)
        a, b = self[0], self[1]
        x = a * c - b * s
        y = a * s + b * c
        return Vector([x, y])

    def angle(self, v):
        """同向量v之间的角度

        在向量为2D时行为会不同于AngleBetween, 这时angle方法会关注向量的顺序位置
        准确而言，这种情况下计算的是从self到v经过的角度, 返回值在[-180, 180]之间
        正数表示逆时针方向
        """
        degree = Vector.AngleBetween(self, v)
        if self.dim == 2:
            cross = np.cross(self, v)
            if cross < 0:
                degree = -degree
        return degree

    def __str__(self):
        s = []
        for ele in self:
            v = '{:.2f}'.format(ele)
            s.append(v)
        return '(' + ', '.join(s) + ')'

    def __mul__(self, v):
        """内积或普通乘法"""
        if isinstance(v, Vector):
            return Vector.InnerProd(self, v)
        else:
            return Vector(np.multiply(self, v))

    @staticmethod
    def InnerProd(v1, v2):
        res = np.multiply(v1, v2)
        return sum(res)

    @staticmethod
    def AngleBetween(v1, v2):
        """计算两个向量夹角, 返回单位为度, 返回值在[0, 180]之间"""
        cos = (v1 * v2) / (v1.norm() * v2.norm())
        # 由于计算精度的原因，可能存在cos = 1.000001之类的情况
        # 这会使得arccos无法正常运行
        if cos >= 1:
            cos = 1
        elif cos <= -1:
            cos = -1
        radian = np.arccos(cos)
        return np.rad2deg(radian)

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @x.setter
    def x(self, val):
        if not isinstance(val, float):
            if isinstance(val, int):
                val = float(val)
            else:
                raise Exception('Type Error')
        self[0] = val

    @y.setter
    def y(self, val):
        if not isinstance(val, float):
            if isinstance(val, int):
                val = float(val)
            else:
                raise Exception('Type Error')
        self[1] = val


def test():
    v = Vector([1, 5])
    u = Vector([2, 3])
    print(v * 3)
    print(v * u)


if __name__ == '__main__':
    test()
