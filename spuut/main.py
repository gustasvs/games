import pygame as pg
import sys
from random import choice, random, randint
from os import path
from settings import *
from sprites import *
from tilemap import *


class Game:
    def __init__(self):
        pg.init()
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.screen = pg.display.set_mode((ekplat, ekgar))
        pg.display.set_caption(TITLE)
        self.font_name = pg.font.match_font(FONT_NAME)
        self.clock = pg.time.Clock()
        self.load_data()
        self.FPS = FPS
        self.dalitaj = 1000.0

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

    def new(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.particles = pg.sprite.Group()
        self.main_particles = pg.sprite.Group()
        self.player = Player(self, ekplat / 2, ekgar / 2)
        self.draw_debug = False
        self.paused = False

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(self.FPS) / self.dalitaj
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def createObstacle(self, x, y, w, h):
        # for xx in range(w):
        #     for yy in range(h):
        #         Obstacle(self, x + xx, y + yy, 1, 1)
        Obstacle(self, x, y, w, h)

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        print(len(self.particles))
        self.all_sprites.update()
        if self.player.mana < 0:
            self.player.gas = False
        if self.player.gas == True:
            self.player.mana -= 1
        if self.player.gas == False:
            if self.player.mana < PLAYER_MANA:
                self.player.mana += ADD_MANA_SPEED

        # if self.player.pos.x > ekplat - ekplat / 6:
        #     for obs in self.walls:
        #         obs.rect.x -= self.player.vel.x
        #     for part in self.main_particles:
        #         part.pos.x -= self.player.vel.x
        #     self.player.pos.x -= self.player.vel.x
        #     self.player.atNoCentra.x -= self.player.vel.x
        # if self.player.pos.x < ekplat / 6:
        #     for obs in self.walls:
        #         obs.rect.x -= self.player.vel.x
        #     for part in self.main_particles:
        #         part.pos.x -= self.player.vel.x
        #     self.player.pos.x -= self.player.vel.x
        #     self.player.atNoCentra.x -= self.player.vel.x
        # if self.player.pos.y > ekgar - ekgar / 6:
        #     for obs in self.walls:
        #         obs.rect.y -= self.player.vel.y
        #     for part in self.main_particles:
        #         part.pos.y -= self.player.vel.y
        #     self.player.pos.y -= self.player.vel.y
        #     self.player.atNoCentra.y -= self.player.vel.y
        if self.player.pos.y < ekgar / 4:
            self.player.pos.y -= self.player.vel.y
            for obs in self.walls:
                obs.rect.y += abs(self.player.vel.y)
                if obs.rect.top >= ekgar:
                    obs.kill()
            for part in self.main_particles:
                part.pos.y -= self.player.vel.y
        while len(self.walls) < 10:
            width = randint(5, 100)
            height = randint(5, 100)
            pposx = round(self.player.pos.x)
            pposy = round(self.player.pos.y)
            x = randint(0, ekplat - width)
            y = randint(-1000, -30)
            self.createObstacle(x, y, width, height)
    # HUD
    def draw_player_mana(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        if pct > 1:
            pct = 1
        BAR_LENGTH = ekplat
        BAR_HEIGHT = 20
        fill = pct * BAR_LENGTH
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
        col = (255 * (1 - pct), 255 * pct, 0)
        pg.draw.rect(surf, col, fill_rect)
        #pg.draw.rect(surf, WHITE, outline_rect, 2)
    
    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        if self.draw_debug:
            for sprite in self.all_sprites:
                if sprite not in self.particles:
                    pg.draw.rect(self.screen, CYAN, (sprite.hit_rect), 1)
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, wall.rect, 1)

        # HUD functions
        self.draw_player_mana(self.screen, 0, 20, self.player.mana / PLAYER_MANA)
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", 105, WHITE, ekplat / 2, ekgar / 2)
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    self.paused = not self.paused
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LSHIFT:
                    self.player.gas = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_LSHIFT:
                    self.player.gas = False

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
