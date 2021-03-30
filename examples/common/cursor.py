from triton.sphere import Sphere

class Cursor(Sphere):

    def __init__(self, **args):
        super(Cursor, self).__init__(mass=1.0, radius=80.0, damping=0.0, elasticity=0.7)
        self._pressed = False

    def press(self):
        self._pressed = True

    def release(self):
        self._pressed = False

    def is_pressed(self):
        return self._pressed
