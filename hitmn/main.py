import pygame as pg
import random
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((ekplat, ekgar))
        pg.display.set_caption(VARDS)
        pg.key.set_repeat(1, 10)
        self.cock = pg.time.Clock()
        self.font_name = pg.font.match_font(FONT_NAME)
        self.level = 0 
        self.draw_debug = False
        self.dalitaj = 1000.0

    def new(self):
        self.level += 1
        self.paused = False
        self.score = 0
        self.load_data()
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.ai = pg.sprite.Group()
        self.finish = pg.sprite.Group()
        self.lodes = pg.sprite.Group()
        self.camera = Camera(self.map.width, self.map.height)

        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            
            if tile_object.name == 'pointman':
                if tile_object.type == 'up':
                    Pointman(self, obj_center.x, obj_center.y, 1)
                elif tile_object.type == 'down':
                    Pointman(self, obj_center.x, obj_center.y, 2)
                elif tile_object.type == 'left':
                    Pointman(self, obj_center.x, obj_center.y, 3)
                else:
                    Pointman(self, obj_center.x, obj_center.y, 4)
            
            if tile_object.name == 'gunman':
                if tile_object.type == 'up':
                    Gunman(self, obj_center.x, obj_center.y, 1)
                elif tile_object.type == 'down':
                    Gunman(self, obj_center.x, obj_center.y, 2)
                elif tile_object.type == 'left':
                    Gunman(self, obj_center.x, obj_center.y, 3)
                else:
                    Gunman(self, obj_center.x, obj_center.y, 4)
            
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            
            if tile_object.name == 'finish':
                Finish(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)

        self.run()

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'img')
        self.music_folder = path.join(self.game_folder, 'music')
        self.map_folder = path.join(self.game_folder, 'maps')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.map_namee = "Lvl" + str(self.level) + ".tmx"
        self.map = Map(path.join(self.map_folder, self.map_namee))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        self.Player_img = pg.image.load(path.join(self.img_folder, Player_img)).convert_alpha()
        self.Lode_img = pg.image.load(path.join(self.img_folder, lodes_IMG)).convert_alpha()
        self.Naza_img = pg.image.load(path.join(self.img_folder, Naza_IMG)).convert_alpha()
    
    def run(self):
        self.playing = True
        while self.playing:
            
            self.dt = self.cock.tick(FPS) / self.dalitaj
            
            #self.ilgums -= 0.015
            self.events()
            if not self.paused:
                self.update()
            self.draw()
    
    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        

    def events(self):
        eve = pg.event.poll()
        if eve.type == pg.QUIT:
            self.quit()
        if eve.type == pg.MOUSEBUTTONDOWN and eve.button == MOUSE_LEFT:
            x, y = pg.mouse.get_pos()
            if self.player.can_move_to(x, y) and self.paused == False and self.player.can_tp:
                #self.player.pos = vec(x + abs(self.camera.x), y + abs(self.camera.y))
                self.player.mana -= PLAYER_MANA // 4    
                self.player.pos = vec(x, y)
                self.player.vel = vec(0, 0)
        if eve.type == pg.MOUSEBUTTONDOWN and eve.button == MOUSE_RIGHT:
            self.player.dur()
        if eve.type == pg.KEYDOWN:
            if eve.key == pg.K_w:
                self.paused = True
        if eve.type == pg.KEYDOWN:
            if eve.key == pg.K_s:
                self.paused = False

    def draw_grid(self):
        for x in range(0, ekplat, Tilesize):
            pg.draw.line(self.screen, (100, 100 ,100), (x, 0), (x, ekgar))
        for y in range(0, ekgar, Tilesize):
            pg.draw.line(self.screen, (100, 100, 100), (0, y), (ekplat, y))
    
    def draw_player_mana(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 200
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
        pg.draw.rect(surf, BALTS, outline_rect, 2)

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.cock.get_fps()))

        self.screen.blit(self.map_img, self.camera.apply(self.map))
        #self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)

        self.draw_player_mana(self.screen, 50, 50, self.player.mana / PLAYER_MANA)
        self.draw_text(str(self.score), 50, BALTS, ekplat - 100, 50)

        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", 105, BALTS, ekplat / 2, ekgar / 2)
        
        #self.draw_text(str(round(self.ilgums)), 60, MELNS, ekplat / 2, 15)
        #self.draw_text(str(self.scorev), 69, MELNS, ekplat /4, 15) ######################################################################################
        pg.display.flip()

    def show_start_screen(self):
        self.screen.fill(LIGHTBLUE)
        self.draw_text("Made by gustasvs", 48, BALTS, ekplat /2, ekgar - 400)
        self.draw_text("Teleporting hitmn", 22, BALTS, ekplat / 2, ekgar - 600)
        self.draw_text("Spied ENTER lai speletu", 22, BALTS, ekplat / 2, ekgar - 200)
        pg.display.flip()
        self.w84key()
        
    def show_go_screen(self):
        self.screen.fill(BALTS)
        self.draw_text("You won with {} score.".format(self.score), 48, MELNS, ekplat /2, ekgar - 400)
        self.draw_text("KGbraki rulle YEEEHOOOOOOOO(Subscribe to gustasvs and kiksmas)", 22, MELNS, ekplat / 2, ekgar - 600)
        self.draw_text("Press anything 3 taims to play next lvl", 22, MELNS, ekplat / 2, ekgar - 200)
        pg.display.flip()
        self.w84key()
        self.new()
    
    def w84key(self):
        waiting = True
        while waiting == True:
            self.cock.tick(FPS)
            for eve in pg.event.get():
                if eve.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if eve.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def quit(self):
        pg.quit()
        sys.exit()

g = Game()
#g.show_start_screen()
while True:
    g.new()
    g.show_go_screen()
pg.quit()
