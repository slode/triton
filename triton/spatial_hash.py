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

