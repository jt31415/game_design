import pygame; pygame.init()
import random
import pygametools as pt
from pygametools import V

import common
from common import * # imports all the common vars

import spawn
import creatures

def draw_grid():
    # draw grid (makes it look like grass tiles)
    offset_x=int(player.pos.x%TILE_SIZE+0.5)
    offset_y=int(player.pos.y%TILE_SIZE+0.5)
    for x in range(-offset_x, width, TILE_SIZE):
        pygame.draw.line(w, GRID_COLOR, (x,0), (x,height+TILE_SIZE), 5)
    for y in range(-offset_y, height, TILE_SIZE):
        pygame.draw.line(w, GRID_COLOR, (0,y), (width+TILE_SIZE,y), 5)

def draw_creatures():
    for creature in game_creatures:
        creature.draw(w)

def draw_humans():
    for human in game_humans:
        human.draw(w)

def draw_weapon(center, resize=None, outline=True):
    if resize:
        draw_weapon = pygame.transform.scale(player.weapon.scaled, (resize, resize))
        draw_weapon = pt.crop_to_bounding(draw_weapon)
    else:
        draw_weapon = pt.crop_to_bounding(player.weapon.scaled)

    # draw the weapon
    weapon_rect = draw_weapon.get_rect()
    weapon_rect.center = center

    w.blit(draw_weapon, weapon_rect.topleft)

    # manipulate rect before rendering for padding and square
    if outline:
        side = max(weapon_rect.size) + 15
        weapon_rect.update((0, 0), (side, side))
        weapon_rect.center = center
        pygame.draw.rect(w, (0,0,0), weapon_rect, 5)

health_bars = [pygame.image.load(img) for img in ['./hud/health_high.svg', './hud/health_medium.svg', './hud/health_low.svg']]
for i in range(len(health_bars)):
    ratio = health_bars[i].get_height() / health_bars[i].get_width()
    health_bars[i] = pygame.transform.smoothscale(health_bars[i], (BAR_WIDTH, BAR_WIDTH * ratio))
    
xp_bars = [pygame.image.load(img) for img in ['./hud/experience_high.svg', './hud/experience_medium.svg', './hud/experience_low.svg']]
for i in range(len(xp_bars)):
    ratio = xp_bars[i].get_height() / xp_bars[i].get_width()
    xp_bars[i] = pygame.transform.smoothscale(xp_bars[i], (BAR_WIDTH, BAR_WIDTH * ratio))
    
def draw_hud():
    # draw the health bar
    health_outline_rect = pygame.Rect(25, 25, BAR_WIDTH, BAR_HEIGHT)
    health_rect = health_outline_rect.copy()
    health_rect.width = (player.health / player.max_health) * BAR_WIDTH
    health_color = (0, 255, 0) if player.health >= 40 else (255, 0, 0)
    pygame.draw.rect(w, health_color, health_rect)
    pygame.draw.rect(w, (0, 0, 0), health_outline_rect, width=5)

    # draw the xp bar
    xp_outline_rect = health_outline_rect.copy()
    xp_outline_rect.x = w.get_width()-BAR_WIDTH-25
    xp_rect = xp_outline_rect.copy()
    xp_rect.width = (player.experience / 100) * BAR_WIDTH
    pygame.draw.rect(w, (255, 255, 0), xp_rect)
    pygame.draw.rect(w, (255, 165, 0), xp_outline_rect, width=5)
    pt.centertext(FONT, str(player.level), (0,0,0), w, xp_outline_rect) # draw the xp level

    draw_weapon((w.get_width()/2, w.get_height()-75))

def draw_screen():
    game_state = common.game_state
    if game_state == 'play':
        w.fill(ARENA_COLOR)

        draw_grid()
        
        # draw arena bounds
        #rect = pygame.Rect(*get_rel(V(-ARENA_SIZE, -ARENA_SIZE)).aslist,d_ARENA_SIZE,d_ARENA_SIZE).clip(w_rect).inflate(DRAW_SIZE, DRAW_SIZE)
        #pygame.draw.rect(w,(0,0,0),rect,10)
    
        player.draw(w) # draw player
        draw_humans() # draw other humans
        draw_creatures() # draw other creatures
        draw_hud() # draw hud on top of everything

    elif game_state == 'upgrade':
        w.blit(saved_screen, (0,0))
        w.blit(darkened_surf, (0,0))
        w.blit(UPGRADE_GUI, (0,0))

        pt.centertext(FONT, 'UPGRADE', (0,0,0), w, (0,10,width,50))
        draw_weapon((195, 115), 140, outline=False)
        
    elif game_state == 'game over':
        w.fill((255,255,255))
        pt.center_img(GAME_OVER_IMG, w, w_rect)
        pt.centertext(FONT_BIG, 'GAME', (0,0,0), w, (0, 0, width, height/3))
        pt.centertext(FONT_BIG, 'OVER', (0,0,0), w, (0, 2*height/3, width, height/3))
        
    pygame.display.flip()
    c.tick(FPS)

def main_loop(attack):
    player.look_at_point(V(*pygame.mouse.get_pos()))
    player.attack_cooldown -= c.get_time()
    
    max_attack_range = player.weapon.range*TILE_SIZE
    for creature in game_creatures:
        creature.attack_cooldown -= c.get_time()

        # player attacks mobs
        target = None
        if attack:
            angle_to_creature = pt.delta_to_degrees(pt.delta(player.pos, creature.pos)) + 90
            dist_to_creature = pt.dist(player.pos, creature.pos)
            if dist_to_creature < max_attack_range and abs(angle_to_creature - player.rot) < 30:
                target=creature
        if target and player.attack_cooldown <= 0:
            player.attack(target)
                
        creature.move(*pt.delta(creature.pos, player.pos).aslist, SPEED*0.1 * c.get_time())
        creature.look_at_point(player.rel)

        # mobs attack player
        max_attack_range = creature.weapon.range*TILE_SIZE
        dist_to_player = pt.dist(player.pos, creature.pos)
        if dist_to_player < max_attack_range and creature.attack_cooldown <= 0:
            creature.attack(player)

def restart_game():
    global player

    common.game_state = 'play'
    common.game_creatures.clear()
    common.game_humans.clear()

    creatures.make_player()
    player = creatures.player
    player.gain_xp(0)
    pygame.time.set_timer(pygame.USEREVENT, 10000) # spawn creatures
    pygame.time.set_timer(pygame.USEREVENT + 1, player.regen) # regen player

restart_game()
        
i=0 # DEBUG

attack = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            attack=True
        elif event.type == pygame.USEREVENT:
            if common.game_state == 'play':
                spawn.spawn_creatures(common.wave_template, 5)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if common.game_state == 'game over':
                    restart_game()
            if event.key == pygame.K_e:
                if common.game_state == 'play':
                    common.game_state = 'upgrade'
                    if player.points>=1: player.weapon = creatures.make_weapon('crossbow')
                    saved_screen = w.copy()
                    #saved_screen = saved_screen.convert_alpha()
                elif common.game_state == 'upgrade':
                    common.game_state = 'play'
        elif event.type == pygame.USEREVENT + 1:
            if common.game_state == 'play':
                player.health = min(player.health + 10, 100)
            
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