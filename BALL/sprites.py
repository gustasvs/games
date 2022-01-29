import pygame as pg
from random import uniform, choice, randint, random
from settings import *
from tilemap import collide_hit_rect
import pytweening as tween
from math import sin, cos, pi, atan2, hypot
vec = pg.math.Vector2

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

def get_angle(origin, destination):
    x_dist = destination[0] - origin[0]
    y_dist = destination[1] - origin[1]
    return atan2(-y_dist, x_dist) % (2 * pi)

def project(pos, angle, distance):
    """Returns tuple of pos projected distance at angle
    adjusted for pygame's y-axis.
    """
    return (pos[0] + (cos(angle) * distance),
            pos[1] - (sin(angle) * distance))

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.speed = PLAYER_SPEED
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.last_shot = 0
        self.mana = PLAYER_MANA
        self.slowmo = False

    def update(self):
        x, y = pg.mouse.get_pos()
        self.distaa = hypot(self.pos.x - x, self.pos.y - y)
        #print(round(self.distaa), self.speed)
        if self.distaa > 5:
            self.angle = get_angle(self.pos, pg.mouse.get_pos())
            self.pos = project(self.pos, self.angle, self.speed)
        if self.distaa < 25 and self.distaa > 5:
            self.speed = 2
        if self.distaa < 75 and self.distaa > 25:
            self.speed = 3
        if self.distaa < 275 and self.distaa > 75:
            self.speed = 4
        if self.distaa > 275:
            self.speed = 5
        if self.slowmo:
            self.speed = 1.5 
        self.rect.center = self.pos
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        self.mask = pg.mask.from_surface(self.image)
    def add_mana(self, amount):
        self.mana += amount
        if self.mana > PLAYER_MANA:
            self.mana = PLAYER_MANA

class WaterBall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.WaterBalls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.speed = choice(MOB_SPEEDS)
        self.game = game
        self.AVOID_RADIUS = AVOID_RADIUS
        if self.speed > 150:
            self.image = game.WaterBall_img[0]
        elif self.speed < 150:
            self.AVOID_RADIUS *= 4
            self.image = game.WaterBall_img[1]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH
        self.target = game.player
        self.updatee = 0
        self.current_frame = 0
        

    def avoid_BALLS(self):
        for mob in self.game.WaterBalls:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < self.AVOID_RADIUS:
                    self.acc += dist.normalize()
    def avoid_BIGBALLS(self):
        for mob in self.game.WaterBalls:
            if mob != self:
                if mob.speed < 150:
                    dist = self.pos - mob.pos
                    if 0 < dist.length() < 10:
                        self.acc += dist.normalize()

    def update(self):
        #print(self.acc, "A")
        target_dist = self.target.pos - self.pos
        self.rot = target_dist.angle_to(vec(1, 0))
        self.rect.center = self.pos
        self.acc = vec(1, 0).rotate(-self.rot)
        if self.speed > 150:
            self.avoid_BALLS()
        else:
            self.avoid_BIGBALLS()
        self.acc.normalize_ip()
        self.acc.scale_to_length(self.speed)
        #print(self.acc)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.kill()
        self.mask = pg.mask.from_surface(self.image)

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


class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self._layer = ITEMS_LAYER
        if type != 'baze':
            self.groups = game.all_sprites, game.items, game.particles
        if type == 'baze':
            self.groups = game.items, game.particles

        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.pos = pos
        self.rect.center = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        # bobbing motion
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1

class Particle(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self, (game.all_sprites, game.particles))
        self.game = game
        self.image = choice(game.Particle_img)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.spawn_time = pg.time.get_ticks()
        self.update_time = pg.time.get_ticks()
    def update(self):
        rando = randint(1, 4)
        if rando == 1:
            self.pos.x += 1
        if rando == 2:
            self.pos.x -= 1
        if rando == 3:
            self.pos.y -= 1
        if rando == 4:
            self.pos.y += 1
        ex, ey = self.image.get_size()
        now = pg.time.get_ticks()
        if now - self.update_time > 100:
            self.update_time = now
            self.image= pg.transform.scale(self.image, (ex - 5, ey - 5))
        if now - self.spawn_time > PARTICLE_LIFETIME:
            self.kill()
        self.rect.center = self.pos


