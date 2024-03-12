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

try:
    from triton.vector2d import Vector2d
except:
    from vector2d import Vector2d


def intersect_circle_line(cc, cr, l1, l2):
    line = l2 - l1
    c2l = l1 - cc

    a = line.dot(line)
    b = 2 * c2l.dot(line)
    c = c2l.dot(c2l) - cr * cr

    disc = b * b - 4 * a * c

    if disc < 0:
        return False
    else:
        disc = math.sqrt(disc)

        t1 = (-b - disc) / (2 * a)
        t2 = (-b + disc) / (2 * a)
        
        if 0 <= t1 <= 1:
            return True
        if 0 <= t2 <= 1:
            return True
    return False



def bounding_box(polygon):
    p1 = polygon[0]
    x_min = p1.x
    x_max = p1.x
    y_min = p1.y
    y_max = p1.y

    for p in polygon[1:]:
        if p.x < x_min:
            x_min = p.x
        elif p.x > x_max:
            x_max = p.x
        if p.y < y_min:
            y_min = p.y
        elif p.y > y_max:
            y_max = p.y
    return (x_min, x_max, y_min, y_max)

def point_outside_box(point, box):
    if (box[0] > point.x or box[1] < point.x
        or box[2] > point.y or box[3] < point.y):
        return True
    return False

def min_distance_point_line(p, l1, l2):
    """Calculates shortest distance from a point p to a line given by the
    points l1 and l2.
    """
    u_nom = ((p.x - l1.x) * (l2.x - l1.x) + (p.y - l1.y) * (l2.y - l1.y))
    u_den = (l2 - l1).length_sq()

    if u_den == 0:
        return (l1, 0.0)

    u = u_nom / u_den

    x = l1.x + u * (l2.x - l1.x)
    y = l1.y + u * (l2.y - l1.y)
    
    closest_point = Vector2d(x, y)
    return (closest_point, u)

def inside_polygon(p, polygon):
    counter = 0
    length = len(polygon) 
    p1 = polygon[0]
    for i in range(1, length):
        p2 = polygon[i % length]
        if p.y > min(p1.y, p2.y):
            if p.y <= max(p1.y, p2.y):
                if p.x <= max(p1.x, p2.x):
                    if p1.y != p2.y:
                        x_inters = (p.y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x
                        if p1.x == p2.x or x_inters:
                            counter += 1
    if counter % 2 == 0:
        return False
    return True

def intersection_line_line(k1, k2, l1, l2):
    """Finds the intersection between two lines, each of which is given by two
    points"""
    ua_nom = (k2.x - k1.x) * (l1.y - k1.y) - (k2.y - k1.y) * (l1.x - k1.x)

    ub_nom = (l2.x - l1.x) * (l1.y - k1.y) - (l2.y - l1.y) * (l1.x - k1.x)

    u_den  = (k2.y - k1.y) * (l2.x - l1.x) - (k2.x - k1.x) * (l2.y - l1.y)

    # parallel lines.
    if u_den == 0.0:
        # coincident
        if ua_nom == 0.0:
            return (k1, 0.0, 0.0)
        return ValueError("Lines are parallel and does not intersect.")

    u1 = ua_nom / u_den
    u2 = ua_nom / u_den
    
    x = l1.x + u1 * (l2.x - l1.x)
    y = l1.y + u1 * (l2.y - l1.y)

    intersection_point = Vector2d(x, y)
    return (intersection_point, u1, u2) 

if __name__ == '__main__':
    import unittest

    class TestGeometry(unittest.TestCase):
        def test_intersect_circle_line(self):
            circle_center = Vector2d(25.0, 0.0)
            circle_radius = 10.0
            line_start = Vector2d(0.0, 0.0)
            line_end = Vector2d(50.0, 0.0)
            xsect = intersect_circle_line(
                circle_center, circle_radius, line_start, line_end)

            self.assertTrue(xsect)


        def test_inside_polygon(self):
            polygon = []
            polygon.append(Vector2d(0.0, 0.0))
            polygon.append(Vector2d(10.0, 0.0))
            polygon.append(Vector2d(10.0, 10.0))
            polygon.append(Vector2d(0.0, 10.0))

            point_inside = Vector2d(5.0, 5.0)
            point_outside = Vector2d(15.0, 15.0)
            point_on_edge = Vector2d(10.0, 10.0)

            self.assertTrue(inside_polygon(point_inside, polygon))
            self.assertFalse(inside_polygon(point_outside, polygon))
            self.assertTrue(inside_polygon(point_on_edge, polygon))

        def test_outside_box(self):
            polygon = []
            polygon.append(Vector2d(0.0, 0.0))
            polygon.append(Vector2d(10.0, 0.0))
            polygon.append(Vector2d(20.0, 10.0))
            polygon.append(Vector2d(10.0, 10.0))
            polygon.append(Vector2d(0.0, 10.0))

            point_inside = Vector2d(10.0, 10.0)
            point_outside = Vector2d(30.0, 10.0)

            self.assertFalse(point_outside_box(point_inside, bounding_box(polygon)))
            self.assertTrue(point_outside_box(point_outside, bounding_box(polygon)))

        def test_min_dist_point_line(self):
            point = Vector2d(0.0, 1.0)
            line1 = Vector2d(1.0, 0.0)
            line2 = Vector2d(1.0, 2.0)

            (cp, u) = min_distance_point_line(point, line1, line2)
            self.assertEqual(u, 0.5)
            self.assertEqual(cp, Vector2d(1.0, 1.0))

        def test_intersection_line_line(self):
            line11 = Vector2d(0.0, 0.0)
            line12 = Vector2d(4.0, 4.0)

            line21 = Vector2d(4.0, 0.0)
            line22 = Vector2d(0.0, 4.0)

            (cp, u1, u2) = intersection_line_line(line11, line12, line21, line22)
            self.assertEqual(cp, Vector2d(2.0, 2.0))
            self.assertEqual(u1, 0.5)
            self.assertEqual(u2, 0.5)

        def test_intersection_line_line_parallel(self):
            line11 = Vector2d(0.0, 0.0)
            line12 = Vector2d(0.0, 4.0)

            line21 = Vector2d(0.0, 0.0)
            line22 = Vector2d(0.0, 4.0)

            (cp, u1, u2) = intersection_line_line(line11, line12, line21, line22)
            self.assertEqual(cp, Vector2d(0.0, 0.0))
            self.assertEqual(u1, 0.0)
            self.assertEqual(u2, 0.0)


    unittest.main()

