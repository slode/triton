from triton.vector import Vector
from triton.vector2d import Vector2d
from triton.integrator import Integrator

class RigidBody2d(object):
    def __init__(self,
        world = None,
        mass = 10.0,
        inertia = 10.0,
        damping = 0.0,
        elasticity = 0.8,
        vel = Vector2d(0,0),
        pos = Vector2d(0,0),
        theta = 0,
        dtheta = 0
        ):

        self._world = world
        self._mass = mass
        self._inertia = inertia
        self._damping = damping
        self._elasticity = elasticity

        self._state = Vector(
            0, # dx
            0, # dy
            0, # dtheta
            0, # x
            0, # y
            0, # theta
            )
        self.pos = pos
        self.vel = vel
        self.dtheta = dtheta
        self.theta = theta
        self._applied_force = Vector2d(0, 0)
        self._applied_torque = 0

        self._gravity = Vector(0, 0, 0)

    @property
    def x(self): return self._state[3]

    @property
    def y(self): return self._state[4]

    @property
    def theta(self): return self._state[5]

    @theta.setter
    def theta(self, value):
        self._state[5] = value

    @property
    def dtheta(self): return self._state[2]

    @dtheta.setter
    def dtheta(self, value):
        self._state[2] = value

    @property
    def pos(self): return Vector2d(self._state[3], self._state[4])

    @pos.setter
    def pos(self, vector):
        self._state[3] = vector[0]
        self._state[4] = vector[1]

    @property
    def vel(self): return Vector2d(self._state[0], self._state[1])

    @vel.setter
    def vel(self, vector):
        self._state[0] = vector[0]
        self._state[1] = vector[1]

    @property
    def world(self): return self._world

    @world.setter
    def world(self, world):
        self._world = world

    @property
    def mass(self): return self._mass

    @mass.setter
    def mass(self, mass):
        self._mass = mass

    @property
    def inertia(self): return self._inertia

    @inertia.setter
    def inertia(self, inertia):
        self._inertia = inertia

    def update(self, time, time_slice):
        t, self._state = Integrator.rk4(time, time_slice, self._state, self._accel)
        self._applied_force = Vector2d(0,0)
        self._applied_torque = 0

    def apply_force_to_com(self, force):
        self._applied_force += force

    def apply_force(self, point_of_contact, force):
        rp = point_of_contact - self.pos
        torque = rp.perp().dot(force)
        self._applied_force += force
        self._applied_torque +=  torque

    @property
    def gravity(self):
        if self._world != None:
            return self._world.gravity
        return self._gravity

    @gravity.setter
    def gravity(self, grav):
        self._gravity = grav

    def _accel(self, time, state):
        v = Vector(
            1/self._mass * self._applied_force[0] - self._damping * state[0] - self._gravity[0],
            1/self._mass * self._applied_force[1] - self._damping * state[1]  - self._gravity[1],
            1/self._inertia * self._applied_torque - self._damping * state[2],
            state[0],
            state[1],
            state[2]
            )
        return v


    def __repr__(self):
        return "RigidBody (dx, dy, d0, x, y, 0): " + repr(self._state)

def main():
    import pygame

    distance_scale = 1.0

    gravitational_const = 0.000000001

    earth = RigidBody2d()
    earth._mass = 5.97*10
    earth.pos = Vector2d(550.0, 400.0)
    earth.vel = Vector2d(0.0, 29.0*10**-2)

    mars = RigidBody2d()
    mars._mass = 6.4
    mars.pos = Vector2d(600.0, 400.0)
    mars.vel = Vector2d(0.0, 24.0*10**-2)

    sun = RigidBody2d()
    sun._mass = 1.9*10**10
    sun.pos = Vector2d(400.0, 400.0)

    t = 0
    dt = 0.9

    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()

    def gravity(ent1, ent2):
        """Returns a force vector from one body to another"""
        diff = (ent2.pos-ent1.pos)
        #Universal gravity
        dist = (diff*distance_scale).length_sqrt()
        if dist < 30:
            dist = 30
        force = gravitational_const * ent1._mass * ent2._mass / dist
        return diff.normalize() * force

    def draw_vectors(screen, ent, force1, force2):
        vect1 = ent + force1*10
        vect2 = ent + force2*10

        pygame.draw.lines(screen, (200,100,100), False,
            [(int(vect1.x), int(vect1.y)),
            (int(ent.x), int(ent.y)),
            (int(vect2.x), int(vect2.y))
            ]
            , 1)

    while not pygame.QUIT in [e.type for e in pygame.event.get()]:

        earth_sun = gravity(earth, sun)
        earth_mars = gravity(earth, mars)
        sun_mars = gravity(sun, mars)

        earth.apply_force(earth.pos, earth_sun)
        earth.apply_force(earth.pos, earth_mars)
        mars.apply_force(mars.pos, -sun_mars)
        mars.apply_force(mars.pos, -earth_mars)
        sun.apply_force(sun.pos, sun_mars)
        sun.apply_force(sun.pos, -earth_sun)

        sun.update(t, dt)
        earth.update(t, dt)
        mars.update(t, dt)

        print(earth)
        t += dt

        screen.fill((255,255,150))
        pygame.draw.circle(screen, (250,250,100), (int(sun.x), int(sun.y)), 10, 0)
        pygame.draw.circle(screen, (20,20,200), (int(earth.x), int(earth.y)), 4, 0)
        pygame.draw.circle(screen, (200,100,100), (int(mars.x), int(mars.y)), 4, 0)

        draw_vectors(screen, earth.pos, earth_mars, earth_sun)
        draw_vectors(screen, mars.pos, -earth_mars, -sun_mars)
        draw_vectors(screen, sun.pos, -earth_sun, sun_mars)

        pygame.display.flip()

        pygame.time.wait(5)


if __name__ == '__main__':
    pass
    #main()
