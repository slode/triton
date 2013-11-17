import pygame
import random, math
from triton.vector2d import Vector2d
from triton.shape import Sphere
from triton.spatial_hash import SpatialHash
from triton.spring_damper_link import SpringDamperLink

class Link(SpringDamperLink):
    def __init__(self, rb1, rb2, damping=.3, spring=1.8, length=70):
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
    downward = Vector2d(0.0, 9.81)

    for i in range(15):
        pos = Vector2d(300.0 + random.random()*100.0, random.random()*100.0)
        sphere = Sphere(
            mass = 0.1,
            radius = 4.0,
            pos = pos,
            damping = 0.07,
            elasticity = 0.97
            )

        spheres.append(sphere)
        sphere_col.append((int(sphere.x)%255,int(sphere.y)%255,int(sphere.radius)*255%255))

    def pyramid_level(value):
        return int(math.ceil((-1.0 + math.sqrt(1.0 + 8.0 * value)) / 2.0))

    links = []
    import math
    for i, sphere in enumerate(spheres):
        level = pyramid_level(i+1)
        try:
            links.append(Link(sphere, spheres[i + level]))
            links.append(Link(sphere, spheres[i + level + 1]))
            links.append(Link(spheres[i + level], spheres[i + level + 1]))
            spheres[i+level].pos = sphere.pos + Vector2d(-70.0, 70.0)
            spheres[i+level+1].pos = sphere.pos + Vector2d(70.0, 70.0)
        except:
            pass

    t = 0
    dt = 0.1

    screen_mode = Vector2d(800.0, 800.0)
    screen = pygame.display.set_mode(screen_mode.tuple())
    clock = pygame.time.Clock()
    mouse_sphere = Sphere(
        mass = 1.0,
        radius = 80.0,
        damping = 0.0,
        elasticity = 0.97
        )
    sphere_col.append((250,100,100))
    pressed = False

    grid = SpatialHash(map_size=screen_mode, grid_size=20)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pressed = True
                pos = pygame.mouse.get_pos()
                mouse_sphere.pos = Vector2d(pos[0], pos[1])
                spheres.append(mouse_sphere)
            elif event.type == pygame.MOUSEBUTTONUP:
                spheres.remove(mouse_sphere)
                pressed = False

        if pressed:
            pos = pygame.mouse.get_pos()
            mouse_sphere.pos = Vector2d(pos[0], pos[1])


        grid.update(spheres)
        for sphere in spheres:
            for neighbour in grid.nearby_objects(sphere):
                if sphere.collides_with(neighbour):
                    sphere.resolve_collision(neighbour)

        for sphere in spheres:
            if sphere.y > 650 and sphere.vel.y > 0:
                counter_force = Vector2d(0.0, 10*(650 -sphere.y))
                sphere.apply_force_to_com(counter_force)
            if sphere.x < 10 and sphere.x < 0:
                counter_force = Vector2d(10.0*(10.0-sphere.x), 0.0)
                sphere.apply_force_to_com(counter_force)
            if sphere.x > 790 and sphere.x > 0:
                counter_force = Vector2d(10.0*(790-sphere.x), 0.0)
                sphere.apply_force_to_com(counter_force)


        for sphere in spheres:
            sphere.apply_force_to_com(1.0 * sphere.mass * downward)

        for link in links:
            link.resolve()

        screen.fill((255,245,225))

        pygame.draw.aaline(screen, (0, 0, 0), (0, 650), (800, 650))

        for link in links:
            link.draw(screen)

        for n, sphere in enumerate(spheres):
            try:
                pygame.draw.circle(
                        screen, sphere_col[n], sphere.pos.tuple(), int(sphere.radius), 0)
            except:
                pass

        for sphere in spheres:
            sphere.update(t, dt)

        pygame.display.flip()
        t += dt


if __name__ == '__main__':
    main()
