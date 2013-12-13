import pygame
import random, math
from triton.vector2d import Vector2d
from triton.sphere import Sphere
from triton.spatial_hash import SpatialHash
from triton.spring_damper_link import SpringDamperLink


class Link(SpringDamperLink):
    def __init__(self, rb1, rb2, damping=0.2, spring=2.0, length=50):
        super(Link, self).__init__(
            rb1, rb2, damping=damping, spring=spring, length=length)

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
    center = Vector2d(400.0, 400.0)
    downward = Vector2d(0.0, 9.81)

    width = 8
    length = 8
    for y in range(1, length+1):
        for x in range(1, width+1):
            pos = Vector2d(float(50.0*x), float(40.0*y+x*15.0))
            sphere = Sphere(
                mass = 0.5,
                radius = 1.0,
                pos = pos,
                damping = 0.1,
                elasticity = 0.97
                )

            spheres.append(sphere)
            sphere_col.append((int(sphere.x)%255,
                               int(sphere.y)%255,
                               int(sphere.radius)*255%255))


    links = []
    for i, sphere in enumerate(spheres):
        try:
            down = spheres[i+width]
            links.append(Link(sphere, down, length=50))
        except IndexError:
            pass

        try:
            if i % width > 0:
                downright = spheres[i+width-1]
                links.append(Link(sphere, downright, length=50*1.40))
        except IndexError:
            pass

        try:
            if (i+1) % width != 0:
                left = spheres[i+1]
                links.append(Link(sphere, left, length=50))
        except IndexError:
            pass

        try:
            if (i+1) % width != 0:
                downleft = spheres[i+width+1]
                links.append(Link(sphere, downleft, length=50*1.40))
        except IndexError:
            pass

    t = 0
    dt = 0.1

    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()
    
    grid = SpatialHash()
    while not pygame.QUIT in [e.type for e in pygame.event.get()]:
        grid.update(spheres)

        for sphere in spheres:
            sphere.apply_force_to_com(sphere.mass * downward)

        for link in links:
            link.resolve()

        screen.fill((255,245,225))

        for n, sphere in enumerate(spheres):
            pygame.draw.circle(
                    screen, sphere_col[n], sphere.pos.tuple(), int(sphere.radius), 0)

        for link in links:
            link.draw(screen)

        for sphere in spheres[width:]:
            sphere.update(t, dt)

        pygame.display.flip()
        t += dt


if __name__ == '__main__':
    main()
