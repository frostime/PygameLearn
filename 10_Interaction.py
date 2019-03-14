"""
游戏总是需要交互的，一般交互用的都是键盘鼠标（顶多加个手柄）
在之前我们使用过事件监听来判断操作，不过有更加简单的方法
使用pygame.key和pygame.mouse

此外我们还可以使用pygame.transform对图像进行旋转、拉伸等变换，但是注意一点
在变换是一定要针对原Surface进行变换，不要对变换后的Surface再变换，否则会失真
"""
import random

import numpy as np
import pygame
from pygame.locals import *

from vector import Vector


class StarSkyBackground(object):
    """绘制星空背景图"""

    def __init__(self, screenSize, starNum=(500, 1000)):
        w, h = screenSize[0], screenSize[1]
        self.backcolor = (6, 15, 58)
        starNum = random.randint(*starNum)
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


def getShipLT(ship, center):
    """获取飞船左上角点"""
    shipSize = ship.get_size()
    # ship的中心位置
    shipPos = center - Vector(shipSize) / 2
    return shipPos


def computeRotateDegree(ship, center, toward):
    """飞船跟着鼠标的方向旋转，计算旋转的角度"""
    mouse = pygame.mouse.get_pos()
    mouse = Vector(mouse)
    # 从飞船到鼠标的向量
    to = (mouse - center).normalize()
    # to = Vector((1, 0))
    # 计算toward和to之间的夹角
    degree = toward.angle(to)
    return degree


def init():
    pygame.init()
    screenSize = (800, 640)
    background = StarSkyBackground(screenSize, (800, 1200))
    screen = pygame.display.set_mode(screenSize)
    ship = pygame.image.load(r'./Image/playership.png').convert_alpha()
    # 飞船正方向, 初始向上
    toward = Vector([0, -1])
    # 飞船初始中心位置
    center = Vector([200, 200])
    background.draw(screen)
    return screen, background, ship, center, toward


def blit(screen, background, ship, center):
    position = getShipLT(ship, center)
    background.draw(screen)
    screen.blit(ship, position)
    shipSize = ship.get_size()
    rect = Rect(position, shipSize)
    pygame.draw.rect(screen, (255, 255, 255), rect, 5)


def thisIsWhatYouShouldNotDo():
    FPS = 60
    screen, background, ship, center, toward = init()
    clock = pygame.time.Clock()
    rotateDegree = 0
    while True:
        timePassed = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
        degree = computeRotateDegree(ship, center, toward)
        # 绘图旋转
        # 由于pygame中坐标系是上下颠倒的
        # 所以角度的正反也要颠倒
        ship = pygame.transform.rotate(ship, -degree)
        # 绘制
        blit(screen, background, ship, center)
        pygame.display.update()


def thisIsWhatYouShouldDo():
    FPS = 60
    screen, background, originShip, center, toward = init()
    ship = originShip
    clock = pygame.time.Clock()
    rotateDegree = 0
    while True:
        timePassed = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
        degree = computeRotateDegree(ship, center, toward)
        # 绘图旋转
        # 由于pygame中坐标系是上下颠倒的
        # 所以角度的正反也要颠倒
        ship = pygame.transform.rotate(originShip, -degree)
        # 绘制
        blit(screen, background, ship, center)
        pygame.display.update()


if __name__ == '__main__':
    thisIsWhatYouShouldDo()
    # try:
    #     thisIsWhatYouShouldNotDo()
    # except:
    #     print('如果你看到这行字，说明程序已经崩了')
    #     print('如果仔细观察一下两个程序有什么不同')
    #     print('你就会发现对ship的处理不同')
    #     print('实际上transform必然会对Surface带来一定的损伤')
