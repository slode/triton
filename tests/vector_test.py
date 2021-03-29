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
 
 
import unittest, math
from triton.vector import Vector
from triton.vector3d import Vector3d
from triton.vector2d import Vector2d

class TestVector2dFunctions(unittest.TestCase):

    def test_addition(self):
        a = Vector2d(3,0)
        b = Vector2d(0,2)
        c = a + b
        self.assertEqual(c, [3,2])
        a += b
        self.assertEqual(a,c)
        d = 1 + a
        self.assertEqual(d, [a.x+1, a.y+1])

    def test_subtraction(self):
        a = Vector2d(3,0)
        b = Vector2d(0,2)
        c = a - b
        self.assertEqual(c, [3,-2])
        a -= b
        self.assertEqual(a,c)
        d = 1 - a
        self.assertEqual(d, [1 - a.x, 1 - a.y])

    def test_multiplication(self):
        a = Vector2d(3,1)
        b = Vector2d(1,2)
        c = a * b
        self.assertEqual(c, [3,2])
        a *= b
        self.assertEqual(a,c)
        d = -1 * a
        self.assertEqual(d, [-1 * a.x, -1 * a.y])

    def test_division(self):
        a = Vector2d(3.0,1.0)
        b = Vector2d(1.0,2.0)
        c = a / b
        self.assertEqual(c, [3, 0.5])
        a /= b
        self.assertEqual(a,c)
        d = 1 / a
        self.assertEqual(d, [1 / a.x, 1 / a.y])

    def  test_length(self):
        a = Vector2d(3,0)
        b = Vector2d(0,4)
        self.assertAlmostEqual((a-b).length(), 5)

    def test_perp(self):
        a = Vector2d(1,9)
        b = a.perp()
        self.assertEqual(b, [-9, 1])
        c = a.dot(b)
        self.assertEqual(c, 0 )

    def test_eq(self):
        a = Vector2d(3,2)
        b = Vector2d(3,2)
        self.assertEqual(a,b)
        self.assertEqual(a,[3,2])
        self.assertNotEqual(a,[2,3])

    def test_normalize(self):
        a = Vector2d(5,2);
        a.normalize()
        self.assertEqual(a.length(), 1)

    def test_angle(self):
        a = Vector2d(4,4)
        b = Vector2d(4,-4)
        c = b.angle_diff(a)
        self.assertAlmostEqual(c, math.pi/2)
        d = b.angle_diff(b)
        self.assertAlmostEqual(d, 0)
        e = Vector2d(-4, -4)
        f = e.angle_diff(a)
        self.assertAlmostEqual(f, math.pi)
        g = a.angle_diff(e)
        self.assertAlmostEqual(g, -math.pi)

        h = a.angle()
        self.assertAlmostEqual(h, math.pi/4)

    def test_normalize(self):
        a = Vector2d(8,9)
        b = a.unit_vector()
        self.assertAlmostEqual(b.length(), 1)
        a.normalize()
        self.assertAlmostEqual(a.length(), 1)

    def test_cross(self):
        a = Vector3d(-0, 10, 0)
        b = Vector3d(10, 0, 0)
        c = b.cross(a)
        self.assertEqual(c, [0, 0, 100])
        d = a.cross(b)
        self.assertEqual(d, [0, 0, -100])

        a = Vector2d(-0, 10)
        b = Vector2d(10, 0)
        c = b.cross(a)
        self.assertEqual(c, 100)



if __name__ == '__main__':
    unittest.main()
