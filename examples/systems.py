from triton.vector2d import Vector2d
from triton.sphere import Sphere
from triton.ecs.ecs import Registry, System, Component, Event

from components import *

class SimulationSystem(System):
    def initialize(self, t=0, dt=0.1):
        self.t = t
        self.dt = dt
        self.on(TickEvent, self.update)

    def update(self, _):
        for e, (r, m) in self.registry.get_components(RigidBody, Movable):
            r.sphere.update(self.t, self.dt)

        for e, (l,) in self.registry.get_components(Link):
            l.link.resolve()

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

        clamp = lambda x, l, u: l if x < l else u if x > u else x

        for e, (l, d) in self.registry.get_components(Link, Drawable):
            x = l.link._rb1.pos - l.link._rb2.pos
            d = x.length()/l.link._length
            red     = clamp(abs(1.0-d)*200, 0, 250)
            green   = clamp(abs(d)*200, 0, 250)
            blue = 100
            color = (red, green, blue)
            pygame.draw.aaline(self.screen, color, l.link._rb1.pos.tuple(), l.link._rb2.pos.tuple())

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

class ScreenBounceSystem(System):
    def initialize(self):
        self.on(TickEvent, self.tick)

    def tick(self, _):
        for er, (r, m) in self.registry.get_components(
                RigidBody, Movable):
            if r.sphere.y > 650:
                counter_force = Vector2d(0.0, 100*(650 -r.sphere.y))
                r.sphere.apply_force_to_com(counter_force)

            if r.sphere.x < 10:
                counter_force = Vector2d(100.0*(10.0-r.sphere.x), 0.0)
                r.sphere.apply_force_to_com(counter_force)
            elif r.sphere.x > 790:
                counter_force = Vector2d(100.0*(790-r.sphere.x), 0.0)
                r.sphere.apply_force_to_com(counter_force)

from triton.steering import *
class ForceSystem(System):
    def initialize(self):
        self.on(ChangeCenterEvent, self.on_change_center_event)
        self.on(TickEvent, self.tick)

    def on_change_center_event(self, ccevent):
        e, [c] = next(self.registry.get_components(Centroid))
        c.new_c(ccevent.pos)

    def tick(self, _):

        for er, (r, m, p) in self.registry.get_components(
                RigidBody, Movable, Seeking):
            if p.target is None:
                continue
            (rt,) = self.registry.get_entity(p.target,
                    RigidBody)
            m.force += pursuit(
                    r.sphere.pos, r.sphere.vel,
                    rt.sphere.pos, rt.sphere.vel)

        for er, (r, m, e) in self.registry.get_components(
                RigidBody, Movable, Evading):
            if e.target is None:
                continue
            (rt,) = self.registry.get_entity(e.target,
                    RigidBody)
            m.force += evade_within(
                    r.sphere.pos, r.sphere.vel,
                    rt.sphere.pos, rt.sphere.vel, 50.0)

        for er, (r, m, w) in self.registry.get_components(
                RigidBody, Movable, Wandering):
            m.force += wander(r.sphere.pos, r.sphere.vel, w.displacement, w.dist)

        e, [c] = next(self.registry.get_components(Centroid))
        for er, (r, m) in self.registry.get_components(
                RigidBody, Movable):
            m.force += arrive(r.sphere.pos, r.sphere.vel,
                    c.center, 50.0)

        for er, (r, m) in self.registry.get_components(
                RigidBody, Movable):
            m.force = truncate(m.force, m.max_force)
            r.sphere.apply_force_to_com(
                    m.force / r.sphere.mass)
            m.force = Vector2d(0.0, 0.0)

class SeekCentroidSystem(System):
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

class GravitationalSystem(System):
    def initialize(self):
        self.on(ChangeCenterEvent, self.on_change_center_event)
        self.on(TickEvent, self.tick)

    def on_change_center_event(self, ccevent):
        e, [c] = next(self.registry.get_components(Centroid))
        c.new_c(ccevent.pos)

    def tick(self, _):
        for er, (r, m) in self.registry.get_components(
                RigidBody, Movable):
            force_vect = Vector2d(0, 9.81)
            r.sphere.apply_force_to_com(force_vect)

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
