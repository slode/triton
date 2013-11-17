import pygame
import random, math
from triton.vector2d import Vector2d
from triton.sphere import Sphere
from triton.spatial_hash import SpatialHash
from triton.spring_damper_link import SpringDamperLink

class Link(SpringDamperLink):
    def __init__(self, rb1, rb2, damping=0.3, spring=3.0, length=50):
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

    nodes = 5
    node_positions = [
            Vector2d(0.0, 0.0),
            Vector2d(0.0, 100.0),
            Vector2d(50.0, 50.0),
            Vector2d(100.0, 0.0),
            Vector2d(100.0, 100.0)
            ]

    for n in node_positions:
        n += Vector2d(400.0, 500.0)

    for y in range(0, nodes):
        pos = Vector2d(float(100.0*y), float(100.0*y))
        sphere = Sphere(
            mass = 1.0,
            radius = 1.0,
            pos = node_positions[y],
            damping = 0.1,
            elasticity = 0.97
            )

        spheres.append(sphere)
        sphere_col.append((int(sphere.x)%255,int(sphere.y)%255,int(sphere.radius)*255%255))

    # create body
    link_conf = [
            (0,1, 200),
            (0,2, 140),
            (0,3, 140),
            (1,2, 140),
            (2,4, 140),
            (2,3, 140),
            (3,4, 200)]

    def create_links(link_conf, spheres):
        links = []
        for a,b,l in link_conf:
            links.append(Link(spheres[a], spheres[b], length=l))
        return links

    links = create_links(link_conf, spheres)
    
    import copy
    def create_contact_point(sphere):
        c_sphere = copy.copy(sphere)
        c_sphere.mass = 1000.0
        c_sphere.pos += Vector2d(0.1, 0.1)
        return c_sphere

    t = 0
    dt = 0.1

    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()

    grid = SpatialHash()

    while not pygame.QUIT in [e.type for e in pygame.event.get()]:
        contact_force_links = []

        # actuate
        if t > 20:
            hind_leg = links[0]
            front_leg = links[5]
            front_leg._length = 200  + 30 * math.cos(t/15)
            hind_leg._length = 200  + 30 * math.cos((t+15)/15)

        grid.update(spheres)

        for sphere in spheres:
            if sphere.y > 650 and sphere.vel.y > 0:
                # counter_force = Vector2d(0.0, 100*(650 -sphere.y))
                #sphere.apply_force_to_com(counter_force)
                contact_force_links.append(Link(sphere, create_contact_point(sphere), 1))
            if sphere.x < 10:
                counter_force = Vector2d(100.0*(10.0-sphere.x), 0.0)
                sphere.apply_force_to_com(counter_force)
                contact_force_links.append(Link(sphere, create_contact_point(sphere), 1))
            if sphere.x > 790:
                counter_force = Vector2d(100.0*(790-sphere.x), 0.0)
                sphere.apply_force_to_com(counter_force)
                contact_force_links.append(Link(sphere, create_contact_point(sphere), 1))

        for sphere in spheres:
            sphere.apply_force_to_com(sphere.mass * downward)

        for link in contact_force_links:
            link.resolve()

        for link in links:
            link.resolve()


        screen.fill((255,245,225))
        for link in links:
            link.draw(screen)

        for n, sphere in enumerate(spheres):
            pygame.draw.circle(
                    screen, sphere_col[n], sphere.pos.tuple(), int(sphere.radius), 0)

        for sphere in spheres:#[width:]:
            sphere.update(t, dt)

        pygame.display.flip()
        t += dt


if __name__ == '__main__':
    main()
