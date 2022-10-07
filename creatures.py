import pygametools as pt
from pygametools import V, get_rel
import pygame, math, random

import common
from common import *

class Weapon:
    def __init__(self, name, damage, range, cooldown, img=None):
        self.name = name
        self.damage = damage
        self.range = range
        self.cooldown = cooldown
        self.image = pygame.image.load(img) if img else pygame.Surface((0,0))
        self.scaled = pygame.transform.smoothscale(self.image, (DRAW_SIZE, DRAW_SIZE))
        self.final_img = self.scaled
    
class Creature:
    def __init__(self, name, weapon, max_health, max_strength, xp_on_death, img, pos=V(0,0)):
        self.name = name
        self.weapon = weapon
        self.max_health = max_health
        self.max_strength = max_strength
        self.health = max_health
        self.strength = max_strength
        self.attack_cooldown = self.weapon.cooldown
        self.xp_on_death = xp_on_death
        
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
        player.gain_xp(self.xp_on_death)
        del self

    def draw(self,surf):
        final=self.final_img
        half=V(int(final.get_width()/2 + 0.5), int(final.get_height()/2 + 0.5)) # half of the image size
        point=V(self.rel.x-half.x, self.rel.y-half.y)
        
        if pygame.Rect(point.x, point.y, final.get_width(), final.get_height()).colliderect(surf.get_rect()): # if on screen
            surf.blit(self.weapon.final_img, point.aslist)
            surf.blit(final,point.aslist)

    def look_at_point(self,point):
        dir=pt.delta(self.rel,point)
        angle=pt.delta_to_degrees(dir) + 90
        if self.rot!= angle:
            self.rot = angle
            self.final_img = pygame.transform.rotate(self.scaled, self.rot) # resized and rotated image
            self.weapon.final_img = pygame.transform.rotate(self.weapon.scaled, self.rot+90)

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
        self.strength = 20
        self.max_strength = 20
        self.attack_cooldown = self.weapon.cooldown
        self.experience = 0
        self.level = 0
        
        self.image = pygame.image.load("./mobs/human.svg")
        self.scaled = pygame.transform.smoothscale(self.image, (DRAW_SIZE, DRAW_SIZE))
        self.final_img = self.scaled

        #position vars
        self.pos=pos
        self.rot=0

    def gain_xp(self, xp):
        self.experience+=xp
        if self.experience>=100:
            self.level += self.experience // 100
            self.experience %= 100

    def die(self):
        print("{} is dead".format(self.name))
        common.game_state = 'game over'
        del self

def spawn_creature(template, pos):
    game_creatures.append(Creature(template[0], Weapon(*template[1]), *template[2:6], pos))

player = Human('Player', Weapon(*weapons['stick']))