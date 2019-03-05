"""
这节还是讲动画，不涉及新的模块，而是讲述如何使用向量来描述复杂运动
完成功能：鼠标引导物体移动的功能
我看的教程里向量用的是一个gamesobjects库，然而那个库用conda安装不了，我又不喜欢它的API，所以用numpy自己写了一个Vecotr类，在vector.py中
"""
from vector import Vector
from sys import exit
from pygame.locals import *
import pygame
import random


class StarSkyBackground(object):
    """绘制星空背景图"""
    def __init__(self, screenSize):
        w, h = screenSize[0], screenSize[1]
        self.backcolor = (6, 15, 58)
        starNum = random.randint(500, 1000)
        self.stars = []
        self.starcolor = (200, 200, 200)
        for i in range(starNum):
            x = random.randint(0, w)
            y = random.randint(0, h)
            self.stars.append((x, y))

    def draw(self, screen):
        screen.fill(self.backcolor)
        for star in self.stars:
            screen.set_at(star, self.starcolor)


def run(FPS=60, v=50):
    pygame.init()
    screenSize = (720, 560)
    screen = pygame.display.set_mode(screenSize)
    background = StarSkyBackground(screenSize)
    ship = pygame.image.load(r'./Image/playership.png').convert_alpha()
    clock = pygame.time.Clock()
    # 飞船位置
    position = Vector([100.0, 100.0])
    # 运动速度大小
    velocity = v
    while True:
        timePassed = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
        background.draw(screen)
        screen.blit(ship, position)
        # 鼠标位置
        mouse = Vector(pygame.mouse.get_pos())
        # ship信息
        shipSize = ship.get_size()
        # ship的中心位置
        shipPos = position + Vector(shipSize) / 2
        # 运动方向，用单位向量描述
        toward = (mouse - shipPos).normalize()
        # 速度向量
        v = toward * velocity
        print('{}---->{}, V = {}'.format(shipPos, mouse, v))
        position += v * timePassed / 1000
        pygame.display.update()

run(v=100)
