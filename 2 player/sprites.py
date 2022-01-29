from settings import *
import pygame as pg
import os
vec = pg.math.Vector2
import random

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.last_shot = 0
        self.game = game
        self.GRAVITY = GRAVITY
        self.LECIENA_STIPRUMS = LECIENA_STIPRUMS
        self.lecspeks = 2
        #anim
        self.walking = False
        self.jumping = False
        self.sliding = False
        self.dur = False
        self.current_frame = 0
        self.last_update = 0
        self.slide_update = 0
        self.holdright = False
        self.holdleft = False
        self.can_slide = True
        self.load_images()
        pg.sprite.Sprite.__init__(self)
        self.image = self.standing_frames[0]
        self.last_shot = 0
        self.rect = self.image.get_rect()
        self.rect.center = (ekplat /2 , ekgar / 2)
        self.pos = vec(ekplat /4 , ekgar / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
    
    def load_images(self):
        self.walking_frames_l = [pg.transform.flip(pg.image.load(os.path.join("pic", "walkingr.png")), True, False), pg.transform.flip(pg.image.load(os.path.join("pic", "walkingr2.png")), True, False), pg.transform.flip(pg.image.load(os.path.join("pic", "walkingr3.png")), True, False), pg.transform.flip(pg.image.load(os.path.join("pic", "walkingr4.png")), True, False), pg.transform.flip(pg.image.load(os.path.join("pic", "walkingr5.png")), True, False), pg.transform.flip(pg.image.load(os.path.join("pic", "walkingr6.png")), True, False)]
        self.walking_frames_r = [pg.image.load(os.path.join("pic", "walkingr.png")), pg.image.load(os.path.join("pic", "walkingr2.png")), pg.image.load(os.path.join("pic", "walkingr3.png")), pg.image.load(os.path.join("pic", "walkingr4.png")), pg.image.load(os.path.join("pic", "walkingr5.png")), pg.image.load(os.path.join("pic", "walkingr6.png"))]
        #self.standing_frames = [pg.image.load(os.path.join("pic", "stavos1.png")), pg.image.load(os.path.join("pic", "stavos2.png")), pg.image.load(os.path.join("pic", "stavos3.png")), pg.image.load(os.path.join("pic", "stavos4.png")), pg.image.load(os.path.join("pic", "stavos5.png")), pg.image.load(os.path.join("pic", "stavos6.png")), pg.image.load(os.path.join("pic", "stavos7.png")), pg.image.load(os.path.join("pic", "stavos8.png")), pg.image.load(os.path.join("pic", "stavos9.png"))]
        #self.dur_frames = [pg.image.load(os.path.join("pic", "sit.png")), pg.image.load(os.path.join("pic", "sit2.png"))]
        self.standing_frames = [pg.image.load(os.path.join("pic", "idle1.png")),pg.image.load(os.path.join("pic", "idle2.png")),pg.image.load(os.path.join("pic", "idle3.png")),pg.image.load(os.path.join("pic", "idle4.png"))]
    def jump(self):
        #if self.pos.y >= ekgar - 180:
        if self.lecspeks >= 0:
            self.vel.y = -self.LECIENA_STIPRUMS
            self.lecspeks -= 1
    
    def slide(self):
        self.walking = False
        self.sliding = True
        if self.can_slide:
            self.can_slide = False
            if self.vel.x > 0 :
                self.vel.x = 10
            if self.vel.x < 0 :
                self.vel.x = -10
        #if self.vel.x == 0:
            #self.walking = True

    def update(self):
        nou = pg.time.get_ticks()
        if nou - self.slide_update > 2000:
            self.slide_update = nou
            self.can_slide = True
        print(self.vel)
        self.animate()
        self.acc = vec(0, self.GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
            if keys[pg.K_s]:
                if self.vel.y == 0:
                    self.slide()
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
            if keys[pg.K_s]:
                if self.vel.y == 0:
                    self.slide()

                    #self.vel.y -= 1
        #if keys[pg.MOUSEBUTTONDOWN]:
            #now = pg.time.get_ticks()
            #if now - self.last_shot > BULLET_RATE:
                #self.last_shot = now
            #dir = vec(1, 0)#.rotate(-self.rot)
            #pos = self.pos + NO_KURIENES
            #Lode(self.game, pos, dir)

        #ieliek bremzi
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # kustibas apr
        self.vel += self.acc
        if abs(self.vel.x) < 0.4:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > ekplat:
            self.pos.x = ekplat
        if self.pos.x < 0:
            self.pos.x = 0
        
        self.rect.midbottom = self.pos # center...
        
        #self.mask = pg.mask.from_surface(self.image)

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        #anime walking
        if self.walking:
            if now - self.last_update > 50:
                #print(round(self.vel.x)) #########################################################
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_r)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image =self.walking_frames_r[self.current_frame]
                elif self.vel.x < 0:
                    self.image = self.walking_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


        now = pg.time.get_ticks()
        if not self.jumping and not self.walking:
            if now - self.last_update > 150: #uptdEEEEEEEEEEEEEE
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]

                #self.image = pg.transform.scale2x(self.image) # SCAAALLEEEEEEE
                #self.image = pg.transform.scale2x(self.image)
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        now = pg.time.get_ticks()
        #self.jumping = False
        if self.jumping:
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jumping_framesu)
                bottom = self.rect.bottom
                if self.vel.y < 0:
                    self.image = self.jumping_framesu[self.current_frame]
                else:
                    self.image = self.jumping_framesd[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        #self.mask = pg.mask.from_surface(self.image)
class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(MELNS)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Siena(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(MELNS)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Lode(pg.sprite.Sprite): 
    def __init__(self, game, pos, targ):
        self.dir = dir
        self.groups = game.all_sprites, game.lodes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((10, 10))
        self.image.fill(MELNS)
        #self.image = pg.image.load(os.path.join("pic", "lode.png"))
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.spawn_time = pg.time.get_ticks()
        self.speed = BULLET_SPEED
        self.target = vec(targ)

        
    def update(self):
        move = self.target - self.pos
        move_lenght = move.length()
        if move_lenght < self.speed:
            self.pos = self.target
            self.kill()
        elif move_lenght != 0:
            move.normalize_ip()
            move = move* self.speed
            self.pos += move
        #self.pos += self.vel / 100
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()
        if pg.sprite.spritecollideany(self, self.game.lietas):
            self.kill()
            Kareivis(self.game) #                       #####################################################################################################

class Kareivis(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.kareivji
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.last_update = 0
        self.image = pg.image.load(os.path.join("pic", "stavos2.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (ekplat /2 , ekgar - 390)
        self.pos = vec(ekplat /2 , ekgar - 390)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.la = True

    def update(self):
        hits= pg.sprite.spritecollideany(self, self.game.lodes)
        if hits:
            self.kill()
        if self.la == False:
            self.acc = vec(-ENE_ATRUMS, 0)
            #self.image =pg.transform.flip(pg.image.load(os.path.join("pic", "walkingr.png")), True, False)
        elif self.la == True:
            self.acc = vec(ENE_ATRUMS, 0)
            #self.image = pg.image.load(os.path.join("pic", "walkingr.png"))
        self.pos += self.acc
        self.rect.midbottom = self.pos # center...

        now = pg.time.get_ticks()
        if now - self.last_update > 3000: #uptdEEEEEEEEEEEEEE
            self.last_update = now
            if self.la == False:
                self.la = True
            else:
                self.la = False

            
            
