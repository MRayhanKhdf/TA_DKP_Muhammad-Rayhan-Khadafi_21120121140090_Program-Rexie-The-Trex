import pygame
from pygame.locals import *
from pygame import mixer
from sys import exit
from random import randint

pygame.init()

screen = pygame.display.set_mode((1100, 600))
pygame.display.set_caption('Rexie the T-Rex')
clock = pygame.time.Clock()
HI_font = pygame.font.Font('font/PressStart2P-Regular.ttf', 20)
game_active = False
start_time = 0
HI = 0

#Track starter
track = pygame.image.load('assets/other/track.png').convert_alpha()
track_x =0

#Obstacle starter
rock = pygame.image.load('assets/rock/rock.png').convert_alpha()

ptera1 = pygame.image.load('assets/ptera/ptera1.png').convert_alpha()
ptera2 = pygame.image.load('assets/ptera/ptera2.png').convert_alpha()
ptera_fly = [ptera1, ptera2]
ptera_index = 0
ptera = ptera_fly[ptera_index]

obstacle_rect_list = []

#Rexie starter
rexie1 = pygame.image.load('assets/dino/RexieRun1.png').convert_alpha()
rexie2 = pygame.image.load('assets/dino/RexieRun2.png').convert_alpha()
rexie3 = pygame.image.load('assets/dino/RexieRun3.png').convert_alpha()
rexie4 = pygame.image.load('assets/dino/RexieRun4.png').convert_alpha()
rexie5 = pygame.image.load('assets/dino/RexieRun5.png').convert_alpha()
rexie6 = pygame.image.load('assets/dino/RexieRun6.png').convert_alpha()
rexie7 = pygame.image.load('assets/dino/RexieRun7.png').convert_alpha()
rexie8 = pygame.image.load('assets/dino/RexieRun8.png').convert_alpha()
rexie_run = [rexie1, rexie2, rexie3, rexie4,rexie5, rexie6, rexie7, rexie8]
rexie_index = 0
rexie = rexie_run [rexie_index]
rexie_rect = rexie.get_rect(midbottom = (80, 470))
rexie_gravity = 0

rexie_jump = pygame.image.load('assets/dino/RexieJump.png').convert_alpha()

#Menu
rexie_menu = pygame.image.load('assets/dino/Rexiemenu.png').convert_alpha()
rexie_menu = pygame.transform.scale2x(rexie_menu)
rexie_menu_rect = rexie_menu.get_rect(center=(555, 250))
title = HI_font.render("Rexie the T-Rex", False, (0, 0, 0))
title_rect = title.get_rect(center = (560, 100))
menutxt = HI_font.render('Press Space  To Play', False, (0, 0, 0))
menutxt_rect = menutxt.get_rect(center = (550, 400))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)

ptera_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(ptera_animation_timer, 200)

#HI
def display_HI():
    current_time = int(pygame.time.get_ticks() / 10) - start_time
    HI = HI_font.render(f'{current_time}', False, (0, 0, 0))
    HI_rect = HI.get_rect(center = (550, 100))
    screen.blit(HI, HI_rect)
    return current_time

#Obstacle Movement
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 475:
                screen.blit(rock, obstacle_rect)
            else:
                screen.blit(ptera, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -200]

        return obstacle_list
    else: return []

#Collision
def collision(rexie,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if rexie.colliderect(obstacle_rect): return False
    return True

#Rexie animate
def rexie_running():
    global rexie, rexie_index
    if rexie_rect.bottom < 470:
        rexie = rexie_jump

    else:
        rexie_index += 0.15
        if rexie_index >= len(rexie_run):rexie_index = 0
        rexie = rexie_run[int(rexie_index)]

#Main Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(rock.get_rect(bottomright=(randint(1200, 1400), 475)))
                else:
                    obstacle_rect_list.append(ptera.get_rect(bottomright=(randint(1200, 1400), 340)))
            if event.type == ptera_animation_timer:
                if ptera_index == 0: ptera_index = 1
                else: ptera_index = 0
                ptera = ptera_fly[ptera_index]

            if event.type == pygame.MOUSEBUTTONUP:
                if rexie_rect.collidepoint(event.pos)and rexie_rect.bottom >=470:
                    rexie_gravity = -20

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and rexie_rect.bottom >=470 :
                    rexie_gravity = -20

        else:
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 10)

    if game_active:
        #Track
        screen.blit (track,(0, -110))

        #Score
        HI = display_HI()

        #Obstacle movement
        obstacle_movement(obstacle_rect_list)

        #Obstacle
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #Rexie
        rexie_gravity += 0.8
        rexie_rect.y += rexie_gravity
        if rexie_rect.bottom >= 470: rexie_rect.bottom =470
        rexie_running()
        screen.blit(rexie, rexie_rect)


        #Collide
        game_active = collision(rexie_rect, obstacle_rect_list)

    else:
        obstacle_rect_list.clear()
        rexie_rect.midbottom = (80, 470)
        rexie_gravity = 0

        HI_Menu = HI_font.render(f'Your Score: {HI}',False, (0,0,0))
        HI_Menu_rect = HI_Menu.get_rect(center =(550, 450))

        screen.blit(track, (0, -110))
        screen.blit(rexie_menu, rexie_menu_rect)
        screen.blit(title, title_rect)

        if HI == 0: screen.blit(menutxt, menutxt_rect)
        else: screen.blit(HI_Menu, HI_Menu_rect)


    pygame.display.update()
    clock.tick(60)