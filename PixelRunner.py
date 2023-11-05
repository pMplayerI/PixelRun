import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300: self.rect.bottom = 300

    def player_animation(self):
        if self.rect.bottom < 300: self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.player_animation()

class Obstacles(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == "fly":
            fly1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
            fly2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
            self.obstacle = [fly1,fly2]
            y_pos = 210
        else:
            snail1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.obstacle = [snail1,snail2]
            y_pos = 300

        self.obstacle_index = 0
        self.image = self.obstacle[self.obstacle_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def obstacles_animation(self):
        self.obstacle_index += 0.1 
        if self.obstacle_index >= len(self.obstacle): self.obstacle_index = 0
        self.image = self.obstacle[int(self.obstacle_index)]

    def obstacles_destroy(self):
        if self.rect.x <= -100: self.kill()

    def update(self):
        self.rect.x -= 5
        self.obstacles_animation()
        self.obstacles_destroy()

def collision():
    if pygame.sprite.spritecollide(player.sprite,obstacles,False):
        obstacles.empty()
        player.sprite.rect.midbottom = (80,300)
        return False
    else: return True

def display_score():
    current_time = pygame.time.get_ticks()//1000 - start_time
    score_surf = font.render("Score: {}".format(current_time),False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    pygame.draw.rect(screen,"#c0e8ec",score_rect)
    pygame.draw.rect(screen,"#c0e8ec",score_rect,10)
    screen.blit(score_surf,score_rect)
    return current_time

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Pixel Runner")
font = pygame.font.Font("font/Pixeltype.ttf",50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1)
sky_surf = pygame.image.load("graphics/Sky.png").convert()
ground_surf = pygame.image.load("graphics/Ground.png").convert()

#Intro
player_stand_surf = pygame.transform.rotozoom((pygame.image.load("graphics/player/player_stand.png").convert_alpha()),0,2)
player_stand_rect = player_stand_surf.get_rect(center = (400,200))
game_name_surf = font.render("Runner",False,(111,196,169))
game_name_rect = game_name_surf.get_rect(center = (400,80))
game_message_surf = font.render("Press Space to run",False,(111,196,169))
game_message_rect = game_message_surf.get_rect(center = (400,330))

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacles = pygame.sprite.Group()

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer: obstacles.add(Obstacles(choice(['fly','snail','snail','snail'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()//1000

    if game_active:
        screen.blit(sky_surf,(0,0))
        screen.blit(ground_surf,(0,300))
        score = display_score()
    
        player.draw(screen)
        player.update()

        obstacles.draw(screen)
        obstacles.update()

        game_active = collision()

    else:
        screen.fill((94,169,162))
        screen.blit(game_name_surf,game_name_rect)
        screen.blit(player_stand_surf,player_stand_rect)
        score_message_surf = font.render("Your score: {}".format(score),False,(111,196,169))
        score_message_rect = score_message_surf.get_rect(center = (400,330))
        if score == 0: screen.blit(game_message_surf,game_message_rect)
        else: screen.blit(score_message_surf,score_message_rect)

    pygame.display.update()
    pygame.time.Clock().tick(30)

