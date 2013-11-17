import pygame
import random, math
from triton.vector2d import Vector2d
from triton.shape import Sphere, SpatialHash

class SpringDamperLink:
    def __init__(self, rb1, rb2, damping=0.2, spring=2.0, length=50):
        self._rb1 = rb1
        self._rb2 = rb2
        self._damping = damping
        self._spring = spring
        self._length = length
        self.ripped = False

    def resolve(self):
        x = self._rb1.pos - self._rb2.pos
        dx = self._rb1.vel - self._rb2.vel
        n = x.unit_vector()
        f = self._spring * (self._length - x.length()) - self._damping * dx.dot(n)
        if f > 0 or self.ripped:
            return
        if f < -65:
            self.ripped = True
            return
        self._rb1.apply_force_to_com(n * f)
        self._rb2.apply_force_to_com(n * -f)

    def draw(self, screen):
        if self.ripped:
            return
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
            sphere_col.append((int(sphere.x)%255,int(sphere.y)%255,int(sphere.radius)*255%255))


    links = []
    for i, sphere in enumerate(spheres):
        try:
            down = spheres[i+width]
            links.append(SpringDamperLink(sphere, down, length=50))
        except:
            pass

        try:
            if i % width > 0:
                downright = spheres[i+width-1]
                #links.append(SpringDamperLink(sphere, downright, length=50*1.40))
        except:
            pass

        try:
            if (i+1) % width != 0:
                left = spheres[i+1]
                links.append(SpringDamperLink(sphere, left, length=50))
        except:
            pass

        try:
            if (i+1) % width != 0:
                downleft = spheres[i+width+1]
                #links.append(SpringDamperLink(sphere, downleft, length=50*1.40))
        except:
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
        for link in links:
            link.draw(screen)

        for n, sphere in enumerate(spheres):
            pygame.draw.circle(
                    screen, sphere_col[n], sphere.pos.tuple(), int(sphere.radius), 0)

        for sphere in spheres[width:]:
            sphere.update(t, dt)

        pygame.display.flip()
        t += dt


if __name__ == '__main__':
    main()
