# Importing necessary libraries
import pygame
import random as ran
from pygame.locals import *
# Initializing pygame
pygame.init()
pygame.mixer.init()
# Setting the window dimensions and title
window_height = 640
window_width = 960
window = pygame.display.set_mode((window_width, window_height))
window_rect = pygame.Rect(0, 0, window_width, window_height)
pygame.display.set_caption("Catch")
# Creating random numbers for powerup spawn
rany = ran.randint(0, 576)
ranx = ran.randint(0, 896)
# Adding health mechanic to the game
health = 2
# Adding random selecting of the Catcher
luck = ran.randint(1, 2)
# Adding some paths
p1path = "assets/images/player1.png"
p2path = "assets/images/player2.png"
shoepath = "assets/images/shoepowerup.png"
outlinepath = "assets/images/outline.png"
healthbarpath = "assets/images/health_bar_icon.png"
halfhealthbarpath = "assets/images/half_health_bar_icon.png"
tingpath = "assets/sounds/ting.wav"
ting = pygame.mixer.Sound(tingpath)


# Adding the healthbar


class HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(healthbarpath)
        self.rect = self.image.get_rect()

        self.rect.y = 575

        if luck == 1:
            self.rect.x = 0
        else:
            self.rect.x = 832
# Adding half healthbar


class HalfHealthBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(halfhealthbarpath)
        self.rect = self.image.get_rect()

        self.rect.y = 700
        if luck == 1:
            self.rect.x = 0
        else:
            self.rect.x = 832
# Adding the shoe powerup


class Shoe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(shoepath)
        self.rect = self.image.get_rect()

        self.rect.x = ranx
        self.rect.y = rany
# Adding the red outline, that the catcher will have


class Outline(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(outlinepath)
        self.rect = self.image.get_rect()

        if luck == 1:
            self.rect.x = player2.rect.x
            self.rect.y = player2.rect.y
        if luck == 2:
            self.rect.x = player1.rect.x
            self.rect.y = player1.rect.y
# Adding the 1. player


class Player1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(p1path)
        self.rect = self.image.get_rect()

        self.rect.x = 0
        self.rect.y = 0
# Adding the 2. player


class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(p2path)
        self.rect = self.image.get_rect()

        self.rect.x = 896
        self.rect.y = 576

    def update(self):
        pass

# Assigning sprites


player2 = Player2()
player1 = Player1()
shoe = Shoe()
health_bar = HealthBar()
half_health_bar = HalfHealthBar()
outline = Outline()
all_sprites = pygame.sprite.Group()
all_sprites.add(half_health_bar)
all_sprites.add(health_bar)
all_sprites.add(shoe)
all_sprites.add(player2)
all_sprites.add(player1)
all_sprites.add(outline)


# Gameloop and setting necessary variables

is_running = True
player1_speed = 16
player2_speed = 16

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

# Keeping player inside the game window

        if not window_rect.contains(player1.rect):
            player1.rect.clamp_ip(window_rect)

        if not window_rect.contains(player2.rect):
            player2.rect.clamp_ip(window_rect)

        if luck == 1:
            outline.rect.y = player2.rect.y
            outline.rect.x = player2.rect.x
        else:
            outline.rect.y = player1.rect.y
            outline.rect.x = player1.rect.x

# Adding movement for both players

        if event.type == KEYDOWN:
            if event.key == K_a:
                player1.rect.x -= player1_speed
            elif event.key == K_d:
                player1.rect.x += player1_speed
            elif event.key == K_w:
                player1.rect.y -= player1_speed
            elif event.key == K_s:
                player1.rect.y += player1_speed
            elif event.key == K_LEFT:
                player2.rect.x -= player2_speed
            elif event.key == K_RIGHT:
                player2.rect.x += player2_speed
            elif event.key == K_UP:
                player2.rect.y -= player2_speed
            elif event.key == K_DOWN:
                player2.rect.y += player2_speed

# Adding players' and shoe powerup hitboxes

    rect1 = pygame.Rect(player1.rect.x, player1.rect.y, 64, 64)
    rect2 = pygame.Rect(player2.rect.x, player2.rect.y, 64, 64)
    rect3 = pygame.Rect(shoe.rect.x, shoe.rect.y, 64, 64)

# Adding the game end while the health drops to 0 or below due to a bug ;)

    if health <= 0:
        is_running = False

# Adding collisions

    if rect1.colliderect(rect2):
        health -= 1
        health_bar.rect.y = 700
        half_health_bar.rect.y = 575
        prany = ran.randint(0, 576)
        pranx = ran.randint(0, 896)
        if luck == 1:
            player1.rect.y = prany
            player1.rect.x = pranx
            player2_speed = 16
        else:
            player2.rect.y = prany
            player2.rect.x = pranx
            player1_speed = 16

    if rect3.colliderect(rect2):
        if luck == 1:
            nrany = ran.randint(0, 576)
            nranx = ran.randint(0, 896)
            shoe.rect.x = nranx
            shoe.rect.y = nrany
            player2_speed += 8
            ting.play()
    if rect3.colliderect(rect1):
        if luck == 2:
            nrany = ran.randint(0, 576)
            nranx = ran.randint(0, 896)
            shoe.rect.x = nranx
            shoe.rect.y = nrany
            player1_speed += 8
            ting.play()

# Printing some values so testing is easier

    # print(player1.rect.x, player1.rect.y, health)
    # print(player2.rect.x, player2.rect.y, health)
    all_sprites.update()

# Adding the white background

    window.fill((0, 0, 0))

# Updating the sprites

    all_sprites.draw(window)

    pygame.display.flip()

# Ending the game
pygame.mixer.quit()
pygame.quit()
