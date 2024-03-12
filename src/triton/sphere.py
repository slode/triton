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
 
 
import math
from triton.vector2d import Vector2d
from triton.rigidbody2d import RigidBody2d

class Sphere(RigidBody2d):
    def __init__(self, radius=10.0, **args):
        super(Sphere, self).__init__(**args)
        self._radius = radius
        self._inertia = 0.4*self._mass*self._radius**2

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value

    def collides_with(self, other):
        relative_pos = other.pos - self.pos
        dist = (relative_pos).length()
        if dist <= (self.radius+other.radius):
            return True

        return False

    def resolve_collision(self, other):
        relative_pos = other.pos - self.pos

        #edge case where spheres spawn on top of each other
        dist = (relative_pos).length()
        while dist == 0:
            self.pos += self.pos.random()
            relative_pos = other.pos - self.pos
            dist = (relative_pos).length()

        overlap = dist - (self.radius+other.radius)
        norm = relative_pos.unit_vector()

        # if the spheres overlap
        if overlap < 0:
            self.pos += overlap/2*norm
            other.pos -= overlap/2*norm

        relative_vel = other.vel - self.vel

        poi = self.pos + self.radius*norm
        self_poi_perp = (poi-self.pos).perp()
        other_poi_perp = (poi-other.pos).perp()

        nominator = -(1 + self._elasticity)*(relative_vel.dot(norm))
        denominator = norm.dot(norm)*(1/self.mass + 1/other.mass)
        denominator += (self_poi_perp.dot(norm))**2/self.inertia
        denominator += (other_poi_perp.dot(norm))**2/other.inertia
        impulse = nominator / denominator

        impulse_norm = impulse*norm

        self.vel -= impulse_norm/self.mass
        other.vel+= impulse_norm/other.mass

        self.dtheta += (self_poi_perp.dot(impulse_norm))/self.inertia
        other.dtheta += (other_poi_perp.dot(impulse_norm))/other.inertia


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
            sphere1.apply_force(sphere1.pos, fvect.normalize() * float(sphere1.mass) * g_constant / fvect.length_sqrt())

        screen.fill((255,245,225))
        for n, i in enumerate(spheres):
            pygame.draw.circle(screen, sphere_col[n], i.pos.tuple(), int(i.radius), 0)

        for i in range(0, len(spheres)):
            sphere1 = spheres[i]
            sphere1.update(t, dt)


        pygame.display.flip()
#        pygame.time.wait(10)
        t += dt


if __name__ == '__main__':
    main()
