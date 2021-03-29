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

from triton.vector2d import Vector2d

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

def point_in_polygon(point, polygon):
    bb = bounding_box(polygon)
    # fail-fast check
    if point_outside_box(point, bb):
        return False

def main():
    polygon = []
    polygon.append(Vector2d(0.0, 0.0))
    polygon.append(Vector2d(10.0, 0.0))
    polygon.append(Vector2d(20.0, 10.0))
    polygon.append(Vector2d(10.0, 10.0))
    polygon.append(Vector2d(0.0, 10.0))

    point_inside = Vector2d(10.0, 10.0)
    point_outside = Vector2d(30.0, 10.0)

    assert not point_outside_box(point_inside, bounding_box(polygon))
    assert point_outside_box(point_outside, bounding_box(polygon))

if __name__ == '__main__':
    main()

