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
 
 
import pygame
import random, math
from triton.vector2d import Vector2d
from triton.sphere import Sphere
from triton.spatial_hash import SpatialHash
from triton.spring_damper_link import SpringDamperLink


class Link(SpringDamperLink):
    def __init__(self, rb1, rb2, damping=0.3, spring=3.0, length=50):
        super(Link, self).__init__(
                rb1, rb2, damping=damping, spring=spring, length=length)

    def draw(self, screen):
        x = self._rb1.pos - self._rb2.pos
        d = x.length()/self._length
        if 0.9 < d < 1.1:
            pygame.draw.aaline(screen, (150,250,150), self._rb1.pos.tuple(), self._rb2.pos.tuple())
        else:
            pygame.draw.aaline(screen, (250,150,150), self._rb1.pos.tuple(), self._rb2.pos.tuple())

def main():
    spheres = []
    sphere_col = []
    center = Vector2d(400.0, 400.0)
    downward = Vector2d(0.0, 9.81)

    width = 6
    length = 6
    for y in range(1, length+1):
        for x in range(1, width+1):
            pos = Vector2d(float(100.0*x), float(100.0*y))
            sphere = Sphere(
                mass = 1.0,
                radius = 1.0,
                pos = pos,
                damping = 0.1,
                elasticity = 0.97
                )

            spheres.append(sphere)
            sphere_col.append((int(sphere.x)%255,int(sphere.y)%255,int(sphere.radius)*255%255))

    for sphere in spheres[-width:]:
        sphere.mass = 10.0

    links = []
    for i, sphere in enumerate(spheres):
        try:
            down = spheres[i+width]
            links.append(Link(sphere, down, length=100))
        except:
            pass

        try:
            if i % width > 0:
                downright = spheres[i+width-1]
                links.append(Link(sphere, downright, length=140))
        except:
            pass

        try:
            if (i+1) % width != 0:
                left = spheres[i+1]
                links.append(Link(sphere, left, length=100))
        except:
            pass

        try:
            if (i+1) % width != 0:
                downleft = spheres[i+width+1]
                links.append(Link(sphere, downleft, length=140))
        except:
            pass

    t = 0
    dt = 0.1

    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()

    grid = SpatialHash()
    while not pygame.QUIT in [e.type for e in pygame.event.get()]:
        grid.update(spheres)

        for sphere in spheres:
            if sphere.y > 650 and sphere.vel.y > 0:
                counter_force = Vector2d(0.0, 100*(650 -sphere.y))
                sphere.apply_force_to_com(counter_force)
            if sphere.x < 10:
                counter_force = Vector2d(100.0*(10.0-sphere.x), 0.0)
                sphere.apply_force_to_com(counter_force)
            if sphere.x > 790:
                counter_force = Vector2d(100.0*(790-sphere.x), 0.0)
                sphere.apply_force_to_com(counter_force)

        for sphere in spheres:
            sphere.apply_force_to_com(sphere.mass * downward)

        for link in links:
            link.resolve()

        screen.fill((255,245,225))
        for link in links:
            link.draw(screen)

        for n, sphere in enumerate(spheres):
            pygame.draw.circle(
                    screen, sphere_col[n], sphere.pos.tuple(), int(sphere.radius), 0)

        for sphere in spheres:#[width:]:
            sphere.update(t, dt)

        pygame.display.flip()
        t += dt


if __name__ == '__main__':
    main()
