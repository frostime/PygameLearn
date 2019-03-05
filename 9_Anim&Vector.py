import numpy as np
from sys import exit
from pygame.locals import *
import pygame
background_image_filename = r'./Image/sushiplate.jpg'
sprite_image_filename = r'./Image/fugu.png'


pygame.init()

screen = pygame.display.set_mode((640, 480), 0, 32)

background = pygame.image.load(background_image_filename).convert()
sprite = pygame.image.load(sprite_image_filename).convert_alpha()

clock = pygame.time.Clock()

sprite_pos = np.array([200, 150])
sprite_speed = 300.

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    pressed_keys = pygame.key.get_pressed()

    key_direction = np.array([0, 0])
    if pressed_keys[K_LEFT]:
        key_direction[0] = -1
    elif pressed_keys[K_RIGHT]:
        key_direction[0] = +1
    if pressed_keys[K_UP]:
        key_direction[1] = -1
    elif pressed_keys[K_DOWN]:
        key_direction[1] = +1

    key_direction.normalize()

    screen.blit(background, (0, 0))
    screen.blit(sprite, sprite_pos)

    time_passed = clock.tick(30)
    time_passed_seconds = time_passed / 1000.0

    sprite_pos += key_direction * sprite_speed * time_passed_seconds

    pygame.display.update()
