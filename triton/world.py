#-------------------------------------------------------------------------------
# Name:        World
# Purpose:
#
# Author:      Stian Lode
#
# Created:     15.09.2012
# Copyright:   (c) Stian Lode 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

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
