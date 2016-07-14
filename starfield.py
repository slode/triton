import pygame as pg
import random

class Starfield(object):
    def __init__(self, rect):
        self.stars = []
        self.pos = (0,0)
        self.size = rect.size
        self.speed = 1
        self.color = (255,255,255, 255)
        self.backgroundcolor = pg.Color(0,0,0)
        for loop in range(100):
            self.stars.append([random.randrange(0, self.size[0] - 1),
                               random.randrange(0, self.size[1] - 1)])

    def draw(self, screen):
        for star in self.stars:
            p = (self.pos[0] + star[0], self.pos[1] + star[1])
            screen.set_at(p, self.color)

    def update(self):
        for star in self.stars:
            star[0] += self.speed
            if star[0] > self.size[0]:
                star[0] = 0
