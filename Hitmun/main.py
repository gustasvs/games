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
        self.MAPE = pg.image.load(os.path.join("pic", "MAPE.png")).convert()

    def new(self):
        self.scorev = 0
        self.scorez = 0
        self.ilgums = ILGUMSS
        self.kareivj_timer = 0
        self.all_sprites = pg.sprite.Group()
        self.kareivji = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.lietas = pg.sprite.Group()
        self.lodes = pg.sprite.Group()
        self.sienasr = pg.sprite.Group()
        self.sienasl = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.s2 = Siena(ekplat / 2 - 3, ekgar /3, 5, ekgar)
        self.s1 = Siena(ekplat / 2 + 3, ekgar /3, 5, ekgar)
        self.last_shot = 0
        self.ilgums = 0
        self.p1 = Platform(200, ekgar - 390, ekplat - 100, 5)
        #self.p2 = Platform(90, ekgar /2, ekplat / 2, 10)
        self.sienasr.add(self.s1)
        self.sienasl.add(self.s2)
        self.lietas.add(self.s1)
        self.lietas.add(self.s2)
        self.lietas.add(self.p1)
        self.all_sprites.add(self.s1)
        self.platforms.add(self.p1)
        #self.all_sprites.add(self.p1)
        #self.platforms.add(self.p2)
        self.all_sprites.add(self.s2)
        Kareivis(self)

        self.run()


    def run(self):
        #game loop
        self.playing = True
        while self.playing:
            self.cock.tick(FPS)
            self.ilgums += 0.015
            self.events()
            self.update()
            self.draw()

    def update(self):
        if self.player.vel.x <0:
            self.player.holdleft = True
        if self.player.vel.x >0:
            self.player.holdright = True
        self.all_sprites.update()
        self.player.GRAVITY = 0.5
        self.player.LECIENA_STIPRUMS = 10
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if self.player.vel.y > 0:
            self.player.pos.y -= 1
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.lecspeks = 1 # 2 JUMOPPPPPPPPPPPPPPPPPPP
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
            self.player.pos.y += 1
        if self.player.vel.y < 0:
            if hits:
                self.player.pos.y = hits[0].rect.bottom + spel_gar
                self.player.vel.y = 2
        hit_sienr = pg.sprite.spritecollide(self.player, self.sienasr, False)
        if hit_sienr:
            if self.player.holdleft == True:
                self.player.vel.x = 0
                self.player.pos.x = hit_sienr[0].rect.x + spel_plat / 2
                self.player.lecspeks = 0
                self.player.LECIENA_STIPRUMS /= 2
                if self.player.vel.y > 1: ## LENAAMA SLIIIID
                    self.player.vel.y = 1
        elif self.player.holdright == True:
            hit_sienl = pg.sprite.spritecollide(self.player, self.sienasl, False)
            if hit_sienl:
                self.player.vel.x = 0
                self.player.pos.x = hit_sienl[0].rect.x - spel_plat / 2
                self.player.lecspeks = 0
                self.player.LECIENA_STIPRUMS /= 2
                if self.player.vel.y > 1: ## LENAAMA SLIIIID
                    self.player.vel.y = 1
        hit_ene = pg.sprite.spritecollide(self.player, self.kareivji, False)
        if hit_ene:
            if hit_ene[0].acc.x < 0:
                if self.player.vel.x < 0:
                    hit_ene[0].kill()
                    self.player.dur = True
                elif self.player.vel.x >= 0:
                    self.player.vel.y -= 5 # nogalina mani
            if hit_ene[0].acc.x > 0:
                if self.player.vel.x <= 0:
                    self.player.vel.y -= 5 # nogalina mani
                elif self.player.vel.x > 0:
                    hit_ene[0].kill()
                    self.player.dur = True
        
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    self.player.jump()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_d:
                    self.player.holdright = True
                    self.player.holdleft = False
            if event.type == pg.KEYUP:
                if event.key == pg.K_d:
                    self.player.holdright = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    self.player.holdleft = True
                    self.player.holdright = False
            if event.type == pg.KEYUP:
                if event.key == pg.K_a:
                    self.player.holdleft = False
            if event.type == pg.MOUSEBUTTONDOWN:
                now = pg.time.get_ticks()
                if now - self.last_shot > BULLET_RATE:
                    self.last_shot = now
                    targ = pg.mouse.get_pos()
                    pos = self.player.pos + NO_KURIENES
                    Lode(self, pos, targ)

    def draw(self):
        self.screen.blit(self.MAPE, [0, 0])
        self.all_sprites.draw(self.screen)
        self.draw_text(str(round(self.ilgums)), 60, MELNS, ekplat / 2, 15)
        pg.display.flip()

    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
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
