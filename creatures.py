import pygametools as pt
from pygametools import V, get_rel
import pygame, math

import common
from common import *

class Weapon:
    def __init__(self, name, damage, range, cooldown, img=None):
        self.name=name
        self.damage=damage
        self.range=range
        self.cooldown=cooldown
        self.image=pygame.image.load(img) if img else pygame.Surface((0,0))
        self.scaled=pygame.transform.smoothscale(self.image, (DRAW_SIZE, DRAW_SIZE))
    
class Creature:
    def __init__(self, name, weapon, max_health, max_strength, img, pos=V(0,0)):
        self.name = name
        self.weapon = weapon
        self.max_health = max_health
        self.max_strength = max_strength
        self.health = max_health
        self.strength = max_strength
        self.attack_cooldown = 0
        
        self.image = pygame.image.load(img)
        self.scaled = pygame.transform.smoothscale(self.image, (DRAW_SIZE, DRAW_SIZE))
        self.final_img = self.scaled

        #position vars
        self.pos=pos
        self.rot=0
    
    def attack(self, target):
        target.take_damage(self.weapon.damage+self.strength)
        self.attack_cooldown = self.weapon.cooldown
    
    def take_damage(self, damage):
        print("{} takes {} damage".format(self.name, damage))
        self.health-=damage
        if self.health<=0:
            self.die()
        else:
            print("{} is hurt".format(self.name))

    def die(self):
        print("{} is dead".format(self.name))
        game_creatures.remove(self)
        del self

    def draw(self,surf):
        final=self.final_img
        half=V(int(final.get_width()/2 + 0.5), int(final.get_height()/2 + 0.5)) # half of the image size
        point=V(self.rel.x-half.x, self.rel.y-half.y)
        
        if pygame.Rect(point.x, point.y, final.get_width(), final.get_height()).colliderect(surf.get_rect()): # if on screen
            surf.blit(self.weapon.scaled, point.aslist)
            surf.blit(final,point.aslist)

    def look_at_point(self,point):
        dir=pt.delta(self.rel,point)
        angle=pt.delta_to_degrees(dir) + 90
        if self.rot!=angle:
            self.rot=angle
            self.final_img=pygame.transform.rotate(self.scaled,self.rot) # resized and rotated image

    def move(self,dx,dy,speed):
        move_vec=V(dx,dy).normalized(speed)
        move_pos=V(self.pos.x+move_vec.x, self.pos.y+move_vec.y)
        #if not (move_pos.x<-CONST['size'] or move_pos.x>CONST['size'] or move_pos.y<-CONST['size'] or move_pos.y>CONST['size']):
        self.pos=move_pos

    @property
    def rel(self):
        return get_rel(self.pos, player.pos, w.get_size())

class Human(Creature):
    def __init__(self, name, weapon, pos=V(0,0)):
        self.name = name
        self.weapon = weapon
        self.health = 100
        self.max_health = 100
        self.strength = 10
        self.max_strength = 10
        self.attack_cooldown = 0
        
        self.image = pygame.image.load("./mobs/human.svg")
        self.scaled = pygame.transform.smoothscale(self.image, (DRAW_SIZE, DRAW_SIZE))
        self.final_img = self.scaled

        #position vars
        self.pos=pos
        self.rot=0

    def die(self):
        print("{} is dead".format(self.name))
        common.game_state = 'game over'
        del self

player = Human('Player', Weapon(*weapons['stick']))

template=creature_types['zombie']
game_creatures.append(Creature(template[0], Weapon(*template[1]), template[2], template[3], template[4], V(50,50)))