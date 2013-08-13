#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Eier
#
# Created:     15.09.2012
# Copyright:   (c) Eier 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from triton.world import World
from triton.rigidbodyentity import RigidBodyEntity

def main():
    world = World()
    world.set_gravity([0, -9.81, 0])
    ent = RigidBodyEntity(world)

    for i in range(1000):
        world.update(0.5)

if __name__ == '__main__':
    main()
