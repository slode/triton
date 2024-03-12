# Copyright (c) 2013 Stian Lode
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import pygame
import math
import random
from triton.vector2d import Vector2d
from triton.sphere import Sphere
from triton.spatial_hash import SpatialHash


class Obstacle:
    def __init__(self, pos):
        self.pos = pos
        self.color = (255, 0, 0)
        self.radius = 40
        self.divert_radius = 80

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos.tuple(), self.radius, 3)
        pygame.draw.circle(screen, (0, 255, 0), self.pos.tuple(), self.divert_radius, 1)


class Triangle(Sphere):
    def __init__(self, pos, vel=Vector2d(0.01, 0.0)):
        super(Triangle, self).__init__(
            mass=1.0, radius=30, pos=pos, vel=vel, damping=0.0, elasticity=1.0
        )
        self.direction = vel

        self.color = (155, 50, 50)

    def get_direction(self):
        if self.vel.length_sq() > 0:
            self.direction = self.vel
        return self.direction

    def draw(self, screen):
        polygon = []
        forward = self.get_direction().normalize()
        polygon.append(self.pos + forward * 10)
        polygon.append(self.pos + (forward.rotate(3 * math.pi / 4) * 10))
        polygon.append(self.pos + (forward.rotate(5 * math.pi / 4) * 10))
        pygame.draw.aalines(screen, self.color, True, polygon)


#        pygame.draw.circle(screen, self.color, self.pos.tuple(), self.radius, 1)


def main():

    obstacles = []
    obstacles.append(Obstacle(Vector2d(200.0, 200.0)))
    obstacles.append(Obstacle(Vector2d(400.0, 200.0)))
    obstacles.append(Obstacle(Vector2d(400.0, 400.0)))
    obstacles.append(Obstacle(Vector2d(200.0, 400.0)))

    ships = []
    for i in range(20):
        pos = Vector2d(random.random() * 800.0, random.random() * 800.0)
        ships.append(Triangle(pos))

    t = 0
    dt = 0.1

    screen_mode = Vector2d(1000.0, 600.0)
    screen = pygame.display.set_mode(screen_mode.tuple())

    def calc_repulsive_force(this_ship, other):
        d = this_ship.pos - other.pos
        # f = d.normalize()
        # this_ship.apply_force_to_com(f * 3.0)
        this_ship.apply_force_to_com(d * 0.1)

    def calc_wall_force(ship):
        wall_force = 50
        distance = 30
        if ship.x < distance:
            ship.apply_force_to_com(Vector2d(wall_force, 0.0))
        elif ship.x > (screen_mode.x - distance):
            ship.apply_force_to_com(Vector2d(-wall_force, 0.0))
        if ship.y < distance:
            ship.apply_force_to_com(Vector2d(0.0, wall_force))
        elif ship.y > (screen_mode.y - distance):
            ship.apply_force_to_com(Vector2d(0.0, -wall_force))

    def calc_obstacle_force(ship, obstacles):
        for o in obstacles:
            d = ship.pos - o.pos
            len_d = d.length()
            if len_d < o.divert_radius:
                distance_to_wall = max(len_d - o.radius, 0.1)
                ship.apply_force_to_com(d.normalize() * 10.0 / distance_to_wall)

    def calc_resistance(this_ship):
        ship.apply_force_to_com(-ship.vel.normalize() * ship.vel.length_sq() * 0.01)

    def do_flock(this_ship, ships):
        if not ships:
            return
        avg_vel = Vector2d(0.0, 0.0)
        avg_pos = Vector2d(0.0, 0.0)
        for ship in ships:
            avg_vel += ship.vel
            avg_pos += ship.pos
        nships = len(ships)
        avg_vel /= nships
        avg_pos /= nships
        this_ship.apply_force_to_com(avg_vel)
        this_ship.apply_force_to_com(avg_pos - this_ship.pos)

    grid = SpatialHash(map_size=screen_mode, grid_size=20)
    while pygame.QUIT not in [e.type for e in pygame.event.get()]:
        grid.update(ships)

        for ship in ships:
            nearby_ships = []
            for neighbour in grid.nearby_objects(ship):
                if ship.collides_with(neighbour):
                    nearby_ships.append(neighbour)
                    calc_repulsive_force(ship, neighbour)
            do_flock(ship, nearby_ships)
            calc_wall_force(ship)
            calc_obstacle_force(ship, obstacles)
            calc_resistance(ship)

        screen.fill((255, 245, 225))
        for ship in ships:
            ship.draw(screen)

        for obstacle in obstacles:
            obstacle.draw(screen)

        for ship in ships:
            ship.update(t, dt)

        pygame.display.flip()
        t += dt


if __name__ == "__main__":
    main()
