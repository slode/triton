import pygame
import random, math
from triton.vector2d import Vector2d
from triton.sphere import Sphere
from triton.spatial_hash import SpatialHash
from triton.spring_damper_link import SpringDamperLink
from triton.cursor import Cursor

class Link(SpringDamperLink):
    def __init__(self, rb1, rb2, damping=.3, spring=0.7, length=50):
        super(Link, self).__init__(
            rb1, rb2, damping=damping, spring=spring, length=length)

    def resolve(self):
        x = self._rb1.pos - self._rb2.pos
        dx = self._rb1.vel - self._rb2.vel
        n = x.unit_vector()
        f = self._spring * (self._length - x.length()) - self._damping * dx.dot(n)
        if f > 0:
            return
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
    center = Vector2d(400.0, 400.0)
    downward = Vector2d(0.0, 9.81)

    width = 10
    length = 10
    for y in range(1, length+1):
        for x in range(1, width+1):
            pos = Vector2d(float(100.0*x), float(100.0 + -x*20.0+20.0*y))
            vel = Vector2d(40.0, 0.0)
            sphere = Sphere(
                mass = 0.1,
                radius = 1.0,
                pos = pos,
                vel = vel,
                damping = 0.1,
                elasticity = 0.97
                )

            spheres.append(sphere)
            sphere_col.append((int(sphere.x)%255,int(sphere.y)%255,int(sphere.radius)*255%255))

    sphere_col.append((int(sphere.x)%255,int(sphere.y)%255,int(sphere.radius)*255%255))
    links = []
    for i, sphere in enumerate(spheres):
        try:
            down = spheres[i+width]
            links.append(Link(sphere, down, length=100.0))
        except:
            pass

        try:
            if i % width > 0:
                downright = spheres[i+width-1]
                links.append(Link(sphere, downright, length=140.0))
        except:
            pass

        try:
            if (i+1) % width != 0:
                left = spheres[i+1]
                links.append(Link(sphere, left, length=100.0))
        except:
            pass

        try:
            if (i+1) % width != 0:
                downleft = spheres[i+width+1]
                links.append(Link(sphere, downleft, length=140.0))
        except:
            pass

    t = 0
    dt = 0.15

    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()

    cursor = Cursor()
    grid = SpatialHash()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                cursor.pos = Vector2d(pos[0], pos[1])
                cursor.press()
                spheres.append(cursor)
                print(cursor.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                spheres.remove(cursor)
                cursor.release()

        grid.update(spheres)

        if cursor.is_pressed():
            pos = pygame.mouse.get_pos()
            cursor.pos = Vector2d(pos[0], pos[1])
            for neighbour in grid.nearby_objects(cursor):
                if cursor.collides_with(neighbour):
                    cursor.resolve_collision(neighbour)


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
