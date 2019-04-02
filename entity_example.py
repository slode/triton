from triton.ecscore import Registry, System, Component

class Movable(Component):
    def __init__(self, dx, dy):
        self.dx, self.dy = dx, dy

class Physical(Component):
    def __init__(self, x, y):
        self.x, self.y = x, y

class Renderable(Component):
    def __init__(self, texture, w, h):
        self.w, self.h = w, h
        self.texture = texture

class Controllable(Component):
    def __init__(self):
        self.controllable = True

class ControlSystem(System):
    def update(self):
        for e, c in self.registry.get_components(Controllable, Movable):
            print(e, c)

class PhysicsSystem(System):
    def update(self):
        for e, (p, m) in self.registry.get_components(Physical, Movable):
            print(e, p, m)

class RenderSystem(System):
    def update(self):
        for e, (p, m, r) in self.registry.get_components(
                Physical, Movable, Renderable):
            print(e, p, m, r)

def main():
    reg = Registry()
    reg.add_entity(Physical(4, 4), Movable(1, 1), Renderable("text1", 2, 2))
    reg.add_entity(Physical(4, 4), Renderable("text1", 2, 2))
    import sys
    reg.add_system(ControlSystem())
    reg.add_system(PhysicsSystem())
    reg.add_system(RenderSystem())

    import time
    while True:
        reg.update()
        time.sleep(1)


main()
