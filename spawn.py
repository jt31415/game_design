import pygametools as pt
from pygametools import V

import creatures
from creatures import spawn_creature, player
import random

from common import *

def spawn_creatures(template, n):
    center = player.pos
    for i in range(n):
        p = V(random.randint(center.x - SPAWN_RADIUS, center.x + SPAWN_RADIUS), 
             random.randint(center.y - SPAWN_RADIUS, center.y + SPAWN_RADIUS))
        in_screen = w_rect.collidepoint(p.aslist)
        while pt.dist(p, center) > SPAWN_RADIUS and in_screen:
            p = V(random.randint(center.x - SPAWN_RADIUS, center.x + SPAWN_RADIUS), 
             random.randint(center.y - SPAWN_RADIUS, center.y + SPAWN_RADIUS))

        spawn_creature(template, p)

spawn_creatures(creature_types['zombie'], 5)