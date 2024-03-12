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
from triton.rigidbody2d import RigidBody2d


class Rectangle(RigidBody2d):
    def __init__(self, dimensions=Vector2d(10.0, 5.0), **args):
        super(Rectangle, self).__init__(**args)
        self._dimensions = dimensions
        self._inertia = 1.0 / 12.0 * self._mass * (self._dimensions.x**2 + self._dimensions.y**2)

    @property
    def dimensions(self):
        return self._dimensions

    @dimensions.setter
    def dimensions(self, value):
        self._dimensions = value

    def collides_with(self, other):
        if hasattr(other, "radius"):
            center = Vector2d(1, 0).rotate(self.theta).normalize()
            center_perp = center.perp()

            relative_pos = other.pos - self.pos
            dist = relative_pos.dot(center)
            lateral_dist = relative_pos.dot(center_perp)

            if (
                abs(dist) <= self.dimensions.x / 2 + other.radius
                and abs(lateral_dist) <= self.dimensions.y / 2 + other.radius
            ):
                return True
            return False

    def resolve_collision(self, other):
        # Get point of impact
        relative_pos = other.pos - self.pos

        # edge case where spheres spawn on top of each other
        dist = (relative_pos).length()
        if dist == 0:
            self.pos += self.pos.random()
            relative_pos = other.pos - self.pos
            dist = (relative_pos).length()

        overlap = dist - (self.radius + other.radius)
        norm = relative_pos.unit_vector()

        # if the spheres overlap
        if overlap < 0:
            self.pos += overlap / 2 * norm
            other.pos -= overlap / 2 * norm

        relative_vel = other.vel - self.vel

        point_of_impact = self.pos + self.radius * norm
        self_poi_perp = (point_of_impact - self.pos).perp()
        other_poi_perp = (point_of_impact - other.pos).perp()

        # Calculate impulse
        nominator = -(1 + self._elasticity) * (relative_vel.dot(norm))
        denominator = norm.dot(norm) * (1 / self.mass + 1 / other.mass)
        denominator += (self_poi_perp.dot(norm)) ** 2 / self.inertia
        denominator += (other_poi_perp.dot(norm)) ** 2 / other.inertia
        impulse = nominator / denominator

        impulse_norm = impulse * norm

        self.vel -= impulse_norm / self.mass
        other.vel += impulse_norm / other.mass

        self.dtheta += (self_poi_perp.dot(impulse_norm)) / self.inertia
        other.dtheta += (other_poi_perp.dot(impulse_norm)) / other.inertia
