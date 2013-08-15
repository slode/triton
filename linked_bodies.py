import pygame
import random, math
from triton.vector2d import Vector2d
from triton.shape import Sphere, SpatialHash

class SpringDamperLink:
    def __init__(self, rb1, rb2, damping=1, spring=1, length=50):
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
    center = Vector2d(400.0, 400.0)
    g_constant = 1.005
    downward = Vector2d(0.0, 9.81)

    stationary_sphere =  Sphere(
            mass = 10**23,
            radius = 5.0,
            pos = Vector2d(300.0, 30.0),
            damping = 0.4,
            elasticity = 0.97
            )
    spheres.append(stationary_sphere)
    sphere_col.append((int(stationary_sphere.x)%255,int(stationary_sphere.y)%255,int(stationary_sphere.radius)*255%255))

    stationary_sphere2=  Sphere(
            mass = 10**23,
            radius = 5.0,
            pos = Vector2d(400.0, 30.0),
            damping = 0.4,
            elasticity = 0.97
            )
    spheres.append(stationary_sphere2)
    sphere_col.append((int(stationary_sphere2.x)%255,int(stationary_sphere2.y)%255,int(stationary_sphere2.radius)*255%255))

    stationary_sphere3=  Sphere(
            mass = 10**23,
            radius = 5.0,
            pos = Vector2d(500.0, 30.0),
            damping = 0.4,
            elasticity = 0.97
            )
    spheres.append(stationary_sphere3)
    sphere_col.append((int(stationary_sphere3.x)%255,int(stationary_sphere3.y)%255,int(stationary_sphere3.radius)*255%255))

    for i in range(9):
        pos = Vector2d(random.random()*800.0, random.random()*800.0)
        vel = (center - pos).perp().normalize()
        sphere = Sphere(
            mass = 1.5,
            radius = 1.0,
            pos = pos,
            damping = 0.99,
            elasticity = 0.97
            )

        spheres.append(sphere)
        sphere_col.append((int(sphere.x)%255,int(sphere.y)%255,int(sphere.radius)*255%255))

    links = []
    for i, sphere in enumerate(spheres):
        try:
            down = spheres[i+3]
            links.append(SpringDamperLink(sphere, down, length=100))
        except:
            pass

        try:
            if i % 3 > 0:
                downright = spheres[i+2]
                links.append(SpringDamperLink(sphere, downright, length=140))
        except:
            pass

        try:
            if (i+1) % 3 != 0:
                left = spheres[i+1]
                links.append(SpringDamperLink(sphere, left, length=100))
        except:
            pass

        try:
            if (i+1) % 3 != 0:
                downleft = spheres[i+4]
                links.append(SpringDamperLink(sphere, downleft, length=140))
        except:
            pass


    for sphere in spheres[-3:]:
        sphere.mass = 10.0
    
    t = 0
    dt = 0.1

    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()

    grid = SpatialHash()
    while not pygame.QUIT in [e.type for e in pygame.event.get()]:
        grid.update(spheres)

        for sphere in spheres:
            break
            for neighbour in grid.nearby_objects(sphere):
                if sphere.collides_with(neighbour):
                    sphere.resolve_collision(neighbour)

        for sphere in spheres:
            if sphere != stationary_sphere and sphere != stationary_sphere2 and sphere != stationary_sphere3:
                sphere.apply_force_to_com(sphere.mass * downward)

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
