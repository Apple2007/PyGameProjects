# Importing Libraries and Setting Up Display and Sound Effects and Score
import pygame, sys, random

from pygame import (
    RLEACCEL,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()
pygame.display.set_caption("Space Invaders: Python Edition")

pygame.mixer.init()
bullitsound = pygame.mixer.Sound("Space Invaders/bullitsound.mp3")
explodesound = pygame.mixer.Sound("Space Invaders/explode.wav")

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode([screen_width, screen_height])

score = 0

font = pygame.font.Font("Space Invaders/font.ttf", 17)
made_font = pygame.font.Font("Space Invaders/font.ttf", 14)

# Custom Event for Alien
addalien = pygame.USEREVENT + 1
pygame.time.set_timer(addalien, 1500)

# Classes for Player and Aliens

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.wrong = pygame.image.load("Space Invaders/player.png").convert()
        self.surf = pygame.transform.scale(self.wrong, (30, 30))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            midbottom=(
                screen_width / 2,
                screen_height - 10,
            )
        )

    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super(Alien, self).__init__()
        sprites_list = ["Space Invaders/alien.png", "Space Invaders/alien_blue.png", "Space Invaders/alien_red.png", "Space Invaders/alien_purple.png"]
        self.wrong = pygame.image.load(random.choice(sprites_list)).convert()
        self.surf = pygame.transform.scale(self.wrong, (40, 40))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, screen_width),
                -10
            )
        )

    def update(self):
        global running
        self.rect.move_ip(0, 1)
        if self.rect.bottom > screen_height:
            running = False
            self.kill()

class Bullit(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.surf = pygame.surface.Surface((10, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center = player.rect.center
        )

    def update(self):
        self.rect.move_ip(0, -2)
        if self.rect.bottom < 0:
            self.kill()

# Decent FPS
clock = pygame.time.Clock()

# Init Player
player = Player()

# Sprite Group for Aliens
aliens = pygame.sprite.Group()
bullit = pygame.sprite.Group()

# Game Loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                bullitsound.play()
                bullit.add(Bullit(player))

        if event.type == QUIT:
            running = False

        if event.type == addalien:
            new_alien = Alien()
            aliens.add(new_alien)


    screen.fill((0, 0, 0))


    for entity in aliens:
        entity.update()
        screen.blit(entity.surf, entity.rect)

    screen.blit(player.surf, player.rect)

    score_counter = font.render("Aliens Shot: " + str(score), True, (255, 255, 255))
    made_by = made_font.render("Game Made By: Jack Shorenstein | Copyright 2023", True, (255, 255, 255))
    screen.blit(score_counter, (10, 10))
    screen.blit(made_by, (445, 10))

    if pygame.sprite.spritecollideany(player, aliens):
        player.kill()
        running = False

    for entity in bullit:
        entity.update()
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.groupcollide(bullit, aliens, True, True):
        explodesound.play()
        score += 1

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    pygame.display.flip()
    clock.tick(60)