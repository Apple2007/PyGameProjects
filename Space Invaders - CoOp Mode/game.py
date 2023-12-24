# Importing Libraries and Setting Up Display and Sound Effects and Score
import pygame, sys, random

from pygame import (
    RLEACCEL,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_a,
    K_d,
    K_w,
    KEYDOWN,
    QUIT,
)

pygame.init()
pygame.display.set_caption("Space Invaders: Python and CoOp Edition")

pygame.mixer.init()
bullitsound = pygame.mixer.Sound("Space Invaders - CoOp Mode/bullitsound.mp3")
explodesound = pygame.mixer.Sound("Space Invaders - CoOp Mode/explode.wav")

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode([screen_width, screen_height])

score = 0

font = pygame.font.Font("Space Invaders - CoOp Mode/font.ttf", 17)
made_font = pygame.font.Font("Space Invaders - CoOp Mode/font.ttf", 14)

# Custom Event for Alien
addalien = pygame.USEREVENT + 1
pygame.time.set_timer(addalien, 1500)

# Classes for Players and Aliens

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        player_sprites = ["Space Invaders - CoOp Mode/player.png", "Space Invaders - CoOp Mode/player_lightblue.png", "Space Invaders - CoOp Mode/player_orange.png", "Space Invaders - CoOp Mode/player_pink.png"]
        self.wrong = pygame.image.load(random.choice(player_sprites)).convert()
        self.surf = pygame.transform.scale(self.wrong, (30, 30))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
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

class PlayerTwo(pygame.sprite.Sprite):
    def __init__(self):
        super(PlayerTwo, self).__init__()
        player_sprites = ["Space Invaders - CoOp Mode/player_two_pink.png", "Space Invaders - CoOp Mode/player_two_slime.png"]
        self.wrong = pygame.image.load(random.choice(player_sprites)).convert()
        self.surf = pygame.transform.scale(self.wrong, (30, 30))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            midbottom=(
                (screen_width / 2) - 75,
                screen_height - 10,
            )
        )

    def update(self, pressed_keys):
        if pressed_keys[K_a]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(5, 0)
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super(Alien, self).__init__()
        sprites_list = ["Space Invaders - CoOp Mode/alien.png", "Space Invaders - CoOp Mode/alien_blue.png", "Space Invaders - CoOp Mode/alien_red.png", "Space Invaders - CoOp Mode/alien_purple.png"]
        self.wrong = pygame.image.load(random.choice(sprites_list)).convert()
        self.surf = pygame.transform.scale(self.wrong, (40, 40))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, screen_width),
                100
            )
        )
        self.bullet_counter = 0
        self.direction = -1

    def update(self):
        self.bullet_counter += 1
        if self.bullet_counter > FPS * 2:
            self.bullet_counter = 0
            bul = BulletAlien(self)
            bulletalien.add(bul)
            
        self.rect.x += self.direction
        if self.rect.left <= 0:
            self.direction = 1000
        elif self.rect.right <= screen_width:
            self.direction = -1

class Bullet(pygame.sprite.Sprite):
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

class BulletAlien(pygame.sprite.Sprite):
    def __init__(self, alien):
        super().__init__()
        self.surf = pygame.surface.Surface((10, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center = alien.rect.center
        )

    def update(self):
        self.rect.move_ip(0, 2)

# Decent FPS
clock = pygame.time.Clock()

# Init Player & Group
player = Player()
playertwo = PlayerTwo()
players = pygame.sprite.Group()
players.add(player)
players.add(playertwo)

# Sprite Group for Aliens
aliens = pygame.sprite.Group()
bullet = pygame.sprite.Group()
bulletalien = pygame.sprite.Group()

# Game Loop
running = True
FPS = 60
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                bullitsound.play()
                bullet.add(Bullet(player))
            if event.key == pygame.K_w:
                bullitsound.play()
                bullet.add(Bullet(playertwo))

        if event.type == QUIT:
            running = False

        if event.type == addalien:
            new_alien = Alien()
            aliens.add(new_alien)


    screen.fill((0, 0, 0))

    for entity in aliens:
        entity.update()
        screen.blit(entity.surf, entity.rect)

    for entity in bulletalien:
        entity.update()
        screen.blit(entity.surf, entity.rect)

    pressed_keys = pygame.key.get_pressed()

    for entity in players:
        entity.update(pressed_keys)
        screen.blit(entity.surf, entity.rect)

    score_counter = font.render("Aliens Shot: " + str(score), True, (255, 255, 255))
    made_by = made_font.render("Game Made By: Jack Shorenstein | Copyright 2023", True, (255, 255, 255))
    screen.blit(score_counter, (10, 10))
    screen.blit(made_by, (445, 10))

    for entity in bullet:
        entity.update()
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.groupcollide(bullet, aliens, True, True):
        explodesound.play()
        score += 1
    
    if pygame.sprite.spritecollide(player, bulletalien, True):
        player.rect.center = (-100,-100)
        player.kill()
    
    if pygame.sprite.spritecollide(playertwo, bulletalien, True):
        playertwo.rect.center = (-100,-100)
        playertwo.kill()

    if len(players) == 0:
        running = False

    pygame.display.flip()
    clock.tick(FPS)