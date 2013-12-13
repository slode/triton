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
from triton.sphere import Sphere
from triton.spatial_hash import SpatialHash

def main():
    import pygame

    spheres = []
    sphere_col = []
    center = Vector2d(400.0, 400.0)
    g_constant = 10.005
    import random
    for i in range(15):
        w = random.random()*20+10
        pos = Vector2d(random.random()*800.0, random.random()*800.0)
        vel = (center - pos).perp().normalize()
        sphere = Sphere(
            mass = w*10**1,
            radius = w,
            pos = pos,
            #vel = vel,
            damping = 0,
            elasticity = 0.97

            )
        spheres.append(sphere)
        sphere_col.append((int(sphere.x)%255,int(sphere.y)%255,int(sphere.radius)*255%255))

    t = 0
    dt = 0.1

    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()
    grid = SpatialHash()

    xrange_offset = Vector2d(10, 0)
    yrange_offset = Vector2d(0, 10)

    while not pygame.QUIT in [e.type for e in pygame.event.get()]:
        grid.update(spheres)

        if random.randrange(1, 1000) == 1:
            center = Vector2d(random.random()*400.0 + 200, random.random()*400.0 + 200)

        for i in range(0, len(spheres)):
            sphere = spheres[i]
            for neighbour in grid.nearby_objects(sphere):
                if sphere.collides_with(neighbour):
                    sphere.resolve_collision(neighbour)

        for i in range(0, len(spheres)):
            sphere1 = spheres[i]
            fvect = center - sphere1.pos
            sphere1.apply_force(sphere1.pos, fvect.normalize() * float(sphere1.mass) * g_constant / fvect.length_sq())

        screen.fill((255,245,225))
        for n, i in enumerate(spheres):
            pygame.draw.circle(screen, sphere_col[n], i.pos.tuple(), int(i.radius), 0)
            #pygame.draw.aaline(screen, (250,250,250), i.pos.tuple(), (i.pos + Vector2d(1,0).rotate(i.theta)*i.radius).tuple())

            #pygame.draw.aaline(screen, sphere_col[0], i.pos.tuple(), ((i.pos+i._applied_force)).tuple())
            #pygame.draw.aaline(screen, (5,5,5), i.pos.tuple(), (i.pos + i.vel).tuple())

        for i in range(0, len(spheres)):
            sphere1 = spheres[i]
            sphere1.update(t, dt)


        pygame.display.flip()
#        pygame.time.wait(10)
        t += dt


if __name__ == '__main__':
    main()
