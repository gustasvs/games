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
        self.scorev = 1
        self.dir = 0
        self.ilgum = 0.015
        self.i = 0
        self.money = 0
        self.level = 1
        self.MOBU_DAUDZUMS = MOBU_DAUDZUMS
        self.LODES_ATSITIENS = 5
        self.ilgums = ILGUMSS
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.platforms1 = pg.sprite.Group()
        self.lodes = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.player = Player(self)
        self.paused = False
        self.mob_timer = 0
        #self.p2 = Platform(0, ekgar * 0.75, ekplat /2, 10)
        self.p1 = Platform(90, ekgar - 170, ekplat - 180, 180)
        self.p2 = Platform(90, ekgar - 170, ekplat - 180, 10)
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.lodes)
        self.all_sprites.add(self.mobs)
        self.platforms.add(self.p1)
        self.platforms1.add(self.p2)
#        self.platforms.add(self.p2)
        self.all_sprites.add(self.p1)
        self.all_sprites.add(self.p2)
#        self.all_sprites.add(self.p2)

        self.run()


    def run(self):
        #game loop
        self.playing = True
        while self.playing:
            #print(self.player.pos.y, ekgar - 170)
            self.cock.tick(FPS)
            self.ilgums -= self.ilgum
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        #for e in self.lodes:
        if self.ilgums < 0:
            self.paused = True
            self.level += 1
            self.ilgum = 0
            self.player.vel.x = 0
            self.player.vel.y = 0
            if self.MOBU_DAUDZUMS > 100:
                self.MOBU_DAUDZUMS -= 100
            for e in self.mobs:
                e.kill()
            for e in self.lodes:
                e.kill()
        if self.paused == False:
            self.money += 0.1
        self.all_sprites.update()
        if self.scorev <= 0:
            self.show_go_scren()


        # mobi spawn

        now = pg.time.get_ticks()
        if now - self.mob_timer > self.MOBU_DAUDZUMS + random.choice([-500,-333, 0, 333, 500]):
            self.mob_timer = now
            self.i = 1
            
            Enemy(self, self.i, self.LODES_ATSITIENS)
        if self.player.pos.y >= ekgar - 170:
            
            hits = pg.sprite.spritecollide(self.player, self.platforms1, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
        if self.player.pos.y > 2000:
            self.scorev -= 1
            self.player.pos.y = ekgar - 600
            self.player.pos.x = random.randint(ekplat / 2, ekplat - 60)
            self.player.vel.y = 0
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        if mob_hits:
            if mob_hits[0].vel.x < 0:
                self.player.vel.x -= 30
            if mob_hits[0].vel.x >= 0:
                self.player.vel.x += 30
                #mob_hits[0].kill()
            #self.scorev -=1
            #self.player.center = (ekplat /2 , 0)
            #self.player.pos = vec(ekplat /4 , 0)
            #self.player.vel = vec(0, 0)
            #self.player.acc = vec(0, 0)
    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            #if event.type == pg.KEYDOWN:
                #if event.key == pg.K_w:
                    #self.player.jump()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if self.paused == True:
                        self.paused = False
                        self.ilgums = ILGUMSS
                        self.ilgum = 0.015
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFTBRACKET:
                    if self.paused == True:
                        if self.money > 20:
                            self.LODES_ATSITIENS += 1
                            
                            self.money-= 20
                if event.key == pg.K_RIGHTBRACKET:
                    if self.paused == True:
                        if self.money > 20:
                            self.scorev += 1
                            self.money -= 20
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    self.player.jump()
                    if self.player.vel.x > 0:
                        self.dir = 1
                    if self.player.vel.x < 0:
                        self.dir = -1
                    self.all_sprites.add(Lode(self, self.player.pos.x, self.player.pos.y - 40, self.dir))
            
             
    
    def draw(self):
        #BackGround = Background('beach1.png', [0,0])
        #zimet, ladet
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(round(self.ilgums)), 60, ORANDZS, ekplat / 2, 15)
        self.draw_text(str(self.scorev), 60, ORANDZS, ekplat /8, 20) ######################################################################################
        self.draw_text(str(round(self.money)), 50, ORANDZS, ekplat - ekplat /8, 20)
        #self.draw_text(f"LIMENIS = {self.level}" , 30, BALTS, 100,200)
        if self.paused == True:
            self.draw_text(str(self.LODES_ATSITIENS), 30, ORANDZS, self.player.pos.x, self.player.pos.y - 80)
        
        pg.display.flip()
    def show_start_screen(self):
        self.screen.fill(BALTS)
        self.draw_text(TITLE, 48, BALTS, ekplat /2, ekgar - 400)
        self.draw_text("4 player spele :D(var ari 3 vai 2)", 22, BALTS, ekplat / 2, ekgar - 600)
        self.draw_text("SPIED jebko... 8==D lai speletu ;)", 22, BALTS, ekplat / 2, ekgar - 200)
        pg.display.flip()
        self.w84key()
        self.w84key()
        self.w84key()

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
    g.show_go_screen()
pg.quit()
