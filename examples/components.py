from triton.ecs.ecs import Component, Event
from triton.vector2d import Vector2d

import random

class Link(Component):
    def __init__(self, link):
        self.link = link

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
    def __init__(self):
        self.force = 0
        self.max_force = 10.0

class Wandering(Component):
    def __init__(self):
        self.displacement = Vector2d(1.0,0.0)
        self.dist = 30.0

class Seeking(Component):
    def __init__(self, target=None):
        self.target = target

class Evading(Component):
    def __init__(self, target=None):
        self.target = target

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
