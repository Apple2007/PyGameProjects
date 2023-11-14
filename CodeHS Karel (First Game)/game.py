# Import all libraries needed for this game and start PyGame and play music
import pygame, sys
from pygame.locals import *

import os
# os.environ['SDL_AUDIODRIVER'] = 'dsp'

import random
import math

pygame.init()

pygame.mixer.init()

pygame.mixer.music.load("CodeHS Karel (First Game)/Digital Days.mp3")
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)


# Setting Colors and Fonts for Game

green = (211, 237, 218)
black = (0, 0, 0)
white = (255, 255, 255)

font = pygame.font.SysFont("Comic Sans", 20)
font_large = pygame.font.SysFont("Comic Sans", 50)

# Setting Size and Aditional Variables

screen_info = pygame.display.Info()
width = screen_info.current_w
height = 350
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

timer = 5800
score = 0
running = True

FPS = pygame.time.Clock()

# Creating Game Object: Karel

class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("CodeHS Karel (First Game)/karel.png")
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height - 70)
        
    def update(self):
        mouse_position = pygame.mouse.get_pos()[0]
        self.rect.center = (mouse_position, height - 70)
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
# Create Game Object: Tennis Ball

class tennis_ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("CodeHS Karel (First Game)/tennis_ball.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, width - 40), 0) 
    
    def update(self):
        self.rect.move_ip(0, 10)
        if (self.rect.bottom > height):
            self.rect.top = 0
            self.rect.center = (random.randint(40, width - 40), 0)

    def caught(self):
        self.rect.center = (random.randint(40, width - 40), 0)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Sets Karel and Ball Varaibles

ball = tennis_ball()
karel = player()

# Game Loop aka Games Runs until quit & Add HUD & Add Timer and Score

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.mixer.music.stop()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                sys.exit()
                running = False

    karel.update()
    ball.update()

    screen.fill(green)
    karel.draw(screen)
    ball.draw(screen)
    shown_time = math.floor(timer / 100)
    clock_timer = font.render('Timer (Length of Song) = ' + str(shown_time), True, black)
    screen.blit(clock_timer, (width - 280, 10))
    scores = font.render('Tennis Balls = ' + str(score), True, black)
    screen.blit(scores, (10, 10))
    
    if pygame.sprite.collide_rect(karel, ball) and running:
        score += 1
        ball.caught()
        
    if timer < 0:
        running = False
        screen.fill(black)
        game_over = font_large.render('GAME OVER!', True, white)
        scores = font_large.render('Tennis Balls = ' + str(score), True, white)
        screen.blit(game_over, (100, (height / 2) - 45))
        screen.blit(scores, (100, height / 2))

    pygame.display.update()
    timer -= 1
    FPS.tick(60)
