# SETINGI
import pygame as pg
vec = pg.math.Vector2

ekplat = 1216
ekgar = 768
Tilesize = 64
FPS = 60
VARDS = "Hitmn"
FONT_NAME = 'GROBOLD'
WALL_IMG = 'wall.png'#  'tile_06.png'
ILGUMS = 100

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

Player_img = 'Player.png'
PLAYER_MANA = 200
ADD_MANA_SPEED = 2
ADD_MANA = 20
KNOKBACK = 100

pointman_fov = 90
pointman_redzamiba = 200
pointman_scale = 96
pointman_lodes_OFFSET = vec(50, 25)
pointman_lodes_BIEZUMS = 200
gunman_fov = 120
gunman_redzamiba = 200
gunman_scale = 96
gunman_lodes_OFFSET = vec(50, 25)
gunman_lodes_BIEZUMS = 100
avoid_radius = 5

lodes_IMG = "Lode.png"
lodes_LIFETIME = 1000
lodes_SPEED = 500


Naza_IMG = "Lode.png"
Naza_LIFETIME = 1000
Naza_SPEED = 200
Naza_OFFSET = vec(0, 0)

LIGHTBLUE = (135, 206, 250)
MELNS = (0, 0, 0)
ORANDZS = (255, 140, 0)
BALTS = (255, 255, 255)
VIOLETS = (128, 0, 128)
SMILSU = (194, 178, 128)
BRUNS = (106,55,5)
ZILS = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)
BGCOLOR = (LIGHTBLUE)
MOUSE_LEFT = 1
MOUSE_RIGHT = 3