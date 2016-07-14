from gamestate import Game, GameState
from triton.vector2d import Vector2d
from triton.sphere import Sphere
from starfield import Starfield

import pygame as pg
import pygame.gfxdraw
import sys

        
class Planet(Sphere):
    mutable = True
    color = pg.Color("Yellow")

    def calc_gravity(self, ent2):
        """Returns a force vector from one body to another"""
        gravitational_const = 2.0
        diff = (ent2.pos-self.pos)
        dist = diff.length_sq()
        force = gravitational_const * self._mass * ent2._mass / dist
        return diff.normalize() * force

class SplashScreen(GameState):
    def __init__(self):
        super(SplashScreen, self).__init__()
        self.title = self.font.render("Planet Golf", True, pg.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.next_state = "GAMEPLAY"
        self.starfield = Starfield(self.screen_rect)
        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_RETURN:
                self.done = True
            elif event.key == pg.K_ESCAPE:
                self.quit = True
    
    def update(self, dt):
        self.starfield.update()
        self.persist['level'] = "planets.txt"

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        surface.blit(self.title, self.title_rect)        
        self.starfield.draw(surface)


class FinishScreen(GameState):
    def __init__(self):
        super(FinishScreen, self).__init__()
        self.next_state = "GAMEPLAY"
        self.starfield = Starfield(self.screen_rect)
        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_RETURN:
                self.done = True
            elif event.key == pg.K_ESCAPE:
                self.next_state = "SPLASH"
                self.done = True
    
    def startup(self, persistent):
        self.persist = {}
        self.persist['level'] = persistent['level']
        self.success = persistent['success']
        self.score = float(persistent['score'])
        self.rank = 0
        self.highscores = []

        if self.success:
            for line in open("highscore_" + self.persist['level'], "r+").readlines():
                self.highscores.append(float(line))
            import bisect
            self.rank = bisect.bisect_left(self.highscores, self.score)
            self.highscores.insert(rank, self.score)
            with open("highscore_" + self.persist['level'], "r+") as f:
                for score in self.highscores:
                    f.write("{0}\n".format(score))


    def update(self, dt):
        self.starfield.update()

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        self.starfield.draw(surface)

        if self.success:
            title = self.font.render(
                    "Success! You scored {0} points!\nRank {1}.".format(self.score, self.rank),
                    True, pg.Color("dodgerblue"))
            title_rect = title.get_rect(center=self.screen_rect.center)
            surface.blit(title, title_rect)
        else:
            title = self.font.render(
                    "You failed! Press 'return' to restart.",
                    True, pg.Color("dodgerblue"))
            title_rect = title.get_rect(center=self.screen_rect.center)
            surface.blit(title, title_rect)
    
class Gameplay(GameState):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.initial_velocity = None
        self.entities = []
        self.started = False
        self.paused = False
        self.starfield = Starfield(self.screen_rect)
        self.show_cursor = False
        self.time = 0.0
        self.next_state = "FINISHED"
        
    def startup(self, persistent):
        self.persist = persistent
        self.persist['success'] = False
        self.persist['score'] = 0
        self.entities = []
        self.started = False
        self.paused = False
        self.starfield = Starfield(self.screen_rect)
        self.show_cursor = False
        self.time = 0.0

        # Load level
        for line in open(self.persist['level']).readlines():
            mass, size, pos, vel, mutable  = line.split(":")
            pos = pos.split(",")
            vel = vel.split(",")
            mutable = mutable.startswith('1')

            entity = Planet(
                    float(size),
                    mass=float(mass), 
                    pos=Vector2d(float(pos[0]), float(pos[1])),
                    vel=Vector2d(float(vel[0]), float(vel[1])),
                    elasticity = 0.97,)
            entity.mutable = mutable
            self.entities.append(entity)
        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.started = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_p:
                self.paused = not self.paused
            elif event.key == pg.K_ESCAPE:
                self.done = True
        
    def update(self, dt):
        dt /= 100.0
        if not self.started:
            p = pg.mouse.get_pos()
            self.cursor = Vector2d([float(i) for i in p])
            player = self.entities[0].pos
            diff = self.cursor - player
            if diff < 100:
                self.show_cursor = True
                diff /= 50
                self.initial_velocity = diff
                self.entities[0].vel = Vector2d(
                        float(diff[0]),
                        float(diff[1]))
            else:
                self.show_cursor = False
        elif not self.paused:
            self.time += dt
            entity_set = list(self.entities)
            # Success condition
            if self.entities[0].collides_with(self.entities[-1]):
                self.persist['init_vel'] = self.initial_velocity
                self.persist['success'] = True
                self.persist['score'] = self.time
                self.done = True
                return

            for entity in entity_set:
                entity_set.remove(entity)
                for other in entity_set:
                    if entity.collides_with(other):
                        entity.resolve_collision(other)

                    force = entity.calc_gravity(other)
                    entity.apply_force(entity.pos, force)
                    other.apply_force(other.pos, -force)

            for entity in self.entities:
                if entity.mutable == True:
                    entity.update(0, dt)

            self.starfield.update()
        else:
            pass
                 

    def draw(self, surface):
        surface.fill(pg.Color("Black"))
        self.starfield.draw(screen)
        if not self.started and self.show_cursor:
            pg.draw.aaline(
                    surface,
                    pg.Color("dodgerblue"),
                    self.entities[0].pos,
                    self.cursor)

        for entity in self.entities:
            pg.gfxdraw.aacircle(
                surface,
                int(entity.pos[0]),
                int(entity.pos[1]),
                int(entity.radius),
                (220,250,100))

            pg.gfxdraw.filled_circle(
                surface,
                int(entity.pos[0]),
                int(entity.pos[1]),
                int(entity.radius),
                (220,250,100))
        

        label = self.font.render(str(self.initial_velocity), True, pg.Color("dodgerblue"))
        surface.blit(label, (10, 40))

        label = self.font.render(str(self.time), True, pg.Color("dodgerblue"))
        surface.blit(label, (10, 80))

        if not self.started:
            text = "Use mouse to launch satellite."
            title = self.font.render(text, True, pg.Color("dodgerblue"))
            title_rect = title.get_rect(center=self.screen_rect.center)
            surface.blit(title, title_rect)

        elif self.paused:
            title = self.font.render("PAUSED", True, pg.Color("dodgerblue"))
            title_rect = title.get_rect(center=self.screen_rect.center)
            surface.blit(title, title_rect)

    
if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((1280, 720))
    states = {
            "SPLASH": SplashScreen(),
            "GAMEPLAY": Gameplay(),
            "FINISHED": FinishScreen()}
    game = Game(screen, states, "SPLASH")
    game.run()
    pg.quit()
    sys.exit()
