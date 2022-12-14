import pygametools as pt
from pygametools import V

import creatures
from creatures import spawn_creature
import random

from common import *

def spawn_creatures(template, n):
    center = creatures.player.pos
    center.x = int(center.x)
    center.y = int(center.y)

    screen_rect = w_rect.copy()
    screen_rect.center = center.aslist

    for i in range(n):
        p = V(random.randint(center.x - SPAWN_RADIUS, center.x + SPAWN_RADIUS), 
             random.randint(center.y - SPAWN_RADIUS, center.y + SPAWN_RADIUS))
        in_screen = screen_rect.collidepoint(p.aslist)
        while pt.dist(p, center) > SPAWN_RADIUS or in_screen:
            p = V(random.randint(center.x - SPAWN_RADIUS, center.x + SPAWN_RADIUS), 
             random.randint(center.y - SPAWN_RADIUS, center.y + SPAWN_RADIUS))
            in_screen = screen_rect.collidepoint(p.aslist)

        spawn_creature(template, p)