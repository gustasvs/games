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
        self.dir = 0
        self.ilgum = 0.1
        self.i = 0
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
        self.mob_timer = 0
        self.p1 = Platform(90, ekgar - 170, ekplat - 180, 180)
        self.p2 = Platform(90, ekgar - 170, ekplat - 180, 10)
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.lodes)
        self.all_sprites.add(self.mobs)
        self.platforms.add(self.p1)
        self.platforms1.add(self.p2)
        self.all_sprites.add(self.p1)
        self.all_sprites.add(self.p2)

        self.run()

    def run(self):
        #game loop
        self.playing = True
        while self.playing:
            #print(self.player.pos.y, ekgar - 170)
            self.cock.tick(FPS)
            self.ilgums -= self.ilgum
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        #for e in self.lodes:
        if self.ilgums < 0:
            self.ilgums = ILGUMSS
            if self.MOBU_DAUDZUMS > 100:
                self.MOBU_DAUDZUMS -= 100
        self.all_sprites.update()



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
            self.playing = False
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        if mob_hits:
            self.player.kill()
            self.playing = False
    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    self.player.jump()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
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
        
        pg.display.flip()

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
pg.quit()
