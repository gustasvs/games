import pygame as pg
from settings import *
vec = pg.math.Vector2
from tilemap import collide_hit_rect
import random

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vel.x > 0:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if sprite.vel.x < 0:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y



class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * Tilesize
        self.rect.y = y * Tilesize


class Barb(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.barbs, game.labie
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.barb_img
        self.rect = self.image.get_rect()
        self.hit_rect = pg.Rect(0, 0, 30, 30).copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * Tilesize
        self.mob_timer = 0
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
    def avoid_labos(self):
        for labais in self.game.labie:
            if labais != self:
                dist = self.pos - labais.pos
                if 0 < dist.length() < avoid_radius:
                    self.acc += dist.normalize()

    def update(self):
        #self.rot = (mob_hits[0]- self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.game.barb_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        now = pg.time.get_ticks()
        
        if self.game.saak:
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_labos()
            if self.acc != 0:
                self.acc.scale_to_length(barb_speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
            if now - self.mob_timer > random.choice([0.1]):
                self.mob_timer = now
                self.rot += random.randint(-1, 1)
            hits = pg.sprite.spritecollide(self, self.game.kreisie, False, pg.sprite.collide_mask)
            if hits:
                self.rot = (hits[0].pos - self.pos).angle_to(vec(1,0 ))
                self.vel = vec(-KNOKBACK, 0).rotate(-self.rot)
            self.mask = pg.mask.from_surface(self.image)
            hits1 = pg.sprite.spritecollide(self, self.game.bultas, False, pg.sprite.collide_mask)
            if hits1:
                self.kill()




class Barb1(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.barbs1, game.kreisie
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.barb1_img
        self.rect = self.image.get_rect()
        self.hit_rect = pg.Rect(0, 0, 30, 30).copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * Tilesize
        self.mob_timer = 0
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 180
    def avoid_kreisos(self):
        for kreisais in self.game.labie:
            if kreisais != self:
                dist = self.pos - kreisais.pos
                if 0 < dist.length() < avoid_radius:
                    self.acc += dist.normalize()
    def update(self):
        #self.rot = (mob_hits[0]- self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.game.barb1_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        now = pg.time.get_ticks()
        
        if self.game.saak:
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_kreisos()
            if self.acc != vec(0, 0):
                self.acc.scale_to_length(barb_speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
            if now - self.mob_timer > random.choice([0.1]):
                self.mob_timer = now
                self.rot += random.randint(-1, 1)
            hits = pg.sprite.spritecollide(self, self.game.labie, False, pg.sprite.collide_mask)
            if hits:
                self.rot = (hits[0].pos - self.pos).angle_to(vec(1,0 ))
                self.vel = vec(-KNOKBACK, 0).rotate(-self.rot)
            self.mask = pg.mask.from_surface(self.image)
            hits1 = pg.sprite.spritecollide(self, self.game.bultas1, False, pg.sprite.collide_mask)
            if hits1:
                self.kill()

class Bonds(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.labie
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bond_img
        self.rect = self.image.get_rect()
        self.hit_rect = pg.Rect(0, 0, 30, 30).copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * Tilesize
        self.mob_timer = 0
        self.last_shot = 0
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
    def avoid_labos(self):
        for labais in self.game.labie:
            if labais != self:
                dist = self.pos - labais.pos
                if 0 < dist.length() < avoid_radius:
                    self.acc += dist.normalize()

    def update(self):
        #self.rot = (mob_hits[0]- self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.game.bond_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        now = pg.time.get_ticks()
        now1 = pg.time.get_ticks()
        
        if self.game.saak:
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_labos()
            if now1 - self.last_shot > BULTAS_BIEZUMS:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + BULTAS_OFFSET.rotate(-self.rot)
                Bulta1(self.game, pos, dir)
                self.vel = vec(1, 0).rotate(-self.rot)
            if self.acc != 0:
                self.acc.scale_to_length(barb_speed /2)
            self.acc += self.vel * -10
            self.vel += (self.acc /20) * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
            if now - self.mob_timer > random.choice([0.1]):
                self.mob_timer = now
                self.rot += random.randint(-1, 1)
            hits = pg.sprite.spritecollide(self, self.game.kreisie, False, pg.sprite.collide_mask)
            if hits:
                self.rot = (hits[0].pos - self.pos).angle_to(vec(1,0 ))
                self.vel = vec(-KNOKBACK, 0).rotate(-self.rot)
            loki = pg.sprite.spritecollide(self, self.game.kreisie, False, collided = pg.sprite.collide_circle_ratio(2.0))
            if loki:
                self.rot = (loki[0].pos - self.pos).angle_to(vec(1,0 ))
            self.mask = pg.mask.from_surface(self.image)
            #if pg.sprite.spritecollideany(self, self.game.walls):
            hits1 = pg.sprite.spritecollide(self, self.game.bultas, False, pg.sprite.collide_mask)
            if hits1:
                self.kill()
                
    

class Bonds1(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.kreisie
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bond1_img
        self.rect = self.image.get_rect()
        self.hit_rect = pg.Rect(0, 0, 30, 30).copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * Tilesize
        self.mob_timer = 0
        self.last_shot = 0
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 180
    def avoid_kreisos(self):
        for kreisais in self.game.labie:
            if kreisais != self:
                dist = self.pos - kreisais.pos
                if 0 < dist.length() < avoid_radius:
                    self.acc += dist.normalize()

    def update(self):
        #self.rot = (mob_hits[0]- self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.game.bond1_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        now = pg.time.get_ticks()
        now1 = pg.time.get_ticks()
        if self.game.saak:
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_kreisos()
            if now1 - self.last_shot > BULTAS_BIEZUMS:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + BULTAS_OFFSET.rotate(-self.rot)
                Bulta(self.game, pos, dir)
            #if self.acc != 0:
                #self.acc.scale_to_length(barb_speed /2)
            self.acc += self.vel * -10
            self.vel += (self.acc /20) * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
            if now - self.mob_timer > random.choice([0.1]):
                self.mob_timer = now
                self.rot += random.randint(-1, 1)
            hits = pg.sprite.spritecollide(self, self.game.labie, False, pg.sprite.collide_mask)
            if hits:
                self.rot = (hits[0].pos - self.pos).angle_to(vec(1,0 ))
                self.vel = vec(-KNOKBACK, 0).rotate(-self.rot)
            loki = pg.sprite.spritecollide(self, self.game.labie, False, collided = pg.sprite.collide_circle_ratio(2.0))
            if loki:
                self.rot = (loki[0].pos - self.pos).angle_to(vec(1,0 ))
            self.mask = pg.mask.from_surface(self.image)
            hits1 = pg.sprite.spritecollide(self, self.game.bultas1, False, pg.sprite.collide_mask)
            if hits1:
                self.kill()


class Bulta(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.labie, game.bultas
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = game.bulta_img
        self.game = game
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * BULTAS_SPEED
        self.spawn_time = pg.time.get_ticks()
        #if pg.sprite.spritecollideany(self, self.game.walls):
            
    def update(self):
        #self.image = pg.transform.rotate(self.game.bond1_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        if self.game.saak:
            #if pg.sprite.spritecollideany(self, self.game.walls):
                #self.kill()
            self.pos += self.vel * self.game.dt
            self.rect.center = self.pos
            #if pg.time.get_ticks() - self.spawn_time > BULTAS_LIFETIME:
                #self.kill()
            #hits = pg.sprite.spritecollide(self, self.game.labie, False, pg.sprite.collide_mask)
            #if hits:
        
        self.mask = pg.mask.from_surface(self.image)


class Bulta1(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.kreisie, game.bultas1
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = game.bulta_img
        self.game = game
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * BULTAS_SPEED
        self.spawn_time = pg.time.get_ticks()
    def update(self):
        #self.image = pg.transform.rotate(self.game.bond1_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        if self.game.saak:
            #if pg.sprite.spritecollideany(self, self.game.walls):
                #self.kill()
            self.pos += self.vel * self.game.dt
            self.rect.center = self.pos
            #if pg.time.get_ticks() - self.spawn_time > BULTAS_LIFETIME:
                #self.kill()
            
            
        
        self.mask = pg.mask.from_surface(self.image)
                

    