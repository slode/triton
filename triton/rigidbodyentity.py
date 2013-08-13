#-------------------------------------------------------------------------------
# Name:        RigidBodyEntity
# Purpose:
#
# Author:      Stian Lode
#
# Created:     30.08.2012
# Copyright:   (c) Stian Lode 2012
# Licence:     GPL
#-------------------------------------------------------------------------------

from triton.vector import Vector
from triton.vector2d import Vector2d
from triton.integrator import Integrator

class RigidBody2d(object):
    def __init__(self, world = None):
        self._world = world
        self._mass = 1
        self._inertia = 1
        self._damping = 0.2

        self._state = Vector(
            0, #dx
            0, #dy
            0, #dtheta
            0, # x
            0, # y
            0, #theta
            )
        self._applied_forces = []
        self._applied_force = Vector(0, 0)

    @property
    def x(self): return self._state[3]

    @property
    def y(self): return self._state[4]

    @property
    def theta(self): return self._state[5]

    @property
    def pos(self): return Vector2d(self._state[3], self._state[4])

    def update(self, time, time_slice):
        t, self._state = Integrator.rk4(time, time_slice, self._state, self._accel)

    def apply_force_to_com(self, force):
        self._applies_force += Vector(force[0], force[1], 0)

    def apply_force(self, point_of_contact, force):
        rp = point_of_contact - self.pos
        torque = rp.perp().dot(force)
        self._applied_force += Vector(force[0], force[1], torque)

    def _gravity(self):
        if self._world != None:
            return self._world.gravity
        return Vector(0, 0, 0)

    def _accel(self, time, state):
        return Vector(
            1/self._mass * self._applied_force[0] - self._damping * state[0] - self._gravity()[0],
            1/self._mass * self._applied_force[1] - self._damping * state[1]  - self._gravity()[1],
            1/self._inertia * self._applied_force[2] - self._damping * state[2],
            state[0],
            state[1],
            state[2]
            )

    def __repr__(self):
        return "RigidBody (dx, dy, d0, x, y, 0): " + repr(self._state)

def main():
    ent = RigidBody2d()
    t = 0
    dt = 0.1
    ent.apply_force(Vector2d(0, 0), Vector2d(1, 0))
    for i in range(10):
        ent.update(t, dt)
        print(ent)

if __name__ == '__main__':
    main()
