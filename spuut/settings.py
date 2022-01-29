import pygame as pg
vec = pg.math.Vector2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)
MELNS = (0, 0, 0)
FONT_NAME = 'GROBOLD'

# game settings
ekplat = 576   # 16 * 64 or 32 * 32 or 64 * 16
ekgar = 1152 #768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "spuut"
BGCOLOR = WHITE
GRAVITY = 0.2


TILESIZE = 64
GRIDWIDTH = ekplat / TILESIZE
GRIDHEIGHT = ekgar / TILESIZE

WALL_IMG = 'tileGreen_39.png'
PARTICLE_IMG = 'Particle.png'
PARTICLE_LIFETIME = 10000

# Player settings
PLAYER_MANA = 200
PLAYER_SPEED = 3
ADD_MANA_SPEED = 2
ADD_MANA = 20
PLAYER_ACC = 0.4
PLAYER_FRICTION = -0.15

PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)


WATERBALL_IMG = 'WaterBall.png'
MOB_SPEEDS = [499, 300, 400, 500, 499, 300, 400, 500, 499, 300, 400, 500, 100]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
AVOID_RADIUS = 40

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# Items
ITEM_IMAGES = {'boom': 'boom.png',
                'baze': 'whitePuff15.png'}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 15
BOB_SPEED = 0.4

# Sounds
BG_MUSIC = 'espionage.ogg'