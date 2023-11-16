# Import PyGame & SYS & Random, Initialze PyGame & pygame.mixer, and Setup Screen
import pygame, sys, random

from pygame import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()
pygame.display.set_caption("Missile Dodge (Horrible Game)")

pygame.mixer.init()
pygame.mixer.music.load("Missile Dodge/axelf.mp3")
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)

screen_height = 600
screen_width = 800

screen = pygame.display.set_mode([screen_width, screen_height])

# Creating Custom Event for Enemies and Cloud
addememy = pygame.USEREVENT + 1
pygame.time.set_timer(addememy, 250)
addcloud = pygame.USEREVENT + 2
pygame.time.set_timer(addcloud, 250)

# Defining Player, Enemy, and Cloud Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("Missile Dodge/pitrizzo-SpaceShip-gpl3-opengameart-24x24.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("Missile Dodge/spr_missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.size = self.surf.get_size()
        self.surf = pygame.transform.scale(self.surf, (int(self.size[0] / 2), int(self.size[1] / 2)))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(screen_width + 20, screen_width + 100),
                random.randint(0, screen_height),
            )
        )
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("Missile Dodge/cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(screen_width + 20, screen_width + 100),
                random.randint(0, screen_height),
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

# Initialize Player Class
player = Player()

# Create Sprite Groups
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Setup Decent FPS (so I won't go more insane...)
clock = pygame.time.Clock()

# Game Loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

        elif event.type == addememy:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == addcloud:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    screen.fill((135, 206, 250))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    enemies.update()
    clouds.update()

    pygame.display.flip()
    clock.tick(30)
