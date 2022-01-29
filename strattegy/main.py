import pygame as pg
import random
from os import path
from settings import *
from sprites import *
from tilemap import *

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((ekplat, ekgar))
        pg.display.set_caption(VARDS)
        pg.key.set_repeat(1, 10)
        self.cock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()
        self.saak = False

    def new(self):
        #self.scorev = 0
        #self.scorez = 0
        #self.ilgums = ILGUMSS
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.barbs = pg.sprite.Group()
        self.barbs1 = pg.sprite.Group()
        self.kreisie = pg.sprite.Group()
        self.labie = pg.sprite.Group()
        self.bultas = pg.sprite.Group()
        self.bultas1 = pg.sprite.Group()
        
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                i = 2
                if tile == '1':
                    Wall(self, col, row)
                
                if tile == "B":
                    Barb1(self, col, row)
                if tile == "b":
                    i += 1
                if tile == "N":
                    Bonds(self, col, row)
                if tile == "n":
                    Bonds1(self, col, row)


        self.run()


    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.map = Map(path.join(game_folder, 'map.txt'))
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (Tilesize, Tilesize))
        self.barb_img = pg.image.load(path.join(img_folder, barb_img)).convert_alpha()
        self.barb1_img = pg.image.load(path.join(img_folder, barb1_img)).convert_alpha()
        self.bond_img = pg.image.load(path.join(img_folder, bondi_img)).convert_alpha()
        self.bond1_img = pg.image.load(path.join(img_folder, bondi1_img)).convert_alpha()
        self.bulta_img = pg.image.load(path.join(img_folder, BULTAS_IMG)).convert_alpha()
    def run(self):
        #game loop
        self.playing = True
        while self.playing:
            
            self.dt = self.cock.tick(FPS) / 1000
            
            #self.ilgums -= 0.015
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        
        #hits1 = pg.sprite.groupcollide(self.labie, self.bultas, False, True)
        #for hit in hits1:
            #hit.kill()

            #self.barbs.rot = (mob_hits[0]- .pos).angle_to(vec(1, 0))
        #print(self.kreisie)

    def events(self):
        # Game Loop - events
        for eve in pg.event.get():
            # check for closing window
            if eve.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if eve.type == pg.MOUSEBUTTONDOWN:
                x, y =pg.mouse.get_pos()
                #if x > ekplat / 2:
                Barb(self,x/Tilesize, y/Tilesize)
            if eve.type == pg.KEYDOWN:
                if eve.key == pg.K_w:
                    self.saak = True
            if eve.type == pg.KEYDOWN:
                if eve.key == pg.K_s:
                    self.saak = False
            '''if eve.type == pg.KEYDOWN:
                if eve.key == pg.K_a:
                    self.player.move(dx=-1)
            if eve.type == pg.KEYDOWN:
                if eve.key == pg.K_d:
                    self.player.move(dx=1)
            if eve.type == pg.KEYDOWN:
                    if eve.key == pg.K_w:
                        self.player.move(dy=-1)
            if eve.type == pg.KEYDOWN:
                    if eve.key == pg.K_s:
                        self.player.move(dy=1) '''
    def draw_grid(self):
        for x in range(0, ekplat, Tilesize):
            pg.draw.line(self.screen, (100, 100 ,100), (x, 0), (x, ekgar))
        for y in range(0, ekgar, Tilesize):
            pg.draw.line(self.screen, (100, 100, 100), (0, y), (ekplat, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.cock.get_fps()))
        #BackGround = Background('beach1.png', [0,0])
        #zimet, ladet
        self.screen.fill(BGCOLOR)
        #self.draw_grid()#######################################################################
        self.all_sprites.draw(self.screen)
        #self.draw_text(str(round(self.ilgums)), 60, MELNS, ekplat / 2, 15)
        #self.draw_text(str(self.scorev), 69, MELNS, ekplat /4, 15) ######################################################################################
        #self.draw_text(str(self.scorez), 69, MELNS, ekplat - ekplat /4, 15)
        pg.display.flip()

    def show_start_screen(self):
        self.screen.fill(LIGHTBLUE)
        self.draw_text(TITLE, 48, BALTS, ekplat /2, ekgar - 400)
        self.draw_text("4 player spele :D(var ari 3 vai 2)", 22, BALTS, ekplat / 2, ekgar - 600)
        self.draw_text("SPIED jebko... 8==D lai speletu ;)", 22, BALTS, ekplat / 2, ekgar - 200)
        pg.display.flip()
        self.w84key()
        
    def show_go_scren(self):
        self.screen.fill(BALTS)
        self.draw_text("GG es uzvareju", 48, MELNS, ekplat /2, ekgar - 400)
        self.draw_text("LOL pauls smird :)", 22, MELNS, ekplat / 2, ekgar - 600)
        self.draw_text("KGbraki rulle YEEEHOOOOOOOO(Subscribe to gustasvs and kiksmas)", 22, MELNS, ekplat / 2, ekgar - 200)
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
                    self.running = False
                if eve.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()
pg.quit()