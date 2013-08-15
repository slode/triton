import pygame
import random, math
from triton.vector2d import Vector2d
from triton.shape import Sphere, SpatialHash

class SpringDamperLink:
    def __init__(self, rb1, rb2, damping=.5, spring=1, length=250):
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
    center = Vector2d(300.0, 300.0)
    g_constant = 10.005
    downward = Vector2d(0.0, 9.81)

    for i in range(15):
        w = random.random()*2+4
        pos = Vector2d(random.random()*600.0, random.random()*600.0)
        vel = (center - pos).perp().normalize()
        sphere = Sphere(
            mass = w * 0.2,
            radius = w * 1.0,
            pos = pos,
            damping = 0.5,
            elasticity = 0.97
            )

        spheres.append(sphere)
        sphere_col.append((int(sphere.x)%255,int(sphere.y)%255,int(sphere.radius)*255%255))

    links = []
    for sphere_from in spheres:
        for sphere_to in spheres:
            if sphere_from != sphere_to: # and random.random()*5 > 4.5:
                links.append(SpringDamperLink(sphere_from, sphere_to))
    
    t = 0
    dt = 0.1

    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()

    grid = SpatialHash()
    while not pygame.QUIT in [e.type for e in pygame.event.get()]:
        grid.update(spheres)

        for sphere in spheres:
            for neighbour in grid.nearby_objects(sphere):
                if sphere.collides_with(neighbour):
                    sphere.resolve_collision(neighbour)

        for sphere in spheres:
            fvect = center - sphere.pos
            sphere.apply_force_to_com(
                    fvect.normalize() * sphere.mass * g_constant / fvect.length_sq())

        for link in links:
            link.resolve()

        screen.fill((255,245,225))
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
