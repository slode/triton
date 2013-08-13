from triton.rigidbody2d import RigidBody2d 
from triton.vector2d import Vector2d

class CoordScaler:

    def __init__(self, screen_size, scale=1):
        self.scale = scale
        if self.scale is None:
            self.adaptive_scale = True
            self.scale = 1
        self.screen_size = screen_size
        self.translation = screen_size/2

    def get_coords(self, cosmic_vect):
        screen_coords = cosmic_vect * self.scale + self.translation
        return screen_coords
        if self.adaptive_scale:
            if not 0 < screen_coords.x < screen_size.x:
                pass
        

def main():
    import pygame
    from collections import deque

    screen_scaler = CoordScaler(Vector2d(800, 800), 350.0 / 249209300000.0)
    max_history = 10000

    gravitational_const = 6.67384*10**-11

    earth = RigidBody2d()
    earth._mass = 5.97*10**24
    earth.pos = Vector2d(149600000000.0, 0.0)
    earth.vel = Vector2d(0.0, 29000.8)
    earth_history = deque([screen_scaler.get_coords(earth.pos).tuple()], max_history)

    mars = RigidBody2d()
    mars._mass = 6.42*10**23
    mars.pos = Vector2d(249209300000.0, 0.0)
    mars.vel = Vector2d(0.0, 24000.077)
    mars_history = deque([screen_scaler.get_coords(mars.pos).tuple()], max_history)

    sun = RigidBody2d()
    sun._mass = 1.989*10**30
    sun.pos = Vector2d(0.0, 0.0)

    t = 0
    dt = 3600

    screen = pygame.display.set_mode(screen_scaler.screen_size.tuple())
    clock = pygame.time.Clock()

    def gravity(ent1, ent2):
        """Returns a force vector from one body to another"""
        diff = (ent2.pos-ent1.pos)
        #Universal gravity
        dist = diff.length_sq()
        force = gravitational_const * ent1._mass * ent2._mass / dist
        return diff.normalize() * force

    def draw_history(screen, history_deque):
        if len(history_deque) < 2:
            return

        pygame.draw.lines(
                screen,
                (150,150,150),
                False,
                history_deque,
                1)

    def int_tuple(tup):
        return (int(tup[0]), int(tup[1]))

    counter = 0
    while not pygame.QUIT in [e.type for e in pygame.event.get()]:
        counter += 1

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

        t += dt
        print("Simulation time (in days): " + str(t/(3600*24)))

        screen.fill((10, 10, 20))
        # draw the sun        
        sun_screen_coords = int_tuple(screen_scaler.get_coords(sun.pos).tuple())
        pygame.draw.circle(screen, (220,200,100), sun_screen_coords, 20, 0)

        # draw the earth
        earth_screen_coords = int_tuple(screen_scaler.get_coords(earth.pos).tuple())
        pygame.draw.circle(screen, (50,50,200), earth_screen_coords, 10, 0)
        if counter % 10 == 0:
            earth_history.append(earth_screen_coords)
        draw_history(screen, earth_history)

        # draw mars
        mars_screen_coords = int_tuple(screen_scaler.get_coords(mars.pos).tuple())
        pygame.draw.circle(screen, (200,100,100), mars_screen_coords, 10, 0)
        if counter % 10 == 0:
            mars_history.append(mars_screen_coords)
        draw_history(screen, mars_history)

        pygame.display.flip()

        pygame.time.wait(0)


if __name__ == '__main__':
    main()
