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
from triton.ecs.ecs import Registry, System, Component, Event

import random

############################
###      Components      ###
############################
class Centroid(Component):
    def __init__(self, center=Vector2d(400.0, 400.0), g=10.05):
        self.center = center
        self.g = g

    def new_c(self, pos=(400,400)):
        self.center = Vector2d(pos[0], pos[1])

class RigidBody(Component):
    def __init__(self, sphere):
        self.sphere = sphere

class Movable(Component):
    pass

class ChangeCenterEvent(Component):
    def __init__(self, pos):
        self.pos = pos

class CollisionEvent(Event):
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2

class FlipColorsEvent(Event):
    pass

class GameQuitEvent(Event):
    pass

class TickEvent(Event):
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
    def initialize(self, t=0, dt=0.1):
        self.t = t
        self.dt = dt
        self.on(TickEvent, self.update)

    def update(self, _):
        for e, (r, m) in self.registry.get_components(
                RigidBody, Movable):
            r.sphere.update(self.t, self.dt)
        self.t += self.dt

import pygame
import pygame.gfxdraw
class RenderSystem(System):
    def initialize(self):
        self.screen = pygame.display.set_mode((800, 800))
        self.clock = pygame.time.Clock()
        self.draw = None
        self.on(FlipColorsEvent, self.toggle_draw)
        self.on(TickEvent, self.tick)
        self.emit(FlipColorsEvent())

    def toggle_draw(self, _):
        self.draw = (pygame.gfxdraw.aacircle
                if self.draw == pygame.gfxdraw.filled_circle
                else pygame.gfxdraw.filled_circle)

    def tick(self, _):
        self.screen.fill((255,245,225))
        for e, (r, d) in self.registry.get_components(
                RigidBody, Drawable):
            self.draw(self.screen,
                     int(r.sphere.pos[0]),
                     int(r.sphere.pos[1]),
                     int(r.sphere.radius),
                     d.color)

        for e, (c, d) in self.registry.get_components(
                Centroid, Drawable):
            self.draw(self.screen,
                     int(c.center[0]),
                     int(c.center[1]),
                     int(10),
                     (20,20,20))

        self.clock.tick(60)
        pygame.display.flip()

class CollisionCheckSystem(System):
    def initialize(self):
        self.on(TickEvent, self.tick)

    def tick(self, _):
        for e1, (r, m) in self.registry.get_components(
                RigidBody, Movable):
            for e2, (r2, m2) in self.registry.get_components(
                    RigidBody, Movable):
                if e1 < e2 and r.sphere.collides_with(r2.sphere):
                    self.emit(CollisionEvent(e1, e2))

class CollisionSystem(System):
    def initialize(self):
        self.on(CollisionEvent, self.on_collision)

    def on_collision(self, c):
        [r1] = self.registry.get_entity(c.e1, RigidBody)
        [r2] = self.registry.get_entity(c.e2, RigidBody)
        r1.sphere.resolve_collision(r2.sphere)

class GravitationalSystem(System):
    def initialize(self):
        self.on(ChangeCenterEvent, self.on_change_center_event)
        self.on(TickEvent, self.tick)

    def on_change_center_event(self, ccevent):
        e, [c] = next(self.registry.get_components(Centroid))
        c.new_c(ccevent.pos)

    def tick(self, _):
        e, [c] = next(self.registry.get_components(Centroid))
        for er, (r, m) in self.registry.get_components(
                RigidBody, Movable):
            force_vect = c.center - r.sphere.pos
            r.sphere.apply_force(
                    r.sphere.pos,
                    force_vect.normalize() * r.sphere.mass * c.g / force_vect.length_sq())

class InputSystem(System):
    def initialize(self):
        self.on(TickEvent, self.tick)

    def tick(self, _):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.emit(GameQuitEvent())
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    self.emit(GameQuitEvent())
                elif event.key == pygame.K_ESCAPE:
                    self.emit(GameQuitEvent())
                elif event.key == pygame.K_f:
                    self.emit(FlipColorsEvent())

        p, _, _ = pygame.mouse.get_pressed()
        if p:
             self.emit(ChangeCenterEvent(pygame.mouse.get_pos()))

class GameLoopSystem(System):
    def initialize(self):
        self.on(GameQuitEvent, self.quit)
        self.on(TickEvent, self.tick)
        self.emit(TickEvent())

    def quit(self, _):
        pygame.quit()
        exit(0)

    def tick(self, _):
        self.emit(TickEvent())

def main():
    regs = Registry()

    for i in range(30):
        m = float(random.randrange(10, 30))
        sphere = Sphere(
            mass = m,
            radius = int(m),
            pos = Vector2d(random.randrange(800.0),
                           random.randrange(800.0)),
            damping = 0.01,
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
    regs.add_system(CollisionCheckSystem())
    regs.add_system(CollisionSystem())
    regs.add_system(GravitationalSystem())
    regs.add_system(SimulationSystem())
    regs.add_system(RenderSystem())
    regs.add_system(GameLoopSystem())

    while True:
        regs.process()

if __name__ == '__main__':
    main()
