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
import random


class Vector:
    def __init__(self, *args):
        if hasattr(
            args[0],
            "__iter__",
        ):
            self._v = args[0][:]
        else:
            self._v = list(args)

    def __len__(self):
        return len(self._v)

    def __getitem__(self, index):
        return self._v[index]

    def __setitem__(self, index, value):
        self._v[index] = value

    def copy(self):
        v = Vector(self._v)
        return v

    def tuple(self):
        """Return the vector as a tuple"""
        return tuple(int(i) for i in self._v)

    def __iadd__(self, other):
        """In-place addition of Vector objects

        Args:
            Vector other
        Returns:
            new Vector
        Usage:
            my_vect_a += my_vect_b
        """
        try:
            if hasattr(other, "__getitem__"):
                if len(other) == len(self):
                    for i, j in enumerate(self):
                        self[i] += other[i]
                else:
                    raise TypeError("Length of vectors not the same.")
            else:
                for i, j in enumerate(self):
                    self[i] += other
        except:
            raise TypeError("Unable to add Vector objects %s and %s" % (repr(self), repr(other)))
        return self

    def __add__(self, other):
        """Addition of Vector objects

        Args:
            Vector other
        Returns:
            new Vector
        Usage:
            new_vect = my_vect_a + my_vect_b
        """
        vect = self.copy()
        vect += other
        return vect

    def __radd__(self, other):
        """Right-side addition of Vector objects

        Args:
            Vector other
        Returns:
            new Vector
        Usage:
            new_vect = my_vect_a + my_vect_b
        """
        return self + other

    def __isub__(self, other):
        """In-place subtraction of Vector objects

        Args:
            Vector other
        Returns:
            new Vector
        Usage:
            my_vect_a -= my_vect_b
        """

        try:
            self += other * -1
        except:
            raise TypeError(
                "Unable to subtract Vector objects %s and %s" % (repr(self), repr(other))
            )
        return self

    def __sub__(self, other):
        """Subtraction of Vector objects

        Args:
            Vector other
        Returns:
            new Vector
        Usage:
            new_vect = my_vect_a - my_vect_b
        """
        return self + (other * -1)

    def __rsub__(self, other):
        """Right-side subtraction of Vector objects

        Args:
            Vector other
        Returns:
            new Vector
        Usage:
            new_vect = my_vect_a - my_vect_b
        """
        return other + (self * -1)

    def __imul__(self, other):
        """In-place multiplication of Vector objects
        i.e. dot product, inner product

        Args:
            Vector other
        Returns:
            new Vector
        Usage:
            my_vect_a *= my_vect_b
        """

        try:
            if hasattr(other, "__getitem__"):
                if len(other) == len(self):
                    for i, j in enumerate(self):
                        self[i] *= other[i]
                else:
                    raise TypeError("Length of vectors not the same.")
            else:
                for i, j in enumerate(self):
                    self[i] *= other
        except:
            raise TypeError(
                "Unable to multiply Vector objects %s and %s" % (repr(self), repr(other))
            )
        return self

    def __mul__(self, other):
        """Multiplication of Vector objects

        Args:
            Vector other
        Returns:
            new Vector
        Usage:
            new_vect = my_vect_a * my_vect_b
        """
        vect = self.copy()
        vect *= other
        return vect

    def __rmul__(self, other):
        """Right-side multiplication of Vector objects

        Args:
            Vector other
        Returns:
            new Vector
        Usage:
            new_vect = my_vect_a * my_vect_b
        """
        return self * other

    def __idiv__(self, other):
        return self.__itruediv__(other)

    def __div__(self, other):
        return self.__truediv__(other)

    def __rdiv__(self, other):
        return self.__rtruediv__(other)

    def __itruediv__(self, other):
        """In-place true division of Vector objects

        Args:
            Vector other
        Returns:
            new Vector
        Usage:
            my_vect_a /= my_vect_b
        """

        try:
            if hasattr(other, "__getitem__"):
                if len(other) == len(self):
                    for i, j in enumerate(self):
                        self[i] /= other[i]
                else:
                    raise TypeError("Length of vectors not the same.")
            else:
                for i, j in enumerate(self):
                    self[i] /= other
        except ZeroDivisionError:
            raise ZeroDivisionError(
                "ZeroDivisionError when dividing Vector objects %s and %s"
                % (repr(self), repr(other))
            )
        except:
            raise TypeError("Unable to divide Vector objects %s and %s" % (repr(self), repr(other)))
        return self

    def __truediv__(self, other):
        """True divison of Vector objects

        Args:
            Vector other
        Returns:
            new Vector
        Usage:
            new_vect = my_vect_a * my_vect_b
        """
        vect = self.copy()
        vect /= other
        return vect

    def __rtruediv__(self, other):
        """Right-side true division of Vector objects

        Args:
            Vector other
        Returns:
            new Vector
        Usage:
            new_vect = unknown_object / my_vect_b
        """
        vect = self.copy()
        try:
            if hasattr(other, "__getitem__"):
                if len(other) == len(self):
                    for i, j in enumerate(self):
                        vect[i] = other[i] / self[i]
                else:
                    raise TypeError("Length of vectors not the same.")
            else:
                for i, j in enumerate(self):
                    vect[i] = other / self[i]
        except ZeroDivisionError:
            raise ZeroDivisionError("ZeroDivisionError when divising " + str(other) + " by " + self)
        except:
            raise TypeError("Unable to divide Vector objects %s and %s" % (repr(self), repr(other)))
        return vect

    def __eq__(self, other):
        """Elementwise equality of Vector objects

        Args:
            Vector other
        Returns:
            True if equal, False otherwise
        Usage:
            my_vect_a == my_vect_b
        """
        if len(self) != len(other):
            return False

        for i, k in zip(self, other):
            if i != k:
                return False

        return True

    def __neq__(self, other):
        """Elementwise inequality of Vector objects

        Args:
            Vector other
        Returns:
            False if equal, True otherwise
        Usage:
            my_vect_a != my_vect_b
        """
        return not self == other

    def __neg__(self):
        vect = self.copy()
        vect *= -1
        return vect

    def __str__(self):
        """Vector object string representation

        Returns:
            string
        Usage:
            str(my_vect)
        """
        return "[" + ", ".join(["%s" % i for i in self._v]) + "]"

    def __repr__(self):
        """Vector object string representation

        Returns:
            string
        Usage:
            str(my_vect)
        """
        return "Vector(" + str(self) + ")"

    def sum(self):
        """Sums the elements of a Vector object

        Returns:
            Scalar dot product
        Usage:
            len = my_vector.dot(other_vect)

        """
        return sum(self._v)

    def dot(self, other):
        """Calculates the dot product of the Vector

        Returns:
            Scalar dot product of vector
        Usage:
            len = my_vector.dot(other_vector)
        """
        return (self * other).sum()

    def length_sq(self):
        """Calculates the length of the Vector

        Returns:
            Length of vector
        Usage:
            len = my_vector.length_sqrt()
        """
        return self.dot(self)

    def length(self):
        """Calculates the length of the Vector

        Returns:
            Length of vector
        Usage:
            len = my_vector.length()
        """
        return (self.length_sq()) ** 0.5

    def normalize(self):
        """Normalizes the Vector object

        Usage:
            my_vect.normalize()
        """
        self /= self.length()
        return self

    def unit_vector(self):
        """Fetches a normalized Vector object version

        Usage:
            my_nomralized_vect = my_vect.normalize()
        """
        vect = self.copy()
        vect.normalize()
        return vect

    def random(self):
        vect = self.copy()
        vect._v = [random.uniform(-1, 1) for i in vect._v]
        vect.normalize()
        return vect


def main():
    a = Vector([5, 7])
    b = Vector([1, -4])
    print(a, b)
    a += b
    print(a)
    a *= -b
    c = a * b - b + a * 2 - 1
    print(a)
    a *= a
    print(a)


if __name__ == "__main__":
    main()
