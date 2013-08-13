#-------------------------------------------------------------------------------
# Name:        Vector3d
# Purpose:
#
# Author:      Stian Lode
#
# Created:     01.09.2012
# Copyright:   (c) Stian Lode 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import math
from triton.vector import Vector

class Vector3d(Vector):
    @property
    def x(self):
        return self._v[0]

    @x.setter
    def x(self, x):
        self._v[0] = x

    @property
    def y(self):
        return self._v[1]

    @y.setter
    def y(self, y):
        self._v[1] = y

    @property
    def z(self):
        return self._v[2]

    @z.setter
    def z(self, z):
        self._v[2] = z

    def copy(self):
        v = Vector3d(self._v)
        return v

    def __repr__(self):
        """Vector object string representation

        Returns:
            string
        Usage:
            str(my_vect)
        """
        return "Vector3d(" + str(self) + ")"

    def cross(self, other):
        """Calculates the cross product

        Args:
            Vector3d
        Returns:
            The perpendicular Vector3d
        Usage:
            new_vect = my_vect.perp()
        """
        return Vector3d(
            [self.y * other.z - other.y * self.z,
            self.z * other.x - other.z * self.x,
            self.x * other.y - other.x * self.y])

def main():
    a = Vector3d([5, 5, 0])
    b = Vector3d([5, -5, 0])
    print(a, b)
    c = b.cross(a)
    print c
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot([0, a.x], [0, a.y], zs=[0, a.z])
    ax.plot([0, b.x], [0, b.y], zs=[0, b.z])
    ax.plot([0, c.x], [0, c.y], zs=[0, c.z])
    plt.show()

if __name__ == '__main__':
    main()