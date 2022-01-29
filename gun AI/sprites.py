from settings import *
import pygame as pg
import numpy
import random
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER
        self.last_shot = 0
        self.game = game
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30, 70))
        self.image.fill(MELNS)
        self.rect = self.image.get_rect()
        self.rect.center = (ekplat /2 , ekgar / 2)
        self.pos = vec(ekplat /4 , ekgar / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
    def jump(self):
        #print(self.pos.y)
        if self.pos.y >= ekgar - 180:
            self.vel.y = -LECIENA_STIPRUMS
    def update(self):
        #print(self.vel)
        #self.animate()
        self.acc = vec(0, GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        
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


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        self._layer = PLATLAYER
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(ZALS)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Lode(pg.sprite.Sprite):    
    def __init__(self, game, x, y, dir):
        self._layer = LODLAYER
        self.dir = dir
        self.groups = game.all_sprites, game.lodes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game= game
        self.image = pg.Surface((10, 10))
        self.image.fill(MELNS)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(self.rect.x , self.rect.y)
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if self.dir == 1:
            self.rect.x += 10
        else:
            self.rect.x -= 10
        if self.rect.x < -20 or self.rect.x > ekplat - 20 :
            self.kill()


class Enemy(pg.sprite.Sprite):
    def __init__(self, game, dir, LODES_ATSITIENS):
        #self.dir = dir
        self.LODES_ATSITIENS = LODES_ATSITIENS
        self._layer = MLAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((random.choice([30]), random.choice([100,100,100,100,100,100,10])))
        self.image.fill(ENE_KRASA)
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([ekplat -100, 100])
        self.rect.y = 300
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(self.rect.x , self.rect.y)
        if self.rect.x == ekplat - 100 :
            self.dir = 1
        if self.rect.x == 100 :
            self.dir = -1
    def update(self):
        self.acc = vec(0, GRAVITY)
        if self.dir == -1:
            if self.vel.x < 5:
                self.vel.x += ENE_SPEED
        if self.dir == 1:
            if self.vel.x > -5:
                self.vel.x -= ENE_SPEED
        if self.rect.y > 1000 :
            self.kill()
        
        # kustibas apr
        self.vel += self.acc
        
        self.pos += self.vel + 0.5 * self.acc
        
        if self.pos.x > ekplat:
            self.pos.x = ekplat
        if self.pos.x < 0:
            self.pos.x = 0
        self.rect.midbottom = self.pos
        if self.pos.y >= ekgar - 170:
            
            hits = pg.sprite.spritecollide(self, self.game.platforms1, False)
            if hits:
                self.pos.y = hits[0].rect.top
                self.vel.y = 0
        hits = pg.sprite.spritecollide(self, self.game.lodes, False)
        if hits:
            if hits[0].dir == 1:
                #print(hits[0])
                self.vel.x += self.LODES_ATSITIENS
            if hits[0].dir == -1:
                self.vel.x -= self.LODES_ATSITIENS
            hits[0].kill()
            
        #self.mask = pg.mask.from_surface(self.image)