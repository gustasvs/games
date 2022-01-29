import pygame as pg
from settings import *
vec = pg.math.Vector2
from tilemap import collide_hit_rect
from os import path
import random
import math
from functions import *

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


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_images()
        self.image = game.Player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = pg.Rect(0, 0, 30, 30).copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.rot = 180
        self.mousex, self.mousey = 0, 0
        self.mana = PLAYER_MANA
        self.can_tp = True

    def update(self):
        if self.mana < PLAYER_MANA // 4:
            self.can_tp = False
        else:
            self.can_tp = True

        if self.mana < PLAYER_MANA:
            self.mana += ADD_MANA_SPEED
        self.mousex, self.mousey = pg.mouse.get_pos()
        if distance((self.mousex, self.mousey), self.pos) > 15:
            #self.rot = (angle_between(self.pos, (self.mousex + abs(self.game.camera.x), self.mousey + abs(self.game.camera.y))) + 180) % 360
            self.rot = (angle_between(self.pos, (self.mousex, self.mousey)) + 180) % 360
        self.image = pg.transform.rotate(self.game.Player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        now = pg.time.get_ticks()
        hits = pg.sprite.spritecollide(self, self.game.finish, False, collide_hit_rect)
        if hits or len(self.game.ai) == 0:
            self.game.playing = False
        self.acc = vec(1, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        self.animate()
        hits = pg.sprite.spritecollide(self, self.game.ai, False, pg.sprite.collide_mask)
        if hits and hits[0].seen_player == False:
            self.rot = (hits[0].pos - self.pos).angle_to(vec(1,0 ))
            hits[0].die()
            self.game.score += 10
            self.vel = vec(-KNOKBACK, 0).rotate(-self.rot)
            for enemy in self.game.ai:
                if enemy.can_see_player():
                    enemy.rot = (self.pos - enemy.pos).angle_to(vec(1, 0))
        self.mask = pg.mask.from_surface(self.image)
    
    def animate(self):
        pass

    def load_images(self):
        pass

    def can_move_to(self, x, y):
        line_of_sight = get_line((int(x), int(y)), (int(self.pos.x), int(self.pos.y)))
        for p in range(1,len(line_of_sight),5):
            for a in self.game.ai:
                if distance((x, y), a.pos) < 50 and a.seen_player == True:
                    return False
                # elif a.rect.collidepoint(line_of_sight[x]):
                    
            for w in self.game.walls:
                if w.rect.collidepoint(line_of_sight[p]):
                    return False
        return True
    
    def add_mana(self, amount):
        self.mana += amount
        if self.mana > PLAYER_MANA:
            self.mana = PLAYER_MANA

    def dur(self):
        dir = vec(1, 0).rotate(-self.rot)
        pos = self.pos + Naza_OFFSET.rotate(-self.rot)
        Nazis(self.game, pos, dir)
        self.vel = vec(1, 0).rotate(-self.rot)


class Pointman(pg.sprite.Sprite):
    def __init__(self, game, x, y, dirr):
        self.groups = game.all_sprites, game.ai
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = True
        self.saujing = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.seen_player = False
        self.pos = vec(x, y)
        self.image = self.walking_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect = pg.Rect(0, 0, 64, 64).copy()
        self.hit_rect.center = self.rect.center
        self.last_shot = 0
        self.griesanaas = 0
        self.vel = vec(0, 0)
        if dirr == 1:
            self.rot = 90
        if dirr == 2:
            self.rot = 270
        if dirr == 3:
            self.rot = 180
        if dirr == 4:
            self.rot = 0
        self.puse = random.randint(0, 1)

    def update(self):
        self.collide_walls()
        self.animate()
        now = pg.time.get_ticks()
        self.rot_uz_spel = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        # ja speletajs ir redzeslokaa
        if self.can_see_player() and ((self.rot - self.rot_uz_spel) % 360 < pointman_fov or (self.rot - self.rot_uz_spel) % 360 > 360 - pointman_fov):
            self.seen_player = True
            self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
            self.griesanaas = now
            if now - self.last_shot > pointman_lodes_BIEZUMS:
                self.last_shot = now
                self.sauj()
        else:
            self.vel = vec(0.5, 0).rotate(-self.rot)
            self.seen_player = False
            # if now - self.griesanaas > 2000:
            #     self.griesanaas = now
            #     if self.puse == 0:
            #         self.rot = (self.rot + 180) % 360
            #     if self.puse == 1:
            #         self.rot = (self.rot - 180) % 360
        # self.rect.center = self.pos
         #self.avoid_ai()
        self.pos += self.vel
        

        self.rect.center = self.hit_rect.center

    def animate(self):
        now = pg.time.get_ticks()
        self.walking = True
        #anime walking
        if self.walking:
            if now - self.last_update > 20:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames)
                self.image = self.walking_frames[self.current_frame]
                self.image = pg.transform.scale(self.image, (pointman_scale, pointman_scale))
                self.image = pg.transform.rotate(self.image, self.rot)
                self.rect = self.image.get_rect()
                self.hit_rect.center = self.pos
            
        self.mask = pg.mask.from_surface(self.image)

    def collide_walls(self):
        self.hit_rect.centerx = self.pos.x
        hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
        if hits:    
            if self.seen_player == False:
                self.rot = (self.rot + 180) % 360
            if self.vel.x > 0:
                self.pos.x = hits[0].rect.left - self.hit_rect.width / 2
            if self.vel.x < 0:
                self.pos.x = hits[0].rect.right + self.hit_rect.width / 2
            self.vel.x = 0
            self.hit_rect.centerx = self.pos.x
        self.hit_rect.centery = self.pos.y
        hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
        if hits:
            if self.seen_player == False:
                self.rot = (self.rot + 180) % 360
            if self.vel.y > 0:
                self.pos.y = hits[0].rect.top - self.hit_rect.height / 2
            if self.vel.y < 0:
                self.pos.y = hits[0].rect.bottom + self.hit_rect.height / 2
            self.vel.y = 0
            self.hit_rect.centery = self.pos.y

    def load_images(self):
        self.walking_frames = [pg.image.load(path.join(self.game.img_folder, 'pointman_walking_1.png')).convert_alpha(), 
                              pg.image.load(path.join(self.game.img_folder, 'pointman_walking_2.png')).convert_alpha(), 
                              pg.image.load(path.join(self.game.img_folder, 'pointman_walking_3.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'pointman_walking_4.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'pointman_walking_5.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'pointman_walking_6.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'pointman_walking_7.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'pointman_walking_8.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'pointman_walking_9.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'pointman_walking_10.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'pointman_walking_11.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'pointman_walking_12.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'pointman_walking_13.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'pointman_walking_14.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'pointman_walking_15.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'pointman_walking_16.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'pointman_walking_17.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'pointman_walking_18.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'pointman_walking_19.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'pointman_walking_20.png')).convert_alpha(),]
        # self.saujing_frames = [pg.image.load('')]

    def sauj(self):
        dir = vec(1, 0).rotate(-self.rot)
        pos = self.pos + pointman_lodes_OFFSET.rotate(-self.rot)
        Lode(self.game, pos, dir)
        self.vel = vec(1, 0).rotate(-self.rot)

    def die(self):
        self.kill()

    def avoid_ai(self):
        for labais in self.game.ai:
            if labais != self:
                dist = self.pos - labais.pos
                if 0 < dist.length() < avoid_radius:
                    self.vel += dist.normalize()

    def can_see_player(self):
        line_of_sight = get_line((int(self.game.player.pos.x), int(self.game.player.pos.y)), (int(self.pos.x), int(self.pos.y)))
        for x in range(1,len(line_of_sight),5):
            for w in self.game.walls:
                if w.rect.collidepoint(line_of_sight[x]):
                    return False
        #if distance(self.game.player.pos, self.pos) > pointman_redzamiba:
            #return False
        return True


class Gunman(pg.sprite.Sprite):
    def __init__(self, game, x, y, dirr):
        self.groups = game.all_sprites, game.ai
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = True
        self.saujing = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.seen_player = False
        self.pos = vec(x, y)
        self.image = self.walking_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect = pg.Rect(0, 0, 64, 64).copy()
        self.hit_rect.center = self.rect.center
        self.last_shot = 0
        self.griesanaas = 0
        self.vel = vec(0, 0)
        if dirr == 1:
            self.rot = 90
        if dirr == 2:
            self.rot = 270
        if dirr == 3:
            self.rot = 0
        if dirr == 4:
            self.rot = 180
        self.puse = random.randint(0, 1)

    def update(self):
        self.collide_walls()
        self.animate()
        now = pg.time.get_ticks()
        self.rot_uz_spel = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        # ja speletajs ir redzeslokaa
        if self.can_see_player() and ((self.rot - self.rot_uz_spel) % 360 < gunman_fov or (self.rot - self.rot_uz_spel) % 360 > 360 - gunman_fov):
            self.seen_player = True
            self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
            self.griesanaas = now
            if now - self.last_shot > gunman_lodes_BIEZUMS:
                self.last_shot = now
                self.sauj()
        else:
            self.seen_player = False
            if now - self.griesanaas > 3000:
                self.griesanaas = now
                self.puse += 1
                if self.puse == 2:
                    self.puse = 0
            if self.puse == 0:
                self.rot = (self.rot + 0.3) % 360
            if self.puse == 1:
                self.rot = (self.rot - 0.3) % 360

        self.vel = vec(0.5, 0).rotate(-self.rot)
        self.pos += self.vel
        

        self.rect.center = self.hit_rect.center

    def animate(self):
        now = pg.time.get_ticks()
        self.walking = True
        #anime walking
        if self.walking:
            if now - self.last_update > 20:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames)
                self.image = self.walking_frames[self.current_frame]
                self.image = pg.transform.scale(self.image, (161, 103))
                self.image = pg.transform.rotate(self.image, self.rot)
                self.rect = self.image.get_rect()
                self.hit_rect.center = self.pos
            
        self.mask = pg.mask.from_surface(self.image)

    def collide_walls(self):
        self.hit_rect.centerx = self.pos.x
        hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
        if hits:    
            if self.seen_player == False:
                self.rot = (self.rot + 180) % 360
            if self.vel.x > 0:
                self.pos.x = hits[0].rect.left - self.hit_rect.width / 2
            if self.vel.x < 0:
                self.pos.x = hits[0].rect.right + self.hit_rect.width / 2
            self.vel.x = 0
            self.hit_rect.centerx = self.pos.x
        self.hit_rect.centery = self.pos.y
        hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
        if hits:
            if self.seen_player == False:
                self.rot = (self.rot + 180) % 360
            if self.vel.y > 0:
                self.pos.y = hits[0].rect.top - self.hit_rect.height / 2
            if self.vel.y < 0:
                self.pos.y = hits[0].rect.bottom + self.hit_rect.height / 2
            self.vel.y = 0
            self.hit_rect.centery = self.pos.y

    def load_images(self):
        self.walking_frames = [pg.image.load(path.join(self.game.img_folder, 'gunman_walking_1.png')).convert_alpha(), 
                              pg.image.load(path.join(self.game.img_folder, 'gunman_walking_2.png')).convert_alpha(), 
                              pg.image.load(path.join(self.game.img_folder, 'gunman_walking_3.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'gunman_walking_4.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'gunman_walking_5.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'gunman_walking_6.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'gunman_walking_7.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'gunman_walking_8.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'gunman_walking_9.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'gunman_walking_10.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'gunman_walking_11.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'gunman_walking_12.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'gunman_walking_13.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'gunman_walking_14.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'gunman_walking_15.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'gunman_walking_16.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'gunman_walking_17.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'gunman_walking_18.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'gunman_walking_19.png')).convert_alpha(),
                              pg.image.load(path.join(self.game.img_folder, 'gunman_walking_20.png')).convert_alpha(),]
        #self.saujing_frames = [pg.image.load('')]

    def sauj(self):
        dir = vec(1, 0).rotate(-self.rot)
        pos = self.pos + gunman_lodes_OFFSET.rotate(-self.rot)
        Lode(self.game, pos, dir)
        self.vel = vec(1, 0).rotate(-self.rot)

    def die(self):
        self.kill()

    def avoid_ai(self):
        for labais in self.game.ai:
            if labais != self:
                dist = self.pos - labais.pos
                if 0 < dist.length() < avoid_radius:
                    self.vel += dist.normalize()

    def can_see_player(self):
        line_of_sight = get_line((int(self.game.player.pos.x), int(self.game.player.pos.y)), (int(self.pos.x), int(self.pos.y)))
        for x in range(1,len(line_of_sight),5):
            for w in self.game.walls:
                if w.rect.collidepoint(line_of_sight[x]):
                    return False
        return True


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Lode(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.lodes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = game.Lode_img
        self.game = game
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * lodes_SPEED
        self.spawn_time = pg.time.get_ticks()
        #if pg.sprite.spritecollideany(self, self.game.walls):
            
    def update(self):
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        if self.game.paused == False:
            if pg.sprite.spritecollideany(self, self.game.walls):
                self.kill()
            self.pos += self.vel * self.game.dt
            self.rect.center = self.pos
            #if pg.time.get_ticks() - self.spawn_time > lodes_LIFETIME:
                #self.kill()
        
        self.mask = pg.mask.from_surface(self.image)


class Nazis(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = game.Naza_img
        self.game = game
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * Naza_SPEED
        self.spawn_time = pg.time.get_ticks()
            
    def update(self):
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        if self.game.paused == False:
            if pg.sprite.spritecollideany(self, self.game.walls):
                self.kill()
            self.pos += self.vel * self.game.dt
            self.rect.center = self.pos
            if pg.time.get_ticks() - self.spawn_time > Naza_LIFETIME:
                self.kill()
        
        self.mask = pg.mask.from_surface(self.image)


class Finish(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.finish
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y