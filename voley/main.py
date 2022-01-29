# Volits! - sit un bliez

import pygame as pg
import random
import time
from settings import *
from sprites import *
from os import path
from pygame.locals import *

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        # self.screen = pg.display.set_mode((ekplat, ekgar), FULLSCREEN | DOUBLEBUF)
        self.screen = pg.display.set_mode((ekplat, ekgar), DOUBLEBUF)
        self.screen.set_alpha(None)
        pg.display.set_caption(VARDS)
        self.cock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'img')

    def new(self):
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.paused = False
        self.last_time_paused = 0
        self.ir_kads_nospiests = False
        self.ballPredictionPos = vec(0, 0)
        self.MAKONU_DAUDZUMS = MAKONU_DAUDZUMS
        self.scorev = 0
        self.scorez = 0
        self.ilgums = ILGUMSS
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.predictionBalls = pg.sprite.Group()
        self.balls = pg.sprite.Group()
        self.clouds = pg.sprite.LayeredUpdates()
        self.ball = Ball(self, (random.choice([0, 1])))
        self.all_sprites.add(self.ball)
        self.balls.add(self.ball)
        self.ground = Platform(0, ekgar - 70, ekplat, 70, SMILSU)
        self.tikls = Tikls(ekplat/2, ekgar * 3 / 4.2, 20, 136)
        self.all_sprites.add(self.ground)
        self.all_sprites.add(self.tikls)
        self.platforms.add(self.ground)

        # add bots / players
        for e in range(self.zalobotuskaits):
            self.bottz = Bot_z(self, e + 1)
            self.all_sprites.add(self.bottz)
        for e in range(self.violetobotuskaits):
            self.bottv = Bot_v(self, e + 1)
            self.all_sprites.add(self.bottv)
        for e in range(self.zalospeletajuskaits):
            self.playerz = Player(self, "z", e + 1)
            self.all_sprites.add(self.playerz)
            self.players.add(self.playerz)
        for e in range(self.violetospeletajuskaits):
            self.playerv = Player(self, "v", e + 1)
            self.all_sprites.add(self.playerv)
            self.players.add(self.playerv)
        

        # start makoni ta lai debesis nav tuksas kad spele sakas
        for e in range(MAKONU_DAUDZUMS // 4):
            cl = Cloud(self)
            cl.pos.x = random.randint(-1000, ekplat)
            cl.pos.y = random.randint(-50, 300)
            self.clouds.add(cl)

        self.run()


    def run(self):
        #game loop
        self.playing = True
        while self.playing:
            self.cock.tick(FPS)
            self.events()
            if self.paused == False:
                self.ilgums -= 0.015
                self.update()
            self.clouds.update()
            self.draw()

    def update(self):

        #CLOUDS
        
        keys = pg.key.get_pressed()
        if TEST_MODE:
            if keys[pg.K_t]:
                self.MAKONU_DAUDZUMS = 2
            if keys[pg.K_y]:
                self.MAKONU_DAUDZUMS = MAKONU_DAUDZUMS
            if keys[pg.K_q]:
                for clo in self.clouds:
                    clo.kill()
        if self.ilgums < 0:
            self.show_go_scren()
        if random.randrange(1, self.MAKONU_DAUDZUMS) == 1:
            self.clouds.add(Cloud(self))
        self.clouds.update()

        # BUMBA (var parlikt balls koda bet nevaig)

        self.all_sprites.update()
        
        if self.ball.vel.y > 0:
            hits = pg.sprite.spritecollide(self.ball, self.platforms, False)
            if hits:
                self.ball.pos.y = hits[0].rect.top
                self.ball.vel.y = 0
                if self.ball.satre:
                    if self.ball.rect.x > ekplat / 2:
                        self.scorev += 1
                        self.ball.kill()
                        self.ball = Ball(self, 0)
                        self.all_sprites.add(self.ball)
                        self.balls.add(self.ball)
                        self.run()
                        
                    if self.ball.rect.x < ekplat / 2:
                        self.scorez += 1
                        self.ball.kill()
                        self.ball = Ball(self, 1)
                        self.all_sprites.add(self.ball)
                        self.balls.add(self.ball)
                        self.run()


        self.ballPrediction = BallPrediction(self, self.ball.pos, self.ball.vel)
        numberofiter = 0
        while self.ballPrediction.pos.y < 640 and numberofiter < 100:
            numberofiter += 1
            self.ballPrediction.update()
        self.ballPredictionPos = self.ballPrediction.pos
        self.ballPrediction.kill()
            
                          
    def events(self):
            for eve in pg.event.get():
                if eve.type == pg.QUIT:
                    if self.playing:
                        self.playing = False
                    self.running = False
                    exit(0)
                if eve.type == pg.KEYDOWN:
                    if eve.key == pg.K_ESCAPE:
                        now = pg.time.get_ticks()
                        if now - self.last_time_paused > 100:
                            if self.paused == False:
                                self.paused = True
                            else:
                                self.paused = False


    def draw(self):
        self.screen.fill(BGCOLOR)
        self.clouds.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(round(self.ilgums)), 60, MELNS, ekplat / 2, 15, True)
        self.draw_text(str(self.scorev), 69, MELNS, ekplat /4, 15, True) 
        self.draw_text(str(self.scorez), 69, MELNS, ekplat - ekplat /4, 15, True)
        for num, player in enumerate(self.players):
            self.draw_text("V", 28, BALTS, player.pos.x, player.pos.y - 130)
            # self.draw_text(f"P{num + 1}", 28, BALTS, player.pos.x, player.pos.y - 130)
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", 105, BALTS, ekplat / 2, ekgar / 2,)
            
        if TEST_MODE:
            self.draw_text(f"FPS = {str(int(self.cock.get_fps()))}", 30, MELNS, ekplat - 50, ekgar - 30)
            self.draw_text(f"^", 50, MELNS, self.ballPredictionPos.x, ekgar - 60)

        pg.display.flip()
        

    def show_go_scren(self):
        self.screen.fill(LIGHTBLUE)
        if self.scorev > self.scorez:
            punkti = self.scorev - self.scorez
            if punkti != 1:
                self.draw_text(f"Violetie uzvareja ar {punkti} punktu parsvaru!", 48, MELNS, ekplat /2, ekgar - 400, True)
            if punkti == 1:
                self.draw_text(f"Violetie uzvareja ar {punkti} punkta parsvaru!", 48, MELNS, ekplat /2, ekgar - 400, True)
        if self.scorev < self.scorez:
            punkti = self.scorez - self.scorev
            if punkti != 1:
                self.draw_text(f"zalie uzvareja ar {punkti} punktu parsvaru", 48, MELNS, ekplat /2, ekgar - 400, True)
            if punkti == 1:
                self.draw_text(f"zalie uzvareja ar {punkti} punkta parsvaru", 48, MELNS, ekplat /2, ekgar - 400, True)
        if self.scorev == self.scorez:
            self.draw_text("neizskirts!!!!", 48, MELNS, ekplat /2, ekgar - 400, True)
        #self.draw_text("LOL pauls smird :)", 22, MELNS, ekplat / 2, ekgar - 600)
        #self.draw_text("KGbraki rulle (Subscribe to gustasvs and kiksmas)", 22, MELNS, ekplat / 2, ekgar - 200)
        pg.display.flip()
        self.w84key()
        self.w84key()
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

    def draw_text(self, text, size, color, x, y, shadow=False):
        if shadow == True:
            fontshadow = pg.font.Font(self.font_name, size)
            if color == MELNS or color == PELEKS:
                colorshadow = BALTS
            else:
                colorshadow = PELEKS
            text_surfaceshadow = fontshadow.render(text, True, colorshadow)
            text_rectshadow = text_surfaceshadow.get_rect()
            text_rectshadow.midtop = (x + 3, y + 3)
            self.screen.blit(text_surfaceshadow, text_rectshadow)
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        self.buttons        = pg.sprite.Group()
        self.start_sprites  = pg.sprite.Group()
        self.VoleyParticles = pg.sprite.Group()
        self.phisics_buttons= pg.sprite.Group()
        self.waiting        = True
        self.p1 = PhysicsButton(ekplat/2 - 150, ekgar/2 + 50, 100, 100,'p1', self, TUMSIZALS, TUMSIVIOLETS, BALTS)
        self.p2 = PhysicsButton(ekplat/2 + 50, ekgar/2 + 50, 100, 100, 'p2', self, TUMSIZALS, TUMSIVIOLETS, BALTS)
        self.b1 = PhysicsButton(ekplat/2 - 390, 200, 50, 50, 'b1', self,  ZALS, VIOLETS, BALTS)
        self.b2 = PhysicsButton(ekplat/2 - 240, 200, 50, 50, 'b2', self,  ZALS, VIOLETS, BALTS)
        self.b3 = PhysicsButton(ekplat/2 - 90, 200, 50, 50, 'b3', self,  ZALS, VIOLETS, BALTS)
        self.b4 = PhysicsButton(ekplat/2 + 40, 200, 50, 50, 'b4', self,  ZALS, VIOLETS, BALTS)
        self.b5 = PhysicsButton(ekplat/2 + 190, 200, 50, 50, 'b5', self,  ZALS, VIOLETS, BALTS)
        self.b6 = PhysicsButton(ekplat/2 + 340, 200, 50, 50, 'b6', self,  ZALS, VIOLETS, BALTS)
        self.playButton           = Button(ekplat/2 - 260, 50, 520, 75, 'play', self, ORANDZS, ORANDZS)
        
        self.phisics_buttons.add(self.b1)
        self.phisics_buttons.add(self.b2)
        self.phisics_buttons.add(self.b3)
        self.phisics_buttons.add(self.b4)
        self.phisics_buttons.add(self.b5)
        self.phisics_buttons.add(self.b6)
        self.phisics_buttons.add(self.p1)
        self.phisics_buttons.add(self.p2)
        self.buttons.add(self.playButton)
    
        self.ground = Platform(0, ekgar - 70, ekplat, 70, SMILSU)
        self.balsts = Platform(250, 250, ekplat - 500, 10, MELNS)
        self.tikls = Tikls(ekplat/2, ekgar * 3 / 4.2, 20, 136)
        self.start_sprites.add(self.balsts)
        self.start_sprites.add(self.ground)
        self.start_sprites.add(self.tikls)

        self.cock = pg.time.Clock()

        while self.waiting == True:
            self.buttons.update()
            self.start_sprites.update()
            self.phisics_buttons.update()
            self.screen.fill(LIGHTBLUE) 
            self.start_sprites.draw(self.screen)
            self.phisics_buttons.draw(self.screen)
            self.buttons.draw(self.screen)
            self.onbutton = False
        


            # self.draw_text(TITLE, 68, BALTS, ekplat /2, ekgar - 680, True)
            # self.draw_text("BOT", 32, MELNS, self.b1.pos.x + self.b1.w / 2, self.b1.pos.y + 15)
            # self.draw_text("BOT", 32, MELNS, self.b2.pos.x + self.b2.w / 2, self.b2.pos.y + 15)
            # self.draw_text("BOT", 32, MELNS, self.b3.pos.x + self.b3.w / 2, self.b3.pos.y + 15)
            # self.draw_text("BOT", 32, MELNS, self.b4.pos.x + self.b4.w / 2, self.b4.pos.y + 15)
            # self.draw_text("BOT", 32, MELNS, self.b5.pos.x + self.b5.w / 2, self.b5.pos.y + 15)
            # self.draw_text("BOT", 32, MELNS, self.b6.pos.x + self.b6.w / 2, self.b6.pos.y + 15)
            # self.draw_text("P1", 48, BALTS, self.p1.pos.x + self.p1.w / 2 + 3, self.p1.pos.y + 48)
            # self.draw_text("P2", 48, BALTS, self.p2.pos.x + self.p2.w / 2 + 3, self.p2.pos.y + 48)
            # self.draw_text("P1", 48, MELNS, self.p1.pos.x + self.p1.w / 2, self.p1.pos.y + 45)
            # self.draw_text("P2", 48, MELNS, self.p2.pos.x + self.p2.w / 2, self.p2.pos.y + 45)

            self.zaloskaits = 0
            self.violetoskaits = 0
            self.zalobotuskaits = 0
            self.violetobotuskaits = 0
            self.zalospeletajuskaits = 0
            self.violetospeletajuskaits = 0
            for e in self.phisics_buttons:
                if e.color != e.nonefill:
                    if e.color == e.purplefill:
                        if e.krasa == "p1":
                            self.violetospeletajuskaits += 1
                        elif e.krasa == "p2":
                            self.violetospeletajuskaits += 1
                        else:
                            self.violetobotuskaits += 1
                        self.violetoskaits += 1
                    if e.color == e.greenfill:
                        if e.krasa == "p1":
                            self.zalospeletajuskaits += 1
                        elif e.krasa == "p2":
                            self.zalospeletajuskaits += 1
                        else:
                            self.zalobotuskaits += 1
                        self.zaloskaits += 1
                    
            self.draw_text(f"Violetie = {self.violetoskaits}", 56, BALTS, ekplat / 2 - 465, ekgar - 53, True)
            
            self.draw_text(f"Zalie = {self.zaloskaits}", 56, BALTS, ekplat / 2 + 160, ekgar -53, True)

            self.draw_text("PLAY", 64, BALTS, ekplat / 2, 75, True)

            if TEST_MODE:
                self.cock.tick(FPS)
                self.draw_text(str(int(self.cock.get_fps())), 30, MELNS, ekplat - 50, ekgar - 30)


            pg.display.flip()
            for eve in pg.event.get():
                if eve.type == pg.QUIT:
                    self.running = False
                    self.waiting = False
                    exit(0)
                if eve.type == pg.KEYDOWN:
                    if eve.key == pg.K_ESCAPE:
                        self.waiting = False

g = Game()
while g.running:
    g.show_start_screen()
    g.new()
    # g.show_go_screen()
pg.quit()



# 2 boti
# ja ball prediction pos ir viena pusee, tad tas to noker, savaadaak otrs.
# ja ir otraa tad pirmais megina leekt
# ja ir pirmaa tad otrs rinko
# bumub no psawan izsit tikai otrs
# ja viens tiek apdullinaats (aiztrieksts) tad bumbu parker otrs
# gremtes sitieni ka parastiem botimem