# Copyright (c) 2013 Stian Lode
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
 
 
import math
from .vector import Vector

class Vector2d(Vector):
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

    def copy(self):
        v = Vector2d(self._v)
        return v

    def __repr__(self):
        """Vector2d object string representation

        Returns:
            string
        Usage:
            str(my_vect)
        """
        return "Vector2d(" + str(self) + ")"

    def perp(self):
        """Calculates the perpendicular vector

        Returns:
            The perpendicular Vector2d
        Usage:
            new_vect = my_vect.perp()
        """
        return Vector2d(-self.y, self.x)

    def cross(self, other):
        """Calculates the cross product between two vectors

        Scalar value corresponding to the z-axis value of the
        cross product in 3d

        Returns:
            The perpendicular Vector2d
        Usage:
            new_vect = my_vect.perp()
        """
        return self.x * other.y - other.x * self.y

    def angle(self):
        """Calculates the angle of a Vector2d object

        Args:
            A Vector2d object.
        Returns:
            Angle of vector in radians
        Usage:
            angle = my_vect.angle()
        """
        return math.atan2(self.y, self.x)

    def angle_diff(self, other):
        """Calculates the angle between Vector2d objects

        Args:
            A Vector2d object.
        Returns:
            Angle between two vectors in radians
        Usage:
            angle = my_vect.angle(other_vect)
        """
        return math.atan2(other[1], other[0]) - math.atan2(self.y, self.x)

    def rotate(self, angle):
        """Return a new Vector2d rotated by argument angle.

        Args:
            An angle in radians.
        Returns:
            A new Vector2d object.
        Usage:
            new_vect = my_vect.rotate(angle)
        """
        cs = math.cos(angle)
        sn = math.sin(angle)
        rx = self.x*cs - self.y*sn
        ry = self.x*sn + self.y*cs
        return Vector2d(rx, ry)

def main():
    a = Vector2d(5,7)
    b = Vector2d(1, -4)
    print(a, b)
    a+=b
    print(a)
    a-=b
    print(a)
    c = b.cross(a)
    print(c)
    d = a*b-b+a*2-1
    print(d)

if __name__ == '__main__':
    main()
