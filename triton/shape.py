#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Eier
#
# Created:     17.09.2012
# Copyright:   (c) Eier 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
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
        if dist == 0:
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

class Rectangle(RigidBody2d):
    def __init__(self, dimensions=Vector2d(10.0, 5.0), **args):
        super(Rectangle, self).__init__(**args)
        self._dimensions = dimensions
        self._inertia = 1.0/12.0*self._mass*(self._dimensions.x**2 +
                        self._dimensions.y**2)

    @property
    def dimensions(self):
        return self._dimensions

    @dimensions.setter
    def dimensions(self, value):
        self._dimensions = value

    def collides_with(self, other):
        center = Vector2d(1,0).rotate(self.theta).normalize()
        center_perp = center.perp()

        relative_pos = other.pos - self.pos
        dist = relative_pos.dot(center)
        lateral_dist = relative_pos.dot(center_perp)

        if (abs(dist) <= self.dimensions.x/2 + other.radius and
            abs(lateral_dist) <= self.dimensions.y/2+other.radius):
            return True
        return False

    def resolve_collision(self, other):
        relative_pos = other.pos - self.pos

        #edge case where spheres spawn on top of each other
        dist = (relative_pos).length()
        if dist == 0:
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

#        if relative_vel.length_sqrt() < 16:
#            return

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



class SpatialHash(object):
    def __init__(self, map_size = Vector2d(800, 800), grid_size = 70):
        self._map_size = map_size
        self._grid_size = grid_size
        self.reset()

    def reset(self):
        self._grid = {}

    def update(self, bodies):
        self.reset()
        for b in bodies:
            self._add_body(b)

    def _add_body(self, body):
        for i in self._sweep(body):
                self._grid.setdefault(i, []).append(body)

    def _hash(self, x, y):
        return x + y * int(self._map_size.x/self._grid_size)

    def _scale_to_grid(self, pos):
        return Vector2d(int(math.floor(pos.x / self._grid_size)), int(math.floor(pos.y / self._grid_size)))

    def _sweep(self, body):
        min = self._scale_to_grid(body.pos - body.radius)
        max = self._scale_to_grid(body.pos + body.radius)

        for x in range(int(min.x), int(max.x+1)):
            for y in range(int(min.y), int(max.y+1)):
                yield self._hash(x, y)

    def nearby_objects(self, body):
        for h in self._sweep(body):
            try:
                bucket = self._grid[h]
                for o in bucket:
                    if o != body:
                        yield o
            except:
                pass

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
