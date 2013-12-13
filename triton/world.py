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
 
 
from triton.vector3d import Vector3d

class World(object):
    def __init__(self):
        self._bodies = []
        self._gravity = Vector3d(0, 9.81, 0)
        self._time = 0
        self._time_slice = 0.1

    @property
    def gravity(self):
        return self._gravity

    @gravity.setter
    def gravity(self, gravity):
        self._gravity = gravity

    def add_body(self, body):
        body.world = self
        self._bodies.append(body)

    def update(self):
        for body in self._bodies:
            body.update(self._time, self._time_slice)

def main():
    from triton.rigidbody2d import RigidBody2d
    world = World()
    world.gravity = Vector3d(0, 9.81, 0)
    world.add_body(RigidBody2d())
    for i in range(100):
        world.update()
        print(world._bodies[0])

if __name__ == '__main__':
    main()
