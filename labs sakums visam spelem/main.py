import pygame as pg
import random
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((ekplat, ekgar))
        pg.display.set_caption(VARDS)
        self.cock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)

    def new(self):
        self.scorev = 0
        self.scorez = 0
        self.ilgums = ILGUMSS
        self.all_sprites = pg.sprite.Group()

        self.run()


    def run(self):
        #game loop
        self.playing = True
        while self.playing:
            self.cock.tick(FPS)
            self.ilgums -= 0.015
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        #BackGround = Background('beach1.png', [0,0])
        #zimet, ladet
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(round(self.ilgums)), 60, MELNS, ekplat / 2, 15)
        self.draw_text(str(self.scorev), 69, MELNS, ekplat /4, 15) ######################################################################################
        self.draw_text(str(self.scorez), 69, MELNS, ekplat - ekplat /4, 15)
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
#g.show_start_screen()
while g.running:
    g.new()
    #g.show_go_screen()
pg.quit()