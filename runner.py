import pygame
from sys import exit
from random import randint

def display_score():
    current_time = pygame.time.get_ticks()//1000 - start_time
    score_surf = font.render("Score: {}".format(current_time),False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    pygame.draw.rect(screen,"#c0e8ec",score_rect)
    pygame.draw.rect(screen,"#c0e8ec",score_rect,10)
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_rect_list):
    if obstacle_rect_list:
        for obstacle_rect in obstacle_rect_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300: screen.blit(snail_surf,obstacle_rect)
            else: screen.blit(fly_surf,obstacle_rect)
        
        obstacle_rect_list = [obstacle_rect for obstacle_rect in obstacle_rect_list if obstacle_rect.x > -100]

        return obstacle_rect_list
    else: return []

def collision(player_rect,obstacle_rect_list):
    if obstacle_rect_list:
        for obstacle_rect in obstacle_rect_list:
            if player_rect.colliderect(obstacle_rect):
                obstacle_rect_list.clear()
                player_rect.midbottom = (80,300)
                return False
    return True  

def player_animation():
    global player_index,player_surf

    if player_rect.bottom < 300: player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Runner")
font = pygame.font.Font("font/Pixeltype.ttf",50)
game_active = False
start_time = 0
bg_music = pygame.mixer.Sound("audio/music.wav")
bg_music.set_volume(0.5)

sky_surf = pygame.image.load("graphics/Sky.png").convert()
ground_surf = pygame.image.load("graphics/Ground.png").convert()

#Obstacles
snail1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail = [snail1,snail2]
snail_index = 0
snail_surf = snail[snail_index]

fly1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
fly2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
fly = [fly1,fly2]
fly_index = 0
fly_surf = fly[fly_index]

obstacle_rect_list = []

#Player
player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0
player_jump_sound = pygame.mixer.Sound("audio/jump.mp3")
player_jump_sound.set_volume(0.2)

#Intro
player_stand_surf = pygame.transform.rotozoom((pygame.image.load("graphics/player/player_stand.png").convert_alpha()),0,2)
player_stand_rect = player_stand_surf.get_rect(center = (400,200))
game_name_surf = font.render("Runner",False,(111,196,169))
game_name_rect = game_name_surf.get_rect(center = (400,80))
game_message_surf = font.render("Press Space to run",False,(111,196,169))
game_message_rect = game_message_surf.get_rect(center = (400,330))
score = 0

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)
fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
                    player_jump_sound.play()
            
            if event.type == obstacle_timer:
                if randint(0,1):
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100),300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100),210)))

            if event.type == snail_animation_timer:
                if snail_index == 0: snail_index = 1
                else: snail_index = 0
                snail_surf = snail[snail_index]

            if event.type == fly_animation_timer:
                if fly_index == 0: fly_index = 1
                else: fly_index = 0
                fly_surf = fly[fly_index]

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()//1000

    if game_active:
        bg_music.play(loops=-1)
        screen.blit(sky_surf,(0,0))
        screen.blit(ground_surf,(0,300))
        score = display_score()

        #Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf,player_rect)

        #Obstacles movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #Collision
        game_active = collision(player_rect,obstacle_rect_list)

    else:   
        screen.fill((94,169,162))
        screen.blit(game_name_surf,game_name_rect)
        screen.blit(player_stand_surf,player_stand_rect)

        score_message_surf = font.render("Your score: {}".format(score),False,(111,196,169))
        score_message_rect = score_message_surf.get_rect(center = (400,330))

        if score == 0: screen.blit(game_message_surf,game_message_rect)
        else: screen.blit(score_message_surf,score_message_rect)
    
    pygame.display.update()
    pygame.time.Clock().tick(60)