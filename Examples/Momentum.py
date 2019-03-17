# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
"""
经典物理题目，光滑地板上滑块碰撞

关于这个命题，可以去看看3blue1brown的一期节目:
两个滑块相撞，如果质量的的差距是(100^n)的话，那碰撞的次数会是圆周率的前n-1位

然而这里由于像素的限制，无法精确模拟，看着玩就行了

其实最好是自己设定采样时间间隔，尽可能精准地进行数值模拟，然后大致地画在屏幕上面
"""
import os
import sys
import logging
import pygame
import pygame.font as font

d = os.path.dirname(__file__)
os.chdir(d)
sys.path.append(r'..')

try:
    from vector import Vector
except ImportError as err:
    print(err)
    sys.exit()


FORMAT = "%(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)


class Block(pygame.sprite.Sprite):
    def __init__(self, mass: int, edge: float,
                 v: Vector, loc: tuple):
        self.image = pygame.surface.Surface((edge, edge))
        self.mass = mass
        self.velocity = v
        self.rect = pygame.rect.Rect(loc[0], loc[1], edge, edge)
        self.image.fill((255, 255, 255))
        pygame.draw.rect(self.image, (0, 0, 0),
                         (0, 0, edge, edge), 1)
        f = font.SysFont(r'SIMKAI', 18)
        text = f.render('m = {}'.format(mass), True,
                        (0, 0, 0), (255, 255, 255))
        (w, h) = text.get_size()
        at = [edge // 2 - w // 2, edge // 2 - h // 2]
        self.image.blit(text, at)
        self.enable = True

    def update(self, dt):
        dx = self.velocity * dt
        self.move(dx.x)

    def move(self, dx):
        if -1 < dx < 0:
            dx = -1
        elif 0 < dx < 1:
            dx = 1
        self.rect = self.rect.move(dx, 0)
        # logging.info('Move: {}'.format(dx))

    @staticmethod
    def crashWith(block1, block2):
        m1 = block1.mass
        v1 = block1.velocity
        m2 = block2.mass
        v2 = block2.velocity
        block1.velocity = (((m1 - m2) * v1 + 2 * m2 * v2) /
                           (m1 + m2))
        block2.velocity = (((m2 - m1) * v2 + 2 * m1 * v1) /
                           (m1 + m2))
        logging.info('Crashed!')
        logging.info('Block1: {}-->{}'.format(v1, block1.velocity))
        logging.info('Block2: {}-->{}'.format(v2, block2.velocity))
        logging.info('')

    def reverseX(self):
        self.velocity.x = -self.velocity.x


class Game(object):
    def __init__(self, screenSize, FPS, bigMass=1, v=20):
        pygame.init()
        self.size = screenSize
        self.screen = pygame.display.set_mode(screenSize)
        pygame.display.set_caption('')
        self.initWidgets(bigMass, v)
        self.FPS = FPS
        self.crashTime = 0
        self.clock = pygame.time.Clock()

    def initWidgets(self, bigMass, v):

        smallMass = 1
        smallEdge = 50
        pos = (240, self.screen.get_height() - smallEdge)
        self.smallBlock = Block(smallMass, smallEdge, Vector([0, 0]), pos)
        bigMass = bigMass
        bigEdge = round(smallEdge * ((bigMass / smallMass) ** (1 / 3)))
        pos = (680, self.screen.get_height() - bigEdge)
        self.bigBlock = Block(bigMass, bigEdge, Vector([-v, 0]), pos)

    def run(self):
        while True:
            dt = self.clock.tick(self.FPS) / 1000
            self.event()
            self.update(dt)
            self.draw()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()

        if not self.smallBlock.enable and not self.bigBlock.enable:
            self.exit()

        # 反弹
        if self.smallBlock.rect.left <= 1:
            self.crashTime += 1
            self.smallBlock.reverseX()
            if self.smallBlock.rect.left < 0:
                self.smallBlock.move(-self.smallBlock.rect.left)

        # 碰撞
        if self.smallBlock.enable and self.bigBlock.enable:
            interval = self.bigBlock.rect.left - self.smallBlock.rect.right
            if interval <= 1:
                self.crashTime += 1
                Block.crashWith(self.smallBlock, self.bigBlock)
                self.smallBlock.move(-1)
                self.bigBlock.move(1)

        # 消失
        if self.smallBlock.enable:
            if self.smallBlock.rect.left >= self.screen.get_width():
                self.smallBlock.enable = False
        if self.bigBlock.enable:
            if self.bigBlock.rect.left >= self.screen.get_width():
                self.bigBlock.enable = False

    def update(self, dt):
        # TODO
        self.smallBlock.update(dt)
        self.bigBlock.update(dt)

    def exit(self):
        pygame.quit()
        sys.exit()

    def draw(self):
        f = font.SysFont(r'SIMKAI', 24)
        text = f.render('Crash Times: {}'.format(self.crashTime),
                        True, (0, 0, 0), (255, 255, 255))
        self.screen.fill((255, 255, 255))
        self.screen.blit(text, (0, 0))
        if self.smallBlock.enable:
            self.screen.blit(self.smallBlock.image, self.smallBlock.rect)
        if self.bigBlock.enable:
            self.screen.blit(self.bigBlock.image, self.bigBlock.rect)
        pygame.display.update()


def main():
    game = Game((800, 300), FPS=200, bigMass=20, v=200)
    game.run()


if __name__ == '__main__':
    main()
