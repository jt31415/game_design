import pygame; pygame.init()
import random
import pygametools as pt
from pygametools import V

import common
from common import * # imports all the common vars

import spawn
from creatures import player

def draw_creatures():
    for creature in game_creatures:
        creature.draw(w)

def draw_humans():
    for human in game_humans:
        human.draw(w)

health_bars = [pygame.image.load(img) for img in ['./hud/health_high.svg', './hud/health_medium.svg', './hud/health_low.svg']]
for i in range(len(health_bars)):
    ratio = health_bars[i].get_height() / health_bars[i].get_width()
    health_bars[i] = pygame.transform.smoothscale(health_bars[i], (BAR_WIDTH, BAR_WIDTH * ratio))
    
xp_bars = [pygame.image.load(img) for img in ['./hud/experience_high.svg', './hud/experience_medium.svg', './hud/experience_low.svg']]
for i in range(len(xp_bars)):
    ratio = xp_bars[i].get_height() / xp_bars[i].get_width()
    xp_bars[i] = pygame.transform.smoothscale(xp_bars[i], (BAR_WIDTH, BAR_WIDTH * ratio))
    
def draw_hud():
    health_outline_rect = pygame.Rect(25, 25, BAR_WIDTH, BAR_HEIGHT)
    health_rect = pygame.Rect(25, 25, BAR_WIDTH * (player.health/player.max_health), BAR_HEIGHT)
    health_color = (0, 255, 0) if player.health >= 40 else (255, 0, 0)
    pygame.draw.rect(w, health_color, health_rect)
    pygame.draw.rect(w, (0, 0, 0), health_outline_rect, width=5)

    xp_outline_rect = health_outline_rect.copy()
    xp_outline_rect.x = w.get_width()-BAR_WIDTH-25
    xp_rect = xp_outline_rect.copy()
    xp_rect.width = (player.experience / 100) * BAR_WIDTH
    pygame.draw.rect(w, (255, 255, 0), xp_rect)
    pygame.draw.rect(w, (255, 165, 0), xp_outline_rect, width=5)
    pt.centertext(FONT, str(player.level), (0,0,0), w, xp_outline_rect)

def draw_screen():
    game_state = common.game_state
    if game_state == 'play':
        w.fill(ARENA_COLOR)
    
        # draw grid (makes it look like grass tiles)
        offset_x=int(player.pos.x%TILE_SIZE+0.5)
        offset_y=int(player.pos.y%TILE_SIZE+0.5)
        for x in range(-offset_x, width, TILE_SIZE):
            pygame.draw.line(w, GRID_COLOR, (x,0), (x,height+TILE_SIZE), 5)
        for y in range(-offset_y, height, TILE_SIZE):
            pygame.draw.line(w, GRID_COLOR, (0,y), (width+TILE_SIZE,y), 5)
        
        # draw arena bounds
        #rect = pygame.Rect(*get_rel(V(-ARENA_SIZE, -ARENA_SIZE)).aslist,d_ARENA_SIZE,d_ARENA_SIZE).clip(w_rect).inflate(DRAW_SIZE, DRAW_SIZE)
        #pygame.draw.rect(w,(0,0,0),rect,10)
    
        player.draw(w) # draw player
        draw_humans() # draw other humans
        draw_creatures() # draw other creatures
        draw_hud() # draw hud on top of everything
        
    elif game_state == 'game over':
        w.fill((255,255,255))
        w.blit(GAME_OVER_IMG, (0, 0))

    pygame.display.flip()
    c.tick(FPS)

def main_loop(attack):
    player.look_at_point(V(*pygame.mouse.get_pos()))
    player.attack_cooldown -= c.get_time()
    
    for creature in game_creatures:
        creature.attack_cooldown -= c.get_time()

        # player attacks mobs
        max_attack_range = player.weapon.range*TILE_SIZE
        target = None
        if attack:
            angle_to_creature = pt.delta_to_degrees(pt.delta(player.pos, creature.pos)) + 90
            dist_to_creature = pt.dist(player.pos, creature.pos)
            if dist_to_creature < max_attack_range and abs(angle_to_creature - player.rot) < 30 and player.attack_cooldown <= 0:
                target=creature
        if target:
            player.attack(target)
                
        creature.move(*pt.delta(creature.pos, player.pos).aslist, SPEED*0.1 * c.get_time())
        creature.look_at_point(player.rel)

        # mobs attack player
        max_attack_range = creature.weapon.range*TILE_SIZE
        dist_to_player = pt.dist(player.pos, creature.pos)
        if dist_to_player < max_attack_range and creature.attack_cooldown <= 0:
            creature.attack(player)
        
i=0 # DEBUG

# start the game

attack = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            attack=True
            
    if common.game_state == 'play':
        # movement
        pressed=pygame.key.get_pressed()
        move_dir=[0,0]
        if pressed[pygame.K_w]: move_dir[1]+=-1
        if pressed[pygame.K_s]: move_dir[1]+=1
        if pressed[pygame.K_a]: move_dir[0]+=-1
        if pressed[pygame.K_d]: move_dir[0]+=1
        player.move(*move_dir, SPEED*c.get_time())
        
        main_loop(attack)
    
        attack = False

    draw_screen()

    # DEBUG
    i+=1
    i%=50
    if i==0: print(c.get_fps())

pygame.quit()