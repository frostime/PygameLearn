"""
游戏总是需要交互的，一般交互用的都是键盘鼠标（顶多加个手柄）
在之前我们使用过事件监听来判断操作，不过有更加简单的方法
使用pygame.key和pygame.mouse


"""
import pygame
from pygame.locals import *
from vector import Vector


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


def main():
    pygame.init()


if __name__ == '__main__':
    main()
