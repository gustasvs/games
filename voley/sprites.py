from settings import *
import pygame as pg
import numpy
import random
import ctypes
from os import path
vec = pg.math.Vector2

class Bot_v(pg.sprite.Sprite):
    def __init__(self, game, veids):
        self._layer = BOT_LAYER
        self.veids = veids
        self.game = game
        self.walking = False
        self.jumping = False
        self.sitting = False
        self.atsitting = False
        self.current_frame = 0
        self.offset = 0
        self.last_update = 0
        self.load_images()
        pg.sprite.Sprite.__init__(self)
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        if self.veids == 1:
            self.rect.center = vec(ekplat /2 - ekplat / 6, ekgar / 2)
            self.pos         = vec(ekplat /2 - ekplat / 6, ekgar / 2)
        if self.veids == 2:
            self.rect.center = vec(ekplat / 6, ekgar / 2)
            self.pos         = vec(ekplat / 6, ekgar / 2)
        if self.veids == 3:
            self.rect.center = vec(ekplat / 2 - ekplat / 4, ekgar / 2)
            self.pos         = vec(ekplat / 2 - ekplat / 4, ekgar / 2)
        if self.veids == 4:
            self.rect.center = vec(ekplat / 4, ekgar / 2)
            self.pos         = vec(ekplat / 4, ekgar / 2)
        if self.veids == 5:
            self.rect.center = vec(ekplat / 2 - 20, ekgar / 2)
            self.pos         = vec(ekplat / 2 - 20, ekgar / 2)
        if self.veids == 6:
            self.rect.center = vec(20, ekgar / 2)
            self.pos         = vec(20, ekgar / 2)


    def load_images(self):
        
        self.walking_frames_l = [pg.image.load(path.join(self.game.img_folder, 'walkingl.png')).convert_alpha(), pg.image.load(path.join(self.game.img_folder, 'walkingl2.png')).convert_alpha()]
        self.walking_frames_r = [pg.image.load(path.join(self.game.img_folder, 'walkingr.png')).convert_alpha(), pg.image.load(path.join(self.game.img_folder, 'walkingr2.png')).convert_alpha()]
        self.atsitting_frames = [pg.image.load(path.join(self.game.img_folder, 'sit.png')).convert_alpha(), pg.image.load(path.join(self.game.img_folder, 'sit2.png')).convert_alpha()]
        self.sitting_frames = [pg.image.load(path.join(self.game.img_folder, 'atsit.png')).convert_alpha(), pg.image.load(path.join(self.game.img_folder, 'atsit2.png')).convert_alpha()]
        self.standing_frames = [pg.image.load(path.join(self.game.img_folder, 'stavos2.png')).convert_alpha(), pg.image.load(path.join(self.game.img_folder, 'stavos1.png')).convert_alpha()]

    def update(self): 
        if self.vel.y > 0:
            hits = pg.sprite.spritecollide(self, self.game.platforms, False)
            if hits:
                self.pos.y = hits[0].rect.top
                self.vel.y = 0
        self.animate()
        self.acc = vec(0, GRAVITY)

        # tuvais tiklam
        if self.veids == 1:
            if self.game.ball.vel.x < -10:
                self.jump()
            if (self.game.ballPredictionPos.x < ekplat / 2 and self.game.ballPredictionPos.x > ekplat / 4) or (self.game.violetobotuskaits < 2 and self.game.ballPredictionPos.x < ekplat / 2):

                if self.game.ballPredictionPos.x > self.pos.x:
                    self.acc.x = PLAYER_ACC
                if self.game.ballPredictionPos.x < self.pos.x:
                    self.acc.x = -PLAYER_ACC

                if abs(self.game.ballPredictionPos.x - self.pos.x) < 50:
                    self.vel.x *= 0.75

            else:
                if self.pos.x < ekplat / 2 - 20:
                    self.acc.x = (PLAYER_ACC / 2)
                
        # talak no tikla
        if self.veids == 2:

            if self.game.ballPredictionPos.x < ekplat / 4 or (self.game.violetobotuskaits < 2 and self.game.ballPredictionPos.x < ekplat / 2):
                
                if self.game.ballPredictionPos.x > self.pos.x:
                    self.acc.x = PLAYER_ACC
                if self.game.ballPredictionPos.x < self.pos.x:
                    self.acc.x = -PLAYER_ACC
                        
                if abs(self.game.ballPredictionPos.x - self.pos.x) < 50:
                    self.vel.x *= 0.75

            else:
                if self.pos.x > ekplat / 4:
                    self.acc.x = - (PLAYER_ACC)

        if self.veids > 2:
            if self.game.ball.vel.x < -20:
                self.jump()
            if self.game.ball.vel.x <= 0 or self.game.ball.pos.x < ekplat / 2:

                if self.game.ballPredictionPos.x > self.pos.x:
                    self.acc.x = PLAYER_ACC
                if self.game.ballPredictionPos.x < self.pos.x:
                    self.acc.x = -PLAYER_ACC
                if abs(self.game.ballPredictionPos.x - self.pos.x) < 50:
                    self.vel.x /= 2

            else:
                if self.pos.x > ekplat / 4:
                    self.acc.x = PLAYER_ACC / 2
    
        self.acc.x += self.vel.x * GROUND_FRICTION
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        
        if self.pos.x > ekplat / 2 - 20:
            self.pos.x = ekplat /2 - 20
        if self.pos.x < 0:
            self.pos.x = 0
        self.rect.midbottom = self.pos # center...
        
        satr = pg.sprite.spritecollide(self, self.game.balls, False, pg.sprite.collide_mask)
        self.atsitting = False
        self.sitting = False
        if satr:
            if self.game.ball.vel.x > -20:
                if self.pos.y > 500:
                    self.atsitting = True
                    self.game.ball.satre = True
                    self.game.ball.vel.x = 15
                    self.game.ball.vel.y = -15
                if self.pos.y <= 500:
                    self.game.ball.vel.x = 30 + self.vel.x
                    self.game.ball.vel.y = 3
            else:
                self.vel.x = -BUMBAS_TRIECIENS + self.game.ball.vel.x # cik daudz atsit atpakal
                self.vel.y = 0
                self.game.ball.vel.x = 1
                self.game.ball.vel.y = -15
        

    def jump(self):
        if self.rect.y > ekgar - 180:
            self.vel.y = -LECIENA_STIPRUMS
    
    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        #anime walking
        if self.walking:
            if now - self.last_update > 200:
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
        if not self.sitting and not self.jumping and not self.atsitting and not self.walking:
            if now - self.last_update > 150: #uptdEEEEEEEEEEEEEE
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        now = pg.time.get_ticks()
        if self.vel.y != 0:
            self.jumping = False
        else:
            self.jumping = False
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

        if self.sitting:
            now = pg.time.get_ticks()
            if now - self.last_update > 150: #uptdEEEEEEEEEEEEEE
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.sitting_frames)
                bottom = self.rect.bottom
                self.image = self.sitting_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        now = pg.time.get_ticks()
        if self.atsitting:
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.atsitting_frames)
                bottom = self.rect.bottom
                self.image = self.atsitting_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        self.mask = pg.mask.from_surface(self.image)

class Bot_z(pg.sprite.Sprite):
    def __init__(self, game, veids):
        self._layer = BOT_LAYER
        self.veids = veids
        self.game = game
        self.walking = False
        self.jumping = False
        self.sitting = False
        self.atsitting = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        pg.sprite.Sprite.__init__(self)
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        if self.veids == 1:
            self.rect.center = vec(ekplat /2 + ekplat / 6, ekgar / 2)
            self.pos         = vec(ekplat /2 + ekplat / 6, ekgar / 2)
        if self.veids == 2:
            self.rect.center = vec(ekplat - ekplat / 6, ekgar / 2)
            self.pos         = vec(ekplat - ekplat / 6, ekgar / 2)
        if self.veids == 3:
            self.rect.center = vec(ekplat / 2 + ekplat / 4, ekgar / 2)
            self.pos         = vec(ekplat / 2 + ekplat / 4, ekgar / 2)
        if self.veids == 4:
            self.rect.center = vec(ekplat - ekplat / 4, ekgar / 2)
            self.pos         = vec(ekplat - ekplat / 4, ekgar / 2)
        if self.veids == 5:
            self.rect.center = vec(ekplat - 20, ekgar / 2)
            self.pos         = vec(ekplat - 20, ekgar / 2)
        if self.veids == 6:
            self.rect.center = vec(ekplat / 2 + 20, ekgar / 2)
            self.pos         = vec(ekpalt / 2 + 20, ekgar / 2)

    def load_images(self):
        self.walking_frames_l = [pg.image.load(path.join(self.game.img_folder, 'zwalkingl.png')).convert_alpha(), pg.image.load(path.join(self.game.img_folder, 'zwalkingl2.png')).convert_alpha()]
        self.walking_frames_r = [pg.image.load(path.join(self.game.img_folder, 'zwalkingr.png')).convert_alpha(), pg.image.load(path.join(self.game.img_folder, 'zwalkingr2.png')).convert_alpha()]
        self.atsitting_frames = [pg.image.load(path.join(self.game.img_folder, 'zsit.png')).convert_alpha(), pg.image.load(path.join(self.game.img_folder, 'zsit2.png')).convert_alpha()]
        self.sitting_frames = [pg.image.load(path.join(self.game.img_folder, 'zatsit.png')).convert_alpha(), pg.image.load(path.join(self.game.img_folder, 'zatsit2.png')).convert_alpha()]
        self.standing_frames = [pg.image.load(path.join(self.game.img_folder, 'zstavos2.png')).convert_alpha(), pg.image.load(path.join(self.game.img_folder, 'zstavos1.png')).convert_alpha()]


    def update(self): 
        #PLATFORMAS
        if self.vel.y > 0:
            hits = pg.sprite.spritecollide(self, self.game.platforms, False)
            if hits:
                self.pos.y = hits[0].rect.top
                self.vel.y = 0

        self.animate()
        self.acc = vec(0, GRAVITY)

        # tuvais tiklam
        if self.veids == 1:
            if self.game.ball.vel.x > 10:
                self.jump()
            if (self.game.ballPredictionPos.x > ekplat / 2 and self.game.ballPredictionPos.x < ekplat -  ekplat / 4) or (self.game.zalobotuskaits < 2 and self.game.ballPredictionPos.x > ekplat / 2):

                if self.game.ballPredictionPos.x > self.pos.x:
                    self.acc.x = PLAYER_ACC
                if self.game.ballPredictionPos.x < self.pos.x:
                    self.acc.x = -PLAYER_ACC

                if abs(self.game.ballPredictionPos.x - self.pos.x) < 50:
                    self.vel.x *= 0.75

            else:
                if self.pos.x > ekplat / 2 + 20:
                    self.acc.x = -(PLAYER_ACC / 2)
                
        # talak no tikla
        if self.veids == 2:

            if self.game.ballPredictionPos.x < ekplat / 4 or (self.game.violetobotuskaits < 2 and self.game.ballPredictionPos.x < ekplat / 2):
                
                if self.game.ballPredictionPos.x > self.pos.x:
                    self.acc.x = PLAYER_ACC
                if self.game.ballPredictionPos.x < self.pos.x:
                    self.acc.x = -PLAYER_ACC
                        
                if abs(self.game.ballPredictionPos.x - self.pos.x) < 50:
                    self.vel.x *= 0.75

            else:
                if self.pos.x > ekplat / 4:
                    self.acc.x = - (PLAYER_ACC)

        if self.veids > 2:
            if self.game.ball.vel.x < -20:
                self.jump()
            if self.game.ball.vel.x <= 0 or self.game.ball.pos.x < ekplat / 2:

                if self.game.ballPredictionPos.x > self.pos.x:
                    self.acc.x = PLAYER_ACC
                if self.game.ballPredictionPos.x < self.pos.x:
                    self.acc.x = -PLAYER_ACC
                if abs(self.game.ballPredictionPos.x - self.pos.x) < 50:
                    self.vel.x /= 2

            else:
                if self.pos.x > ekplat / 4:
                    self.acc.x = PLAYER_ACC / 2
                    
        self.acc.x += self.vel.x * GROUND_FRICTION
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc


        if self.pos.x < ekplat / 2 + 40:
            self.pos.x = ekplat /2 + 40
        if self.pos.x > ekplat - 10:
            self.pos.x = ekplat - 10
        self.rect.midbottom = self.pos

        satr = pg.sprite.spritecollide(self, self.game.balls, False, pg.sprite.collide_mask)
        self.atsitting = False
        self.sitting = False
        if satr:
            if self.game.ball.vel.x < 20:
                if self.pos.y > 500:
                    self.atsitting = True
                    self.game.ball.satre = True
                    self.game.ball.vel.x = 0
                    self.game.ball.vel.x -= 15
                    self.game.ball.vel.y = 0
                    self.game.ball.vel.y -= 15
                if self.pos.y <= 500:
                    self.sitting = True
                    self.game.ball.vel.x = 0
                    self.game.ball.vel.x = -30 + self.vel.x
                    #print(self.game.ball.vel.x, 'z')
                    self.game.ball.vel.y = 0
                    self.game.ball.vel.y = +3
            else:
                self.vel.x = BUMBAS_TRIECIENS + self.game.ball.vel.x
                self.vel.y = 0
                self.game.ball.vel.x = -1
                self.game.ball.vel.y = -15
        

    def jump(self):
        if self.rect.y > ekgar - 180:
            self.vel.y = -LECIENA_STIPRUMS
    
    def animate(self):
        if self.veids == 'z':
            now = pg.time.get_ticks()
            if self.vel.x != 0:
                self.walking = True
            else:
                self.walking = False
            #anime walking
            if self.walking:
                if now - self.last_update > 200:
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
            if not self.sitting and not self.jumping and not self.atsitting and not self.walking:
                if now - self.last_update > 150: #uptdEEEEEEEEEEEEEE
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                    bottom = self.rect.bottom
                    self.image = self.standing_frames[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom

            if self.sitting:
                now = pg.time.get_ticks()
                if now - self.last_update > 150: #uptdEEEEEEEEEEEEEE
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.sitting_frames)
                    bottom = self.rect.bottom
                    self.image = self.sitting_frames[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom

            now = pg.time.get_ticks()
            if self.atsitting:
                if now - self.last_update > 150:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.atsitting_frames)
                    bottom = self.rect.bottom
                    self.image = self.atsitting_frames[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
            self.mask = pg.mask.from_surface(self.image)


class Player(pg.sprite.Sprite):
    def __init__(self, game, krasa, veids):
        self._layer = PLAYER_LAYER
        self.game = game
        self.krasa = krasa
        self.veids = veids
        self.walking = False
        self.sap = False
        self.jumping = False
        self.sitting = False
        self.atsitting = False
        self.current_frame = 0
        self.last_update = 0
        if self.krasa == "z":
            self.load_imagesz()
        if self.krasa == "v":
            self.load_imagesv()
        pg.sprite.Sprite.__init__(self)
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        if self.krasa == "v":
            if self.veids == 1:
                self.rect.center = vec(ekplat / 2 - ekplat / 6, ekgar / 2)
                self.pos         = vec(ekplat / 2 - ekplat / 6, ekgar / 2)
            if self.veids == 2:
                self.rect.center = vec(ekplat / 6, ekgar / 2)
                self.pos         = vec(ekplat / 6, ekgar / 2)
        if self.krasa == "z":
            if self.veids == 1:
                self.rect.center = vec(ekplat / 2 + ekplat / 6, ekgar / 2)
                self.pos         = vec(ekplat / 2 + ekplat / 6, ekgar / 2)
            if self.veids == 2:
                self.rect.center = vec(ekplat - ekplat / 6, ekgar / 2)
                self.pos         = vec(ekplat - ekplat / 6, ekgar / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
    
    def load_imagesv(self):
        self.walking_frames_l = [pg.image.load(path.join(self.game.img_folder, 'walkingl.png')).convert_alpha(), pg.image.load(path.join(self.game.img_folder, 'walkingl2.png')).convert_alpha()]
        self.walking_frames_r = [pg.image.load(path.join(self.game.img_folder, 'walkingr.png')).convert_alpha(), pg.image.load(path.join(self.game.img_folder, 'walkingr2.png')).convert_alpha()]
        self.atsitting_frames = [pg.image.load(path.join(self.game.img_folder, 'sit.png')).convert_alpha(), pg.image.load(path.join(self.game.img_folder, 'sit2.png')).convert_alpha()]
        self.sitting_frames   = [pg.image.load(path.join(self.game.img_folder, 'atsit.png')).convert_alpha(), pg.image.load(path.join(self.game.img_folder, 'atsit2.png')).convert_alpha()]
        self.standing_frames  = [pg.image.load(path.join(self.game.img_folder, 'stavos2.png')).convert_alpha(), pg.image.load(path.join(self.game.img_folder, 'stavos1.png')).convert_alpha()]

    def load_imagesz(self):
        self.walking_frames_l = [pg.image.load(path.join(self.game.img_folder, 'zwalkingl.png')).convert_alpha(), pg.image.load(path.join(self.game.img_folder, 'zwalkingl2.png')).convert_alpha()]
        self.walking_frames_r = [pg.image.load(path.join(self.game.img_folder, 'zwalkingr.png')).convert_alpha(), pg.image.load(path.join(self.game.img_folder, 'zwalkingr2.png')).convert_alpha()]
        self.atsitting_frames = [pg.image.load(path.join(self.game.img_folder, 'zsit.png')).convert_alpha(), pg.image.load(path.join(self.game.img_folder, 'zsit2.png')).convert_alpha()]
        self.sitting_frames   = [pg.image.load(path.join(self.game.img_folder, 'zatsit.png')).convert_alpha(), pg.image.load(path.join(self.game.img_folder, 'zatsit2.png')).convert_alpha()]
        self.standing_frames  = [pg.image.load(path.join(self.game.img_folder, 'zstavos2.png')).convert_alpha(), pg.image.load(path.join(self.game.img_folder, 'zstavos1.png')).convert_alpha()]

    def update(self):
        #PLATFORMAS
        self.acc = vec(0, GRAVITY)
        if self.vel.y > 0:
            hits = pg.sprite.spritecollide(self, self.game.platforms, False)
            if hits:
                self.pos.y = hits[0].rect.top
                self.vel.y = 0
        
        keys = pg.key.get_pressed()
        if self.krasa == "v":
            if self.veids == 1:
                if keys[pg.K_a]:
                    self.acc.x = -PLAYER_ACC
                if keys[pg.K_d]:
                    self.acc.x = PLAYER_ACC
                if keys[pg.K_w]:
                    self.jump()
            if self.veids == 2:
                if keys[pg.K_j]:
                    self.acc.x = -PLAYER_ACC
                if keys[pg.K_l]:
                    self.acc.x = PLAYER_ACC
                if keys[pg.K_i]:
                    self.jump()
            satr = pg.sprite.spritecollide(self, self.game.balls, False, pg.sprite.collide_mask)
            if satr:
                if self.game.ball.vel.x > -20:
                    if self.veids == 1:
                        if keys[pg.K_s]:
                            self.game.ball.satre = True
                            self.game.ball.vel.x = 15
                            self.game.ball.vel.y = -15
                        if keys[pg.K_e]:
                            self.game.ball.vel.x = 30 + self.vel.x
                            self.game.ball.vel.y = 3
                    if self.veids == 2:
                        if keys[pg.K_k]:
                            self.game.ball.satre = True
                            self.game.ball.vel.x = 15
                            self.game.ball.vel.y = -15
                        if keys[pg.K_o]:
                            self.game.ball.vel.x = 30 + self.vel.x
                            self.game.ball.vel.y = 3
                        
                else:
                    self.vel.x = -BUMBAS_TRIECIENS + self.game.ball.vel.x # cik daudz atsit atpakal
                    self.vel.y = 0
                    self.game.ball.vel.x = 1
                    self.game.ball.vel.y = -15
            self.animatev()

        keys = pg.key.get_pressed()
        if self.krasa == "z":
            if self.veids == 1:
                if keys[pg.K_j]:
                    self.acc.x = -PLAYER_ACC
                if keys[pg.K_l]:
                    self.acc.x = PLAYER_ACC    
                if keys[pg.K_i]:
                    self.jump() 
            if self.veids == 2:
                if keys[pg.K_a]:
                    self.acc.x = -PLAYER_ACC
                if keys[pg.K_d]:
                    self.acc.x = PLAYER_ACC    
                if keys[pg.K_w]:
                    self.jump() 
            satr = pg.sprite.spritecollide(self, self.game.balls, False, pg.sprite.collide_mask)
            if satr:
                if self.game.ball.vel.x < 20:
                    if self.veids == 1:
                        if keys[pg.K_k]:
                            self.game.ball.satre = True
                            self.game.ball.vel.x = -15
                            self.game.ball.vel.y = -15
                        if keys[pg.K_o]:
                            self.game.ball.vel.x = -30 + self.vel.x
                            self.game.ball.vel.y = 3
                    if self.veids == 2:
                        if keys[pg.K_s]:
                            self.game.ball.satre = True
                            self.game.ball.vel.x = -15
                            self.game.ball.vel.y = -15
                        if keys[pg.K_e]:
                            self.game.ball.vel.x = -30 + self.vel.x
                            self.game.ball.vel.y = 3
                else:
                    self.vel.x = BUMBAS_TRIECIENS + self.game.ball.vel.x
                    self.vel.y = 0
                    self.game.ball.vel.x = -1
                    self.game.ball.vel.y = -15
            self.animatez()

        self.acc.x += self.vel.x * GROUND_FRICTION
        self.vel += self.acc
        if abs(self.vel.x) < 0.4:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        
        if self.krasa == "v":
            if self.pos.x > ekplat / 2 - 20:
                self.pos.x = ekplat /2 - 20
            if self.pos.x < 0:
                self.pos.x = 0
        if self.krasa == "z":
            if self.pos.x < ekplat / 2 + 40:
                self.pos.x = ekplat /2 + 40
            if self.pos.x > ekplat - 10:
                self.pos.x = ekplat - 10

        self.rect.midbottom = self.pos # center...

    def animatev(self):

        now = pg.time.get_ticks()
        keys = pg.key.get_pressed()
        
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        #anime walking
        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_r)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image =self.walking_frames_r[self.current_frame]
                elif self.vel.x < 0:
                    self.image = self.walking_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if not self.sitting and not self.jumping and not self.atsitting and not self.walking:
            if now - self.last_update > 150: #uptdEEEEEEEEEEEEEE
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if self.veids == 1:
            if keys[pg.K_e]:
                if self.sitting == False:
                    self.last_update = 0
                self.sitting = True
            else:
                self.sitting = False
        if self.veids == 2:
            if keys[pg.K_o]:
                if self.sitting == False:
                    self.last_update = 0
                self.sitting = True
            else:
                self.sitting = False
        if self.sitting:
            now = pg.time.get_ticks()
            if now - self.last_update > 150: #uptdEEEEEEEEEEEEEE
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.sitting_frames)
                bottom = self.rect.bottom
                self.image = self.sitting_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if self.veids == 1:
            if keys[pg.K_s]:
                if self.atsitting == False:
                    self.last_update = 0
                self.atsitting = True
            else:
                self.atsitting = False
        if self.veids == 2:
            if keys[pg.K_k]:
                if self.atsitting == False:
                    self.last_update = 0
                self.atsitting = True
            else:
                self.atsitting = False
        if self.atsitting:
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.atsitting_frames)
                bottom = self.rect.bottom
                self.image = self.atsitting_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        self.mask = pg.mask.from_surface(self.image)

    def animatez(self):

        now = pg.time.get_ticks()
        keys = pg.key.get_pressed()

        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        #anime walking
        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_r)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image =self.walking_frames_r[self.current_frame]
                elif self.vel.x < 0:
                    self.image = self.walking_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if not self.sitting and not self.atsitting and not self.walking:
            if now - self.last_update > 150: #uptdEEEEEEEEEEEEEE
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        
        if self.veids == 1:
            if keys[pg.K_o]:
                if self.sitting == False:
                    self.last_update = 0
                self.sitting = True
            else:
                self.sitting = False
        if self.veids == 2:
            if keys[pg.K_e]:
                if self.sitting == False:
                    self.last_update = 0
                self.sitting = True
            else:
                self.sitting = False
        if self.sitting:
            if now - self.last_update > 150: #uptdEEEEEEEEEEEEEE
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.sitting_frames)
                bottom = self.rect.bottom
                self.image = self.sitting_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if self.veids == 1:
            if keys[pg.K_k]:
                if self.atsitting == False:
                    self.last_update = 0
                self.atsitting = True
            else:
                self.atsitting = False
        if self.veids == 2:
            if keys[pg.K_s]:
                if self.atsitting == False:
                    self.last_update = 0
                self.atsitting = True
            else:
                self.atsitting = False
        if self.atsitting:
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.atsitting_frames)
                bottom = self.rect.bottom
                self.image = self.atsitting_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        self.mask = pg.mask.from_surface(self.image)
        
    def jump(self):
        if self.rect.y > ekgar - 180:
            self.vel.y = -LECIENA_STIPRUMS


class Ball(pg.sprite.Sprite):
    def __init__(self, game, side):
        self._layer = BALL_LAYER
        self.game = game
        self.satre = False
        self.parsts = False
        self.saujas = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        pg.sprite.Sprite.__init__(self)
        self.image = self.stav[0]
        #self.image = pg.Surface((30, 30))
        #self.image.fill(BALTS)
        self.rect = self.image.get_rect()
        self.rect.center = (ekplat /2 , ekgar / 2)
        if side == 1:
            self.pos = vec(ekplat - ekplat / 8 , ekgar / 1.5)
        else:
            self.pos = vec(ekplat /8 , ekgar / 1.5)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
    
    def load_images(self):
        self.stav = [pg.image.load(path.join(self.game.img_folder, 'bumba1.png')).convert_alpha(), pg.image.load(path.join(self.game.img_folder, 'bumba2.png')).convert_alpha(), pg.image.load(path.join(self.game.img_folder, 'bumba3.png')).convert_alpha(), pg.image.load(path.join(self.game.img_folder, 'bumba4.png')).convert_alpha()]
    
    def update(self):
        self.animate()

        self.acc = vec(0, GRAVITYB)
        if TEST_MODE:
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT]:
                self.acc.x = -0.2
            if keys[pg.K_RIGHT]:
                self.acc.x = 0.2
            if keys[pg.K_UP]:
                self.jump()
            if keys[pg.K_DOWN]:
                self.vel.y = 50
        

        self.acc.x += self.vel.x * -0.008
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        if self.pos.x > ekplat - 10:
            self.vel.x *= -1
            self.vel.y -= 5
            self.pos.x -= 20       
        if self.pos.x < 0 :
            self.vel.x *= -1
            self.vel.y -= 5
            self.pos.x += 20
        if self.pos.y > 530:
            if self.pos.x < ekplat /2 + 40  and self.pos.x > ekplat /2 - 20:
                self.vel.x *= -1
                self.vel.y -= 5
        # hits = pg.sprite.spritecollide(self, self.game.tikls, False)
        #     self.vel.x *= -1

    def animate(self):
        now = pg.time.get_ticks()

        if not self.saujas:
            # if now - self.last_update > 50:
            if now - self.last_update > abs(200 - ((abs(self.vel.x) + abs(self.vel.y)) * 10)) and (abs(self.vel.x) + abs(self.vel.y)) > 1:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.stav)
                bottom = self.rect.bottom
                if self.vel.y < 0:
                    self.image = self.stav[self.current_frame]
                else:
                    self.image = self.stav[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        
        self.rect.midbottom = self.pos.x, self.pos.y
        self.mask = pg.mask.from_surface(self.image)
    def jump(self):
        self.vel.y = -LECIENA_STIPRUMS


class BallPrediction(pg.sprite.Sprite):
    def __init__(self, game, pos, vel):
        self.game = game
        self.stav = [pg.image.load(path.join(self.game.img_folder, 'bumba1.png')).convert_alpha()]
        pg.sprite.Sprite.__init__(self)
        self.image = self.stav[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = vec(pos)
        self.vel = vec(vel)
        
    
    def update(self):
        self.acc = vec(0, GRAVITYB)

        self.acc.x += self.vel.x * -0.008
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        if self.pos.x > ekplat - 10:
            self.vel.x *= -1
            self.vel.y -= 5
            self.pos.x -= 20       
        if self.pos.x < 0 :
            self.vel.x *= -1
            self.vel.y -= 5
            self.pos.x += 20
        if self.pos.y > 530:
            if self.pos.x < ekplat /2 + 40  and self.pos.x > ekplat /2 - 20:
                self.vel.x *= -1
                self.vel.y -= 5
                
        # hits = pg.sprite.spritecollide(self, self.game.tikls, False)
        # if hits:
        #     self.vel.x *= -1

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        self._layer = WALL_LAYER
        pg.sprite.Sprite.__init__(self)
        #images = [pg.image.load('beach1.png')]
        self.image = pg.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Tikls(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        self._layer = WALL_LAYER
        pg.sprite.Sprite.__init__(self)
        #images = [pg.image.load('beach1.png')]
        self.image = pg.Surface((w, h))
        self.image.fill(BALTS)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Cloud(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self, game.clouds)
        self.game = game
        self.load_images()
        self.speed = 1
        self.image = random.choice(self.makonis)# pg.image.load("cloud1.png")
        self.image.set_colorkey(MELNS)
        self.rect = self.image.get_rect()
        scale = random.randrange(50, 101) / 100
        self.image = pg.transform.scale(self.image, (int(self.rect.width * scale),int(self.rect.height * scale)))
        scale *= 100
        if scale < 65:
            self._layer = 0
            self.speed = 1
        if 80 > scale > 64:
            self._layer = 1
            self.speed = 0.5
        if scale > 89:
            self._layer = 3
            self.speed = 2
        self.pos = vec(-200, random.randrange(-50, 300))
        self.rect.y = self.pos.y
    def update(self):
        self.pos.x += self.speed
        self.rect.x = self.pos.x
        if self.rect.top > 1400:
            self.kill()

    def load_images(self):
        self.makonis = [pg.image.load(path.join(self.game.img_folder, 'cloud1.png')).convert_alpha(), pg.image.load(path.join(self.game.img_folder, 'cloud2.png')).convert_alpha(), pg.image.load(path.join(self.game.img_folder, 'cloud3.png')).convert_alpha()]

class Button(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, krasa, game, fill, clickfill):
        pg.sprite.Sprite.__init__(self)
        self.color = fill
        self.game = game
        self.krasa = krasa
        self.fill = fill
        self.clickfill = clickfill
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pg.Surface((self.w, self.h))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.last_click = 0


    def update(self):
        now = pg.time.get_ticks()

        (mousex, mousey) = pg.mouse.get_pos()
        self.image = pg.Surface((self.w, self.h))
        self.rect.x = self.x + 5
        self.rect.y = self.y + 5
        if mousex > self.rect.x and mousex < self.rect.x + self.w and mousey > self.rect.y and mousey < self.rect.y + self.h:
            self.game.onbutton = True
            self.image = pg.Surface((self.w+20, self.h+20))
            self.rect.x = self.x - 5
            self.rect.y = self.y - 5
            
            if pg.mouse.get_pressed()[0] == 1:
                
                if now - self.last_click > 500:
                    self.last_click = now

                    if self.krasa == 'disable':
                        if (self.game.disableEffects == False):
                            self.game.disableEffects = True
                        else:
                            self.game.disableEffects = False

                if self.krasa == 'play':
                    if pg.mouse.get_pressed()[0] == 1:
                        if (self.game.zaloskaits > 0 and self.game.violetoskaits > 0):
                            self.game.waiting = False
                        else:
                            ctypes.windll.user32.MessageBoxW(0, u"All teams should have atleast 1 player.", u"Team size error.", 0)

        self.image.fill(self.color)
        

class VoleyParticle(pg.sprite.Sprite):
    def __init__(self, x, y, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        # self.image = pg.Surface((10, 10))
        # self.image.fill(BALTS)
        self.image = random.choice([pg.image.load('bumba1.png'), pg.image.load('bumba2.png'), pg.image.load('bumba3.png'), pg.image.load('bumba4.png')])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = vec(0, 0)
        self.pos = vec(x - 10, y - 10)
        self.vel.x = random.choice([-10,-5,-2,-1,0,1,2,5,10])

    def update(self):
        self.vel.y += 1
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        if self.pos.y > ekgar + 50 :
            self.kill()
        if self.pos.x < 0:
            self.vel.x *= -1
            self.pos.x = 5
        if self.pos.x > ekplat - 15:
            self.vel.x *= -1
            self.pos.x = ekplat - 15


class PhysicsButton(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, krasa, game, greenfill, purplefill, nonefill):
        pg.sprite.Sprite.__init__(self)
        if y < 210:
            self.color = nonefill
        else:
            if x > ekplat / 2:
                self.color = greenfill
            else:
                self.color = purplefill
        self.game = game
        self.krasa = krasa
        self.greenfill = greenfill
        self.purplefill = purplefill
        self.nonefill = nonefill
        self.w = w
        self.h = h
        self.image = pg.Surface((self.w, self.h))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.bijpos = self.pos
        self.bijnospiests = False

    def update(self):
        self.acc = vec(0, GRAVITY)

        (mousex, mousey) = pg.mouse.get_pos()
        if ((mousex > self.rect.x and mousex < self.rect.x + self.w and mousey > self.rect.y and mousey < self.rect.y + self.h) or (self.bijnospiests == True )) and pg.mouse.get_pressed()[0] == 1 and self.game.ir_kads_nospiests == False:
            self.bijnospiests = True
            self.game.ir_kads_nospiests = True
            for e in self.game.phisics_buttons:
                if e.pos != self.pos:
                    if self.pos.x < e.pos.x + e.w and self.pos.x + self.w > e.pos.x and self.pos.y + self.h > e.pos.y and self.pos.y < e.pos.y + e.h:
                        if e.pos.x < self.pos.x:
                            e.vel.x -= random.randint(1, 3)
                        else:
                            e.vel.x -= random.randint(-3, 1)
                        if e.pos.y < self.pos.y:
                            e.vel.y += random.randint(1, 3)
                        else:
                            e.vel.y += random.randint(1, 3)
            # if abs(self.pos.x + self.w / 2 - mousex) + abs(self.pos.y + self.h / 2 - mousey) < 30:
            self.vel = vec(0, 0)
            self.acc = vec(0, 0)
            self.pos = vec(mousex - self.w / 2, mousey - self.h / 2)
        elif pg.mouse.get_pressed()[0] == 0 and self.bijnospiests == True:
            self.bijnospiests = False
            self.game.ir_kads_nospiests = False
            self.vel.x -= (self.pos.x + self.w / 2 - mousex) / 2
            self.vel.y -= (self.pos.y + self.h / 2 - mousey) / 2
        else:
            self.bijnospiests = False
            self.game.ir_kads_nospiests = False

        
        for e in self.game.phisics_buttons:
            if e.pos != self.pos:
                if self.rect.colliderect(e.rect):
                    if abs(self.vel.x) > 0.2:
                        if e.pos.x < self.pos.x:
                            if self.krasa == "p1" or self.krasa == "p2":
                                if e.krasa == "p1" or e.krasa == "p2":
                                    e.vel.x -= 1
                                else:
                                    e.vel.x -= 5
                            else:
                                if e.krasa == "p1" or e.krasa == "p2":
                                    e.vel.x -= 1
                                else:
                                    e.vel.x -= 1
                        else:
                            if self.krasa == "p1" or self.krasa == "p2":
                                if e.krasa == "p1" or e.krasa == "p2":
                                    e.vel.x += 1
                                else:
                                    e.vel.x += 5
                            else:
                                if e.krasa == "p1" or e.krasa == "p2":
                                    e.vel.x += 1
                                else:
                                    e.vel.x += 1
                    if e.pos.y < self.pos.y:
                        if self.krasa == "p1" or self.krasa == "p2":
                            if e.krasa == "p1" or e.krasa == "p2":
                                e.vel.y -= 1
                            else:
                                e.vel.y -= 5
                        else:
                            if self.vel.y < -1:
                                if e.krasa == "p1" or e.krasa == "p2":
                                    e.vel.y -= 1
                                else:
                                    e.vel.y -= 1
                    else:
                        if self.krasa == "p1" or self.krasa == "p2":
                            if e.krasa == "p1" or e.krasa == "p2":
                                e.vel.y += 1
                            else:
                                e.vel.y += 5
                        else:
                            if e.krasa == "p1" or e.krasa == "p2":
                                e.vel.y += 1
                            else:
                                e.vel.y += 1

        self.acc.x += self.vel.x * GROUND_FRICTION
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        if abs(self.vel.y) < 0.1:
            self.vel.y = 0
        self.pos += self.vel + 0.5 * self.acc

        hits = self.rect.colliderect(self.game.balsts.rect)
        if hits:
            if self.vel.y > 0:
                self.pos.y = self.game.balsts.rect.y - self.h + 1
                self.vel.y = 0
                
            # if self.vel.y < 0:
            #     self.vel.y /= 2
            # self.vel.y *= -1
        

        if self.pos.y > ekgar - 70 - self.h:
            self.pos.y = ekgar - 70 - self.h
            if abs(self.vel.y < 5):
                self.vel.y = 0
            else:
                self.vel.y /= 2
                self.vel.y *= -1
                
        if self.pos.y < 0:
            self.pos.y = 0
            self.vel.y = self.vel.y - self.vel.y / 4
            self.vel.y *= -1

        if self.pos.x > ekplat - self.w:
            self.pos.x = ekplat - self.w
            self.vel.x /= 2
            self.vel.x *= -1

        if self.pos.x < 0:
            self.pos.x = 0
            self.vel.x /= 2
            self.vel.x *= -1

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        if self.pos.y < 210:
            self.color = self.nonefill
        else:
            if self.pos.x + self.w / 2 + 5> ekplat / 2:
                self.color = self.greenfill
            else:
                self.color = self.purplefill
        self.image.fill(self.color)