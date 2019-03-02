import pygame
from pygame.locals import *
from sys import exit
import os

pygame.init()
screen = screen = pygame.display.set_mode((640, 480))

while True:
    events = pygame.event.get()
    for event in events:
        print(event)
        if event.type == pygame.QUIT:
            exit()
    pygame.display.update()
    os.system('pause')
