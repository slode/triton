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
from triton.ecs import Registry, System, Component

import random

############################
###      Components      ###
############################
class Centroid(Component):
    def __init__(self, center=Vector2d(400.0, 400.0), g=10.05):
        self.center = center
        self.g = g

    def new_c(self):
        self.center = Vector2d(random.randrange(800.0),
                               random.randrange(800.0))


class RigidBody(Component):
    def __init__(self, sphere):
        self.sphere = sphere

class Movable(Component):
    pass

class FlipColorsEvent(Component):
    pass

class GameQuitEvent(Component):
    pass


class Drawable(Component):
    def __init__(self):
        self.color = (
                random.randrange(255),
                random.randrange(255),
                random.randrange(255))

############################
###       Systems        ###
############################
class SimulationSystem(System):
    def __init__(self, t=0, dt=0.1):
        self.t = t
        self.dt = dt

    def update(self, *args, **kwargs):
        for e, (r, m) in self.registry.get_components(
                RigidBody, Movable):
            r.sphere.update(self.t, self.dt)
        self.t += self.dt

import pygame
import pygame.gfxdraw
class RenderSystem(System):
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 800))
        self.clock = pygame.time.Clock()

    def update(self, *args, **kwargs):
        flip = self.registry.get_entities(FlipColorsEvent)
        draw = (pygame.gfxdraw.aacircle 
                if flip
                else pygame.gfxdraw.filled_circle)

        self.screen.fill((255,245,225))
        for e, (r, d) in self.registry.get_components(
                RigidBody, Drawable):
            draw(self.screen,
                 int(r.sphere.pos[0]),
                 int(r.sphere.pos[1]),
                 int(r.sphere.radius),
                 d.color)

        for e, (c, d) in self.registry.get_components(
                Centroid, Drawable):
            draw(self.screen,
                 int(c.center[0]),
                 int(c.center[1]),
                 int(10),
                 (20,20,20))
        self.clock.tick(60)
        pygame.display.flip()

class CollisionSystem(System):
    def update(self):
        for e, (r, m) in self.registry.get_components(
                RigidBody, Movable):
            for e2, (r2, m2) in self.registry.get_components(
                    RigidBody, Movable):
                if e < e2 and r.sphere.collides_with(r2.sphere):
                    r.sphere.resolve_collision(r2.sphere)

class GravitationalSystem(System):
    def update(self):
        ec, [c] = next(self.registry.get_components(Centroid))
        for e, (r, m) in self.registry.get_components(
                RigidBody, Movable):
            force_vect = c.center - r.sphere.pos
            r.sphere.apply_force(
                    r.sphere.pos,
                    force_vect.normalize() * r.sphere.mass * c.g / force_vect.length_sq())

class InputSystem(System):
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.registry.add_entity(GameQuitEvent())
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    self.registry.add_entity(GameQuitEvent())
                elif event.key == pygame.K_ESCAPE:
                    self.registry.add_entity(GameQuitEvent())
                elif event.key == pygame.K_f:
                    e = self.registry.get_entities(FlipColorsEvent)
                    if e:
                        self.registry.remove_entities(e)
                    else:
                        self.registry.add_entity(FlipColorsEvent())
                elif event.key == pygame.K_c:
                    e, [c] = next(self.registry.get_components(Centroid))
                    c.new_c()

def main():
    regs = Registry()

    for i in range(30):
        sphere = Sphere(
            mass = float(random.randrange(10.0, 50.0)),
            radius = random.randrange(10.0, 30.0),
            pos = Vector2d(random.randrange(800.0),
                           random.randrange(800.0)),
            damping = 0.0,
            elasticity = 0.97
            )
        regs.add_entity(
                RigidBody(sphere),
                Drawable(),
                Movable())

    regs.add_entity(
            Centroid(),
            Drawable())

    regs.add_system(InputSystem())
    regs.add_system(CollisionSystem())
    regs.add_system(GravitationalSystem())
    regs.add_system(SimulationSystem())
    regs.add_system(RenderSystem())

    while not any(regs.get_components(GameQuitEvent)):
        regs.update()

if __name__ == '__main__':
    main()
