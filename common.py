'''
This file contains the common variables used by the other files.
'''

import pygame

size = width, height = [640, 480]

w = pygame.display.set_mode(size)
darkened_surf = pygame.Surface(w.get_size(), pygame.SRCALPHA)
darkened_surf.fill((0,0,0,100))
w_rect = w.get_rect()
c = pygame.time.Clock()
FPS=60

# arena size
ARENA_SIZE = 1000
n_ARENA_SIZE = -ARENA_SIZE
d_ARENA_SIZE = ARENA_SIZE*2

# arena drawing
ARENA_COLOR = pygame.Color(164,205,218)
GRID_COLOR = pygame.Color(*[max(0, i-20) for i in [ARENA_COLOR.r, ARENA_COLOR.g, ARENA_COLOR.b]])
TILE_SIZE = 50
NUM_TILES = max(width, height)//TILE_SIZE + 1

# player drawing
DRAW_SIZE = 120

# HUD drawing
BAR_WIDTH = 200
BAR_HEIGHT = 30
FONT = pygame.font.Font('./fonts/Zector.ttf', 25)
FONT.bold = True
FONT_BIG = pygame.font.Font('./fonts/Zector.ttf', 80)
FONT_BIG.bold = True

# in game player
SPEED=0.3
SPAWN_RADIUS=500

# upgrade
UPGRADE_GUI = pygame.image.load('./extra/upgrade_gui.png')

# game over
GAME_OVER_IMG = pygame.image.load("./hud/game_over.png")

weapons = {
    'stick': ['stick', 5, 1, 200, './weapons/stick.png'],
    'axe': ['axe', 10, 2, 1000, './weapons/axe.png'],
    'crossbow': ['crossbow', 25, 5, 5000, './weapons/crossbow.png'],
    'null': ['null', 0, 1, 500]
}

creature_types = {
    'zombie': ['Zombie', weapons['null'], 10, 5, 10, './mobs/zombie.png'],
    'ice_zombie': ['Ice Zombie', weapons['stick'], 20, 10, 10, './mobs/ice_zombie.png'],
    'fire_zombie': ['Fire Zombie', weapons['axe'], 40, 20, 10, './mobs/fire_zombie.png']
}

wave_template = creature_types['zombie']

game_humans = []
game_creatures = []

game_state = 'play'