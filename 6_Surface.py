"""
这一节将Surface的使用
特别提一下convert的问题，一般在load一个image之后，应该调用一下convert()方法从而加快运行效率，此外，在需要透明图片的时候需要调用convert_alpha()

class pygame.Surface:
    Surface((width, height), flags=0, depth=0, masks=None) -> Surface
    set_clip(rect) -> None:
        设定只有rect区域内的部分可以被更新update, 其他部分不被更新
        应用场景: 比如魔兽上面是菜单，下面是操作面板，中间的小兵和英雄打的不可开交时候，上下的部分也是保持相对不动的
    subsurface(Rect) -> Surface:
        在一个Surface中再提取一个Surface，当往Subsurface上画东西的时候，同时也向父表面上操作
    set_at((x, y), Color) -> None:
        设置某一像素的RGB
    fill(color, rect=None, special_flags=0) -> Rect
    convert(Surface) -> Surface
    convert(depth, flags=0) -> Surface
    convert(masks, flags=0) -> Surface
    convert() -> Surface
        更改像素的格式，返回更改后的Surface
        如果没有参数，那么会按照display的Surface(screen)的格式进行更改，这样做可以让blit的速度提高
        注意，对于具有alpha通道的图片，该方法会去除透明成分
    convert_alpha(Surface) -> Surface
    convert_alpha() -> Surface
        同上，但是会保留alpha成分

class pygame.Rect:
    矩形区域类，表示游戏界面中某一块矩形区域, 在locals中也有定义
    非常有用!
    https://www.pygame.org/docs/ref/rect.html
    Rect(left, top, width, height) -> Rect
    Rect((left, top), (width, height)) -> Rect
    collidepoint(x, y) -> bool
    collidepoint((x,y)) -> bool
        点是否在Rect内
    colliderect(Rect) -> bool:
        两个Rect是否相交

"""
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import random
import os


def testConvert():
    pygame.init()
    width = 640
    height = 480
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Hello World!")
    background = pygame.image.load(r'./Image/sushiplate.jpg').convert()
    img1 = pygame.image.load(r'./Image/fugu.png').convert()
    img2 = pygame.image.load(r'./Image/fugu.png').convert_alpha()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        screen.blit(background, (0, 0))
        screen.blit(img1, (0, 0))
        screen.blit(img2, (320, 240))
        pygame.display.update()


def testRect():
    """矩形的测试"""
    pygame.init()
    width = 640
    height = 480
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Rect")
    rect1 = Rect(0, 0, 320, 240)
    rect2 = Rect(0, 240, 320, 240)
    overlap = rect1.colliderect(rect2)
    print('rect1和rect2有交叉:', overlap)
    while True:
        event = pygame.event.wait()
        if event.type == QUIT:
            pygame.quit()
            return
        elif event.type == MOUSEMOTION:
            pos = event.pos
            if rect1.collidepoint(pos):
                print('鼠标在rect1内')
            if rect2.collidepoint(pos):
                print('鼠标在rect2内')
        pygame.display.update()


def testClipping():
    fontPath = r'C:\Windows\Fonts\SIMKAI.ttf'
    pygame.init()
    background = pygame.image.load(r'./Image/sushiplate.jpg').convert()
    size = (640, 480)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Clip')
    font = pygame.font.Font(fontPath, 20)
    text = font.render('只有左半边屏幕被更新', True, (0, 0, 0), (255, 255, 255))
    (w, h) = text.get_size()
    at = [0, 240 - h // 2]
    direct = 1
    # 设置只让左半边的屏幕信息可以被更新
    rect = Rect(0, 0, 320, 480)
    # 预先绘制背景, 否则右半边什么也没有
    screen.blit(background, (0, 0))
    screen.set_clip(rect)
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


def testSubsurface():
    pygame.init()
    img = pygame.image.load(r'./Image/animals.bmp').convert()
    screen = pygame.display.set_mode((480, 480))
    animals = []
    # 把子图截取出来
    for y in range(0, 800, 40):
        loc = Rect(0, y, 40, 40)
        subImg = img.subsurface(loc)
        animals.append(subImg)
    while True:
        event = pygame.event.wait()
        if event.type == QUIT:
            pygame.quit()
            return
        # 随机绘制到screen上面
        for i in range(0, 480, 40):
            for j in range(0, 480, 40):
                x = random.randint(0, 19)
                img = animals[x]
                screen.blit(img, (i, j))
        pygame.display.update()


def testFillPixel():
    """使用Surface的fill和set_at方法绘制星空图"""
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    screen.fill((6, 15, 58))
    starNum = random.randint(500, 1000)
    for i in range(starNum):
        x = random.randint(0, 500)
        y = random.randint(0, 500)
        screen.set_at((x, y), (200, 200, 200))
    pygame.display.update()
    os.system('pause')


if __name__ == '__main__':
    testConvert()
