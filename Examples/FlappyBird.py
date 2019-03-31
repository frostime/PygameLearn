# -*- coding: utf-8 -*-
import pygame
from pygame.math import Vector2
import sys
from random import randint


gameSize = (480, 640)
# bird的x坐标
birdXCord = 172
birdSize = (55, 40)
# 柱子宽度
pillarWidth = 75
# 水平两个柱子之间的空白区域的宽度
hInterval = 190
# 上下两根柱子之间的距离
vInterval = 160
# 柱子最少多长
minPillarHeight = 30
maxPillarHeight = gameSize[1] - minPillarHeight - vInterval
# 画面移动速度 pixels/s
moveSpeed = 100
# 重力加速度 pixels / s^2
g = 600
# 每次按键，向上加速 pixels / s
vRender = -500
# 向上最大的速度，防止一直render
maxVUp = -450



class Bird(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.surface.Surface(birdSize)
        self.image.fill((0, 0, 0))
        self.hPos = (gameSize[1] - birdSize[1]) // 2
        self.rect = pygame.rect.Rect((birdXCord, self.hPos), birdSize)
        # 速度，以向下为正方向
        self.v = -10

    def update(self, dt):
        # print(self.hPos, self.v)
        dx = self.v * dt
        dv = g * dt
        self.hPos += dx
        self.v += dv
        # 把连续的位置放到离散的像素中
        topPixel = round(self.hPos)
        if topPixel < 0:
            topPixel = 0
            self.hPos = topPixel
            self.v = 0
        elif topPixel > (gameSize[1] - birdSize[1]):
            topPixel = gameSize[1] - birdSize[1]
            self.hPos = topPixel
            self.v = 0
        self.rect.top = topPixel

    def render(self):
        self.v += vRender
        # 防止向上速度过大
        self.v = max(self.v, maxVUp)


class Pillar(pygame.sprite.Sprite):
    def __init__(self, length, up=False):
        """长度多少, 是不是上面的柱子"""
        size = (pillarWidth, length)
        if up:
            pos = (gameSize[0], 0)
        else:
            pos = (gameSize[0], gameSize[1] - length)
        self.rect = pygame.rect.Rect(pos, size)
        self.image = pygame.surface.Surface((size))
        self.image.fill((0, 0, 0))

    def update(self, dx):
        self.rect.left -= dx
        # print(self.rect.left)


class Game(object):
    def __init__(self, FPS=40):
        pygame.init()
        self.size = gameSize
        self.screen = pygame.display.set_mode(gameSize)
        pygame.display.set_caption('Flappy Bird')
        self.initWidgets()
        self.FPS = FPS
        # self.sound = pygame.mixer.Sound(r'../Media/jump.wav')
        self.clock = pygame.time.Clock()

    def initWidgets(self):
        self.bird = Bird()
        # 按顺序放上下的柱子
        pUp, pDown = self.generatePillar()
        self.pillars = [pUp, pDown]
        # 记录最后一根柱子左侧距离屏幕的距离
        self.lastPillarLeft = 0

    def generatePillar(self):
        height1 = randint(minPillarHeight, maxPillarHeight)
        height2 = gameSize[1] - height1 - vInterval
        pUp = Pillar(height1, True)
        pDown = Pillar(height2, False)
        return pUp, pDown


    def run(self):
        print('Game Start')
        while True:
            dt = self.clock.tick(self.FPS) / 1000
            self.event()
            self.update(dt)
            self.draw()

    def gameStart(self):
        gameNotStart = True
        while gameNotStart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    gameNotStart = False
            self.draw()
        self.run()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.bird.render()
                # self.sound.play()
        if self.lastPillarLeft >= (hInterval + pillarWidth):
            pUp, pDown = self.generatePillar()
            self.pillars.append(pUp)
            self.pillars.append(pDown)
            self.lastPillarLeft = 0
        right = self.pillars[0].rect.right
        if right < 0:
            self.pillars.pop(0)
            self.pillars.pop(0)
        # print(len(self.pillars))

    def update(self, dt):
        self.bird.update(dt)
        dx = moveSpeed * dt
        for p in self.pillars:
            p.update(dx)
        # print(self.pillars[0].rect.left)
        self.lastPillarLeft += dx
        # print(self.lastPillarLeft)

    def exit(self):
        pygame.quit()
        sys.exit()

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.bird.image, self.bird.rect)
        for p in self.pillars:
            self.screen.blit(p.image, p.rect)
        pygame.display.update()


def main():
    import os
    os.chdir(os.path.dirname(__file__))
    game = Game(FPS=50)
    game.gameStart()


if __name__ == '__main__':
    main()
