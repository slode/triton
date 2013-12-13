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
 
 
from triton.vector2d import Vector2d
import math

class SpatialHash(object):
    def __init__(self, map_size = Vector2d(800, 800), grid_size = 70):
        self._map_size = map_size
        self._grid_size = grid_size
        self.reset()

    def reset(self):
        self._grid = {}

    def update(self, bodies):
        self.reset()
        for b in bodies:
            self._add_body(b)

    def _add_body(self, body):
        for i in self._sweep(body):
                self._grid.setdefault(i, []).append(body)

    def _hash(self, x, y):
        return x + y * int(self._map_size.x/self._grid_size)

    def _scale_to_grid(self, pos):
        return Vector2d(int(math.floor(pos.x / self._grid_size)), int(math.floor(pos.y / self._grid_size)))

    def _sweep(self, body):
        min = self._scale_to_grid(body.pos - body.radius)
        max = self._scale_to_grid(body.pos + body.radius)

        for x in range(int(min.x), int(max.x+1)):
            for y in range(int(min.y), int(max.y+1)):
                yield self._hash(x, y)

    def nearby_objects(self, body):
        for h in self._sweep(body):
            try:
                bucket = self._grid[h]
                for o in bucket:
                    if o != body:
                        yield o
            except:
                pass

