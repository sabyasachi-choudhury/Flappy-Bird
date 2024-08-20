# Imports
import time

import pygame
import random
from pygame.locals import (K_ESCAPE, QUIT, KEYDOWN, K_SPACE, MOUSEBUTTONDOWN)

# Init
pygame.init()

# Colors
blue = (143, 242, 255)
black = (0, 0, 0)
white = (255, 255, 255)

# Setting global vars
global vel_y
global change_angle
global angle
change_angle = -10
angle = 0
vel_y = 0

# Setting non global vars
game = True
menu = True
s_width = 1000
s_height = 800
score = 0
game_speed = 25

# Screen
screen = pygame.display.set_mode((s_width, s_height))


# Top pillar
class TopPillar(pygame.sprite.Sprite):
    def __init__(self, h):
        self.height = h
        super(TopPillar, self).__init__()
        self.surf = pygame.transform.smoothscale(pygame.image.load("pipe2.png").convert(), (50, self.height))
        self.rect = self.surf.get_rect(center=(s_width, self.height / 2))


# Bottom pillar
class BottomPillar(pygame.sprite.Sprite):
    def __init__(self, top_height):
        self.height = s_height - top_height - 175
        super(BottomPillar, self).__init__()
        self.surf = pygame.transform.smoothscale(pygame.image.load("pipe.png").convert(), (50, self.height))
        self.rect = self.surf.get_rect(
            center=(s_width, s_height - self.height + self.height / 2))


# Creating coin
class Coin(pygame.sprite.Sprite):
    def __init__(self, top_height):
        self.pos_aid = top_height
        super(Coin, self).__init__()
        self.surf = pygame.transform.smoothscale(pygame.image.load("FlappyCoin.png").convert(), (40, 40))
        self.rect = self.surf.get_rect(center=(s_width, self.pos_aid + 75))


# Creating player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.transform.smoothscale(pygame.image.load("FlappyBird.png").convert(), (45, 30))
        self.rect = self.surf.get_rect(center=(s_width / 2, s_height / 2))
        self.og_surf = self.surf

        self.surf = pygame.transform.rotate(self.og_surf, 30)
        self.rect = self.surf.get_rect(center=self.rect.center)


# Creating play button
class PlayButton(pygame.sprite.Sprite):
    def __init__(self):
        super(PlayButton, self).__init__()
        self.surf = pygame.transform.smoothscale(pygame.image.load("play.png").convert(), (200, 85))
        self.rect = self.surf.get_rect(center=(s_width/2, s_height/2))
        self.surf.set_colorkey((0, 0, 0))


# Defining gravity
def gravity(spr, accel):
    global vel_y
    global change_angle
    global angle
    spr.rect.move_ip(0, vel_y)
    spr.surf = pygame.transform.rotate(spr.og_surf, angle)
    spr.rect = spr.surf.get_rect(center=spr.rect.center)
    if angle > -80:
        angle += change_angle
    if vel_y < 30:
        vel_y += accel


# User events
add_pillar = pygame.USEREVENT + 1
pygame.time.set_timer(add_pillar, 1700)

increase_speed = pygame.USEREVENT + 2
pygame.time.set_timer(increase_speed, 8500)

# Groups
all_sprites = pygame.sprite.Group()
pillars = pygame.sprite.Group()
coins = pygame.sprite.Group()
player_group = pygame.sprite.Group()


# Main loop
# Menu conditional
if menu:
    play_button = PlayButton()

while menu:
    # Screen fill
    screen.fill(blue)

    # Detecting events
    for event in pygame.event.get():
        if event.type == QUIT:
            menu = False
            game = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                menu = False
                game = False
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if play_button.rect.collidepoint(mouse_pos):
                menu = False
                time.sleep(1)
                play_button.kill()

    screen.blit(play_button.surf, play_button.rect)

    pygame.display.flip()


# Game conditional
if game:
    player = Player()
    all_sprites.add(player)
    player_group.add(player)

# Game loop
while game:
    # Screen fill
    screen.fill(blue)

    # Getting press list
    press_list = pygame.key.get_pressed()

    # Detecting events
    for event in pygame.event.get():
        if event.type == QUIT:
            game = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                game = False
            if event.key == K_SPACE:
                vel_y = -20
                angle = 70

        if event.type == add_pillar:
            height = random.randint(50, 500)
            # Making the objects
            top_pillar = TopPillar(height)
            bottom_pillar = BottomPillar(height)
            coin = Coin(height)

            # Adding to groups
            all_sprites.add(top_pillar)
            all_sprites.add(bottom_pillar)
            all_sprites.add(coin)
            pillars.add(top_pillar)
            pillars.add(bottom_pillar)
            coins.add(coin)

        if event.type == increase_speed:
            game_speed += 1

    # Gravity
    gravity(player, 3)

    # Player limits
    if player.rect.top > s_height or player.rect.bottom < 0:
        game = False

    # Coll with pillars
    if pygame.sprite.spritecollideany(player, pillars):
        game = False

    # Coll with coins
    for x in coins:
        if pygame.sprite.spritecollideany(x, player_group):
            pygame.mixer.Sound("point.wav").play()
            x.kill()
            score += 1

    # Moving pillars
    for pill in pillars:
        pill.rect.move_ip(-10, 0)

    # Moving coins
    for c in coins:
        c.rect.move_ip(-10, 0)

    # Rendering all
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
        if entity.rect.right < 0 or entity.rect.bottom < 0 or entity.rect.top > s_height:
            entity.kill()

    # Display.flip
    pygame.display.flip()
    pygame.time.Clock().tick(game_speed)

# Quit
pygame.quit()
print(score)
