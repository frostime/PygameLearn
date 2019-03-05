# -*- coding: utf-8 -*-
"""
在游戏界面上绘制文字内容
pygame.font：
    SysFont(name, size, bold=False, italic=False) -> font:
        name是一个字符串, 返回Font对象, 这种方法无法使用中文
    class Font:
        Font(filename, size) -> Font
        Font(object, size) -> Font
            根据字体文件构造字体, size以pixels为单位
            这种方式可以使用中文
        render(text, antialias, color, background=None) -> Surface:
            按照字体绘制文字，返回Surface对象
            第一个参数是写的文字
            第二个参数是个布尔值，以为这是否开启抗锯齿，就是说True的话字体会比较平滑，不过相应的速度有一点点影响
            第三个参数是字体的颜色, 如RGB元组(0, 0, 0)
            第四个是背景色，如果你想没有背景色（也就是透明），那么可以不加这第四个参数
"""
import pygame
from pygame.locals import *


def testFont():
    """
    使用字体, 汉语部分无法正常显示
    文字会在屏幕中央飘来飘去
    """
    pygame.init()
    background = pygame.image.load(r'./Image/sushiplate.jpg').convert()
    size = (640, 480)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('使用字体, 但无法使用中文')
    # 楷体字
    font = pygame.font.SysFont(r'SIMKAI', 24)
    text = font.render('You can\'t use 汉语', True, (0, 0, 0), (255, 255, 255))
    (w, h) = text.get_size()
    at = [0, 240 - h // 2]
    direct = 1
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        x = at[0]
        x = (x + direct)
        at[0] = x
        if x == 0 or x == (size[0] - w):
            direct = -direct
        screen.blit(background, (0, 0))
        screen.blit(text, at)
        pygame.display.update()


def useChinese():
    fontPath = r'C:\Windows\Fonts\SIMKAI.ttf'
    pygame.init()
    background = pygame.image.load(r'./Image/sushiplate.jpg').convert()
    size = (640, 480)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('使用字体')
    font = pygame.font.Font(fontPath, 20)
    text = font.render('汉语', True, (0, 0, 0), (255, 255, 255))
    (w, h) = text.get_size()
    at = [0, 240 - h // 2]
    direct = 1
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        x = at[0]
        x = (x + direct)
        at[0] = x
        if x == 0 or x == (size[0] - w):
            direct = -direct
        screen.blit(background, (0, 0))
        screen.blit(text, at)
        pygame.display.update()


def main():
    useChinese()
    # testFont()


if __name__ == '__main__':
    main()
