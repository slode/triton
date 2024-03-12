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


class AtomicForceLink(object):
    """A link between two rigid bodies.

    The link applies the classical spring-damper second degree differential
    equation to the link.
    """

    def __init__(self, rb1, rb2, damping=0.3, spring=3.0, length=50):
        self._rb1 = rb1
        self._rb2 = rb2
        self._damping = damping
        self._spring = spring
        self._length = length
        self._f = 0

    def resolve(self):
        x = self._rb1.pos - self._rb2.pos
        dx = self._rb1.vel - self._rb2.vel
        if x.length() == 0.0:
            return
        n = x.unit_vector()
        fa = self._spring / x.length() ** 2
        fr = -self._damping / x.length()
        self._f = fa + fr
        self._f *= 0.99

        self._rb1.apply_force_to_com(n * self._f)
        self._rb2.apply_force_to_com(n * -self._f)


class Link(AtomicForceLink):
    def __init__(self, rb1, rb2, damping=20.3, spring=30.0, length=100):
        super(Link, self).__init__(rb1, rb2, damping=damping, spring=spring, length=length)

    def draw(self, screen):
        if abs(self._f) < 0.1:
            pygame.draw.aaline(
                screen, (150, 250, 150), self._rb1.pos.tuple(), self._rb2.pos.tuple()
            )
        else:
            pygame.draw.aaline(
                screen, (250, 150, 150), self._rb1.pos.tuple(), self._rb2.pos.tuple()
            )


def update_links(spheres):
    links = []
    for me in range(len(spheres)):
        for neigh in range(me, len(spheres)):
            if me != neigh:
                links.append(Link(spheres[me], spheres[neigh]))
    return links


def main():
    spheres = []
    sphere_col = []
    downward = Vector2d(0.0, 0.0)  # 9.81)

    for i in range(15):
        pos = Vector2d(random.random() * 400.0, random.random() * 400.0)
        vel = Vector2d(0.0, 0.0)
        sphere = Sphere(mass=1.0, radius=4.0, pos=pos, vel=vel, damping=0.0, elasticity=0.97)

        spheres.append(sphere)
        sphere_col.append(
            (int(sphere.x) % 255, int(sphere.y) % 255, int(sphere.radius) * 255 % 255)
        )

    links = update_links(spheres)

    t = 0
    dt = 0.03

    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()

    while not pygame.QUIT in [e.type for e in pygame.event.get()]:

        for sphere in spheres:
            if sphere.y > 650:
                counter_force = Vector2d(0.0, 100 * (650 - sphere.y))
                sphere.apply_force_to_com(counter_force)
            if sphere.x < 10:
                counter_force = Vector2d(100.0 * (10.0 - sphere.x), 0.0)
                sphere.apply_force_to_com(counter_force)
            if sphere.x > 790:
                counter_force = Vector2d(100.0 * (790 - sphere.x), 0.0)
                sphere.apply_force_to_com(counter_force)

        for sphere in spheres:
            sphere.apply_force_to_com(sphere.mass * downward)

        update_links(spheres)
        for link in links:
            link.resolve()

        screen.fill((255, 245, 225))

        pygame.draw.aaline(screen, (0, 0, 0), (0, 650), (800, 650))

        # links = update_links(spheres)
        for link in links:
            link.draw(screen)

        for n, sphere in enumerate(spheres):
            pygame.draw.circle(screen, sphere_col[n], sphere.pos.tuple(), int(sphere.radius), 0)

        for sphere in spheres:
            sphere.update(t, dt)

        pygame.display.flip()
        t += dt


if __name__ == "__main__":
    main()
