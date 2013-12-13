import pygame
import random, math
from triton.vector2d import Vector2d
from triton.sphere import Sphere
from triton.rectangle import Rectangle
from triton.spatial_hash import SpatialHash

class Ship(Rectangle):
    def __init__(self):
        pos = Vector2d(400.0, 400.0)
        vel = Vector2d(.0, .0)
        super(Ship, self).__init__(
            mass=1.0,
            pos=pos,
            vel=vel,
            dtheta=0., #05 * 180 / math.pi,
            damping=0.00,
            elasticity=0.97,
            dimensions=Vector2d(100,40))

        self.surface = pygame.Surface(self.dimensions.tuple())

        dim = self.dimensions
        rect_tuple = (5, 5, dim.x-10, dim.y-10)
        self.surface.fill((0,100,0))
        pygame.draw.rect(self.surface, (255,0,0), rect_tuple, 0)

    def draw(self, screen):
        tmp_surface = self.surface.copy()
        tmp_surface = pygame.transform.rotate(tmp_surface, self.theta)
        r = tmp_surface.get_rect(center = self.pos.tuple())
        screen.blit(tmp_surface, r.topleft)
        
class Ball(Sphere):
    def __init__(self):
        super(Ball, self).__init__(
            radius=3,
            mass=1.0,
            pos=Vector2d(425.0, 425.0),
            vel=Vector2d(0.0, -10.0),
            damping=0.00,
            elasticity=0.97)

    def draw(self, screen):
        pygame.draw.circle(
            screen, (255, 0, 0), self.pos.tuple(), self.radius, 0) 
        


def main():
    ship = Ship()
    ball = Ball()
    t = 0
    dt = 0.1

    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()

    while not pygame.QUIT in [e.type for e in pygame.event.get()]:
        screen.fill((255,245,225))

        ship.draw(screen)
        ball.draw(screen)

        if ship.collides_with(ball):
            ship.resolve_collision(ball)

        ship.update(t, dt)
        ball.update(t, dt)

        pygame.display.flip()
        clock.tick(50)
        t += dt


if __name__ == '__main__':
    main()
