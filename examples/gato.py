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
    def __init__(self, rb1, rb2, damping=10.1, spring=1000.0, length=50):
        super(Link, self).__init__(
                rb1, rb2, damping=damping, spring=spring, length=length)

    def draw(self, screen):
        x = self._rb1.pos - self._rb2.pos
        d = x.length()/self._length
        if 0.9 < d < 1.1:
            pygame.draw.aaline(screen, (150,250,150), self._rb1.pos.tuple(), self._rb2.pos.tuple())
        else:
            pygame.draw.aaline(screen, (250,150,150), self._rb1.pos.tuple(), self._rb2.pos.tuple())

class Joint(Sphere):
    def __init__(self, link1, link2):
        self.link1 = link1
        self.link2 = link2

class Manipulator:
    def __init__(self):
        self.links = []

    def add_link(self, sphere, link):
        pass

def main():
    spheres = []
    center = Vector2d(400.0, 400.0)
    downward = Vector2d(0.0, 9.81)

    manipulator = [
            (Vector2d(400.0, 400.0), 0.0),
            (Vector2d(390.0, 500.0), 100.0),
            (Vector2d(410.0, 600.0), 100.0),
            (Vector2d(410.0, 700.0), 100.0),
            (Vector2d(410.0, 800.0), 100.0),
            ]
    links = []

    prev_sphere = None
    for pos, length in manipulator:
        sphere = Sphere(
            mass = 10.0,
            radius = 3.0,
            pos = pos,
            damping = 0.0,
            elasticity = 1.0
            )

        spheres.append(sphere)
        if prev_sphere is not None:
            links.append(Link(sphere, prev_sphere, length=length))
        prev_sphere = sphere

    def apply_torque(screen, sphere1, sphere2, link, dt):
        target = Vector2d(10.0, -10.0)
        link_vector = sphere2.pos - sphere1.pos
        vec = link_vector.perp().normalize()
        deviation = target.angle_diff(link_vector)
        
        Kc = 80.0
        # P
        force = Kc * 2.9 * deviation

        # I
        if hasattr(sphere2, "sum_deviation"):
            sphere2.sum_deviation += deviation * dt
            iforce = sphere2.sum_deviation * 0.1 * Kc 
            force += iforce
        else:
            sphere2.sum_deviation = 0.0
        
        # D
        if hasattr(sphere2, "prev_deviation"):
            dforce = (sphere2.prev_deviation - deviation) / dt
            force += dforce * -8.4 * Kc 

        sphere2.prev_deviation = deviation

        sphere2.apply_force_to_com(vec * -1.0 * force)
    
    t = 0
    dt = 0.01

    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()

    grid = SpatialHash()
    while not pygame.QUIT in [e.type for e in pygame.event.get()]:
        contact_force_links = []

        grid.update(spheres)

        for sphere in spheres:
            if sphere.y > 650 and sphere.vel.y > 0:
                counter_force = Vector2d(0.0, 100*(650 -sphere.y))
                sphere.apply_force_to_com(counter_force)
            if sphere.x < 10:
                counter_force = Vector2d(0.0*(10.0-sphere.x), 0.0)
                sphere.apply_force_to_com(counter_force)
            if sphere.x > 790:
                counter_force = Vector2d(0.0*(790-sphere.x), 0.0)
                sphere.apply_force_to_com(counter_force)

        for sphere in spheres[:]:
            sphere.apply_force_to_com(sphere.mass * downward)

        for s1, s2, l in zip(spheres, spheres[1:], links):
            apply_torque(screen, s1, s2, l, dt)

        for link in contact_force_links:
            link.resolve()

        for link in links:
            link.resolve()

        screen.fill((255,245,225))
        for link in links:
            link.draw(screen)

        for n, sphere in enumerate(spheres):
            pygame.draw.circle(
                    screen,
                    (100,100,100,100),
                    sphere.pos.tuple(),
                    int(sphere.radius),
                    0)

        for sphere in spheres[1:]:
            sphere.update(t, dt)

        pygame.display.flip()
        t += dt


if __name__ == '__main__':
    main()
