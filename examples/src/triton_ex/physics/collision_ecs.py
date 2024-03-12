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

import random

from triton.vector2d import Vector2d
from triton.sphere import Sphere
from triton.ecs.ecs import Registry


from triton_ex.common.systems import (
    InputSystem,
    CollisionSystem,
    CollisionCheckSystem,
    SeekCentroidSystem,
    SimulationSystem,
    RenderSystem,
    GameLoopSystem,
)
from triton_ex.common.components import RigidBody, Drawable, Movable, Centroid, Drawable


def main():
    regs = Registry()

    for i in range(30):
        m = float(random.randrange(10, 30))
        sphere = Sphere(
            mass=m,
            radius=int(m),
            pos=Vector2d(random.randrange(800.0), random.randrange(800.0)),
            damping=0.01,
            elasticity=0.97,
        )
        regs.add_entity(RigidBody(sphere), Drawable(), Movable())

    regs.add_entity(Centroid(), Drawable())

    regs.add_system(InputSystem())
    regs.add_system(CollisionCheckSystem())
    regs.add_system(CollisionSystem())
    regs.add_system(SeekCentroidSystem())
    regs.add_system(SimulationSystem())
    regs.add_system(RenderSystem())
    regs.add_system(GameLoopSystem())

    while True:
        regs.process()


if __name__ == "__main__":
    main()
