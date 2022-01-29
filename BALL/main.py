import pygame as pg
import sys
from random import choice, random, randint
from os import path
from settings import *
from sprites import *
from tilemap import *

# HUD functions
def draw_player_mana(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 1000
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


class Game:
    def __init__(self):
        pg.init()
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.screen = pg.display.set_mode((ekplat, ekgar))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.FPS = FPS
        self.dalitaj = 1000.0

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        music_folder = path.join(game_folder, 'music')
        map_folder = path.join(game_folder, 'maps')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.map = TiledMap(path.join(map_folder, MAP_NAME))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.WaterBall_img = [pg.image.load(path.join(img_folder, "WaterBall1.png")).convert_alpha(), pg.image.load(path.join(img_folder, "WaterBall2.png")).convert_alpha()]
        self.Particle_img = [pg.image.load(path.join(img_folder, PARTICLE_IMG)).convert_alpha()]
        self.gun_flashes = []
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        # Sound loading


    def new(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.WaterBalls = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.particles = pg.sprite.Group()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'zombie':
                WaterBall(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name in ['health']:
                Item(self, obj_center, tile_object.name)
            if tile_object.name == 'spawner':
                self.spawnerx = obj_center.x
                self.spawnery = obj_center.y
            if tile_object.name == 'spawner1':
                self.spawnerx1 = obj_center.x
                self.spawnery1 = obj_center.y
            if tile_object.name == 'boom':
                Item(self, obj_center, tile_object.name)
            if tile_object.name == 'bazee':
                Item(self, obj_center, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(self.FPS) / self.dalitaj  # fix for Python 2.x
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        if self.player.mana < 0:
            self.player.slowmo = False
            self.dalitaj = 1000.0
        if self.player.slowmo == True:
            self.player.mana -= 1
        if self.player.slowmo == False:
            if self.player.mana < PLAYER_MANA:
                self.player.mana += ADD_MANA_SPEED
        if len(self.WaterBalls) < 50:
            if randint(1, 10) == 1:
                choice([WaterBall(self, self.spawnerx, self.spawnery), WaterBall(self, self.spawnerx1, self.spawnery1)])
               
        Particle(self, self.player.pos.x, self.player.pos.y)
        self.all_sprites.update()
        self.camera.update(self.player)
        # players piesk irtem
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'boom':
                hit.kill()
                for e in self.WaterBalls:
                    dist = hypot(hits[0].pos.x - e.pos.x, hits[0].pos.y - e.pos.y)
                    if dist < 250:
                        e.kill()
                #MuzzleFlash(self, hits[0].pos)
            if hit.type == 'baze':
                for e in self.WaterBalls:
                    e.kill()
                    # end screen
        hits = pg.sprite.spritecollide(self.player, self.WaterBalls, False, pg.sprite.collide_mask)
        for hit in hits:
            self.player.add_mana(ADD_MANA)
            self.playing = False



    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply(self.map))
        # self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if sprite not in self.particles:
                if self.draw_debug:
                    pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)

        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        # HUD functions
        draw_player_mana(self.screen, ekplat / 2 - 500, 20, self.player.mana / PLAYER_MANA)
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("PAUZE", self.title_font, 105, RED, ekplat / 2, ekgar / 2, align="center")
        pg.display.flip()

    def events(self):
        # catch all events here
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
                    self.player.slowmo = True
                    self.dalitaj = 5000.0
            if event.type == pg.KEYUP:
                if event.key == pg.K_LSHIFT:
                    self.player.slowmo = False
                    self.dalitaj = 1000.0

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
