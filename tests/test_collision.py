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
from triton.vector2d import Vector2d
from triton.sphere import Sphere
from triton.rectangle import Rectangle


def test_sphere_direct_hit():
    sphere1 = Sphere(
        mass=1, radius=10, pos=Vector2d(10, 10), vel=Vector2d(0, 10), damping=0.0, elasticity=1.0
    )
    sphere2 = Sphere(
        mass=1, radius=10, pos=Vector2d(10, 30), vel=Vector2d(0, -10), damping=0.0, elasticity=1.0
    )
    collides = sphere1.collides_with(sphere2)
    assert sphere1.pos == (10, 10), "First check"
    assert collides == True
    assert sphere1.dtheta == 0, "First dtheta"
    sphere1.resolve_collision(sphere2)
    assert sphere1.dtheta == 0
    assert sphere1.pos == (10, 10)
    assert sphere1.vel == (0, -10)


def test_sphere_gracing_hit():
    sphere1 = Sphere(
        mass=1, radius=10, pos=Vector2d(10, 10), vel=Vector2d(10, 0), damping=0.0, elasticity=1.0
    )
    sphere2 = Sphere(
        mass=1, radius=10, pos=Vector2d(10, 30), vel=Vector2d(0, 0), damping=0.0, elasticity=1.0
    )
    collides = sphere1.collides_with(sphere2)
    assert sphere1.pos == (10, 10), "First check"
    assert collides == True
    sphere1.resolve_collision(sphere2)
    assert sphere1.dtheta == 0
    assert sphere2.dtheta == 0
    assert sphere1.pos == (10, 10)
    assert sphere1.vel == (10, 0)


def test_sphere_slight_hit():
    sphere1 = Sphere(
        mass=1, radius=10, pos=Vector2d(10, 10), vel=Vector2d(10, 10), damping=0.0, elasticity=1.0
    )
    sphere2 = Sphere(
        mass=1, radius=10, pos=Vector2d(10, 30), vel=Vector2d(0, 0), damping=0.0, elasticity=1.0
    )
    collides = sphere1.collides_with(sphere2)
    assert sphere1.pos == (10, 10), "First check"
    assert collides == True
    sphere1.resolve_collision(sphere2)
    assert sphere1.dtheta == 0
    assert sphere2.dtheta == 0
    assert sphere1.pos == (10, 10)
    assert sphere1.vel == (10, 0)
    assert sphere2.vel == (0, 10)


def _test_rect_slight_hit():
    rect1 = Rectangle(
        mass=1, dimensions=Vector2d(100, 20), pos=Vector2d(50, 10), vel=Vector2d(0, 0), theta=0
    )

    sphere1 = Sphere(
        mass=1,
        radius=10,
        pos=Vector2d(10, 30),
        vel=Vector2d(0, 0),
    )

    collides = rect1.collides_with(sphere1)
    assert collides == True
    rect1.resolve_collision(sphere1)
