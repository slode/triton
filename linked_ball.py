import pygame
import random, math
from triton.vector2d import Vector2d
from triton.shape import Sphere, SpatialHash

class SpringDamperLink:
    def __init__(self, rb1, rb2, damping=.1, spring=1, length=100):
        self._rb1 = rb1
        self._rb2 = rb2
        self._damping = damping
        self._spring = spring
        self._length = length

    def resolve(self):
        x = self._rb1.pos - self._rb2.pos
        dx = self._rb1.vel - self._rb2.vel
        n = x.unit_vector()
        f = self._spring * (self._length - x.length()) - self._damping * dx.dot(n)
        self._rb1.apply_force_to_com(n * f)
        self._rb2.apply_force_to_com(n * -f)

    def draw(self, screen):
        x = self._rb1.pos - self._rb2.pos
        d = x.length()/self._length
        if 0.9 < d < 1.1:
            pygame.draw.aaline(screen, (150,250,150), self._rb1.pos.tuple(), self._rb2.pos.tuple())
        else:
            pygame.draw.aaline(screen, (250,150,150), self._rb1.pos.tuple(), self._rb2.pos.tuple())


        
def main():
    spheres = []
    sphere_col = []
    downward = Vector2d(0.0, 9.81)

    for i in range(15):
        pos = Vector2d(random.random()*100.0, random.random()*100.0)
        vel = Vector2d(20.0, 0.0)
        sphere = Sphere(
            mass = 1.0,
            radius = 4.0,
            pos = pos,
            vel = vel,
            damping = 0.0,
            elasticity = 0.97
            )

        spheres.append(sphere)
        sphere_col.append((int(sphere.x)%255,int(sphere.y)%255,int(sphere.radius)*255%255))

    links = []
    for sphere_from in spheres:
        for sphere_to in spheres:
            if sphere_from != sphere_to:
                links.append(SpringDamperLink(sphere_from, sphere_to))

    t = 0
    dt = 0.1

    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()

    while not pygame.QUIT in [e.type for e in pygame.event.get()]:

        for sphere in spheres:
            if sphere.y > 650:
                counter_force = Vector2d(0.0, 100*(650 -sphere.y))
                sphere.apply_force_to_com(counter_force)
            if sphere.x < 10:
                counter_force = Vector2d(100.0*(10.0-sphere.x), 0.0)
                sphere.apply_force_to_com(counter_force)
            if sphere.x > 790:
                counter_force = Vector2d(100.0*(790-sphere.x), 0.0)
                sphere.apply_force_to_com(counter_force)


        for sphere in spheres:
            sphere.apply_force_to_com(sphere.mass * downward)

        for link in links:
            link.resolve()

        screen.fill((255,245,225))

        pygame.draw.aaline(screen, (0, 0, 0), (0, 650), (800, 650))

        for link in links:
            link.draw(screen)

        for n, sphere in enumerate(spheres):
            pygame.draw.circle(
                    screen, sphere_col[n], sphere.pos.tuple(), int(sphere.radius), 0)

        for sphere in spheres:
            sphere.update(t, dt)

        pygame.display.flip()
        t += dt


if __name__ == '__main__':
    main()
